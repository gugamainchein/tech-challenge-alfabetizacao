import argparse
import logging
import sys
from pathlib import Path

from google.cloud import bigquery

from pipeline.ingestion import batch
from pipeline.monitoring.alerts import notify_failure
from pipeline.monitoring.runs import RunTracker, new_run_id
from pipeline.settings import ROOT, get_settings

log = logging.getLogger("pipeline")

SQL_DIR = ROOT / "sql"


def run_sql_layer(client: bigquery.Client, settings, layer: str, tracker: RunTracker) -> None:
    for path in sorted(Path(SQL_DIR / layer).glob("*.sql")):
        sql = path.read_text(encoding="utf-8").format(project=settings.project_id)
        with tracker.step(f"{layer}:{path.stem}") as m:
            job = client.query(sql)
            job.result()
            m["bytes_processed"] = job.total_bytes_processed
            m["rows_out"] = job.num_dml_affected_rows


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="pipeline")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("batch")
    sub.add_parser("silver")
    sub.add_parser("gold")
    p = sub.add_parser("produce")
    p.add_argument("--n", type=int, default=500)
    sub.add_parser("consume")
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
    settings = get_settings()
    client = bigquery.Client(project=settings.project_id, location=settings.bq_location)
    run_id = new_run_id()
    tracker = RunTracker(client, settings.table("ops", "pipeline_runs"), run_id, args.cmd)

    try:
        if args.cmd == "batch":
            for table in settings.config["tables"]:
                with tracker.step(f"bronze:{table}") as m:
                    info = batch.extract_to_bronze(client, settings, table, run_id)
                    m["bytes_processed"] = info["bytes_processed"]
                    log.info("%s exportada, job %s", table, info["job_id"])
        elif args.cmd in ("silver", "gold"):
            run_sql_layer(client, settings, args.cmd, tracker)
            # TODO rodar checks da camada antes de publicar (quality.runner)
        elif args.cmd == "produce":
            raise NotImplementedError("carregar lista de municípios da silver e chamar produce()")
        elif args.cmd == "consume":
            raise NotImplementedError("loop de micro-lotes com stream_consumer.consume_batch")
    except Exception as exc:
        log.exception("execução %s falhou", run_id)
        notify_failure(settings.alert_webhook, run_id, args.cmd, str(exc))
        return 1

    log.info("execução %s concluída", run_id)
    return 0


if __name__ == "__main__":
    sys.exit(main())
