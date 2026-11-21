import logging
from datetime import date

from google.cloud import bigquery

from pipeline.settings import Settings

log = logging.getLogger(__name__)


def build_select(settings: Settings, table: str, run_id: str) -> str:
    cols = settings.config["tables"][table]["columns"]
    cols = cols if isinstance(cols, str) else ", ".join(cols)
    return f"""
        SELECT {cols},
               CURRENT_TIMESTAMP() AS _ingested_at,
               '{run_id}' AS _run_id,
               'oficial' AS _origem
        FROM `{settings.source_table(table)}`"""


def dry_run_bytes(client: bigquery.Client, sql: str) -> int:
    cfg = bigquery.QueryJobConfig(dry_run=True, use_query_cache=False)
    return client.query(sql, job_config=cfg).total_bytes_processed


def extract_to_bronze(client: bigquery.Client, settings: Settings, table: str, run_id: str) -> dict:
    select = build_select(settings, table, run_id)
    scanned = dry_run_bytes(client, select)
    log.info("%s: dry run estima %.1f MB", table, scanned / 1e6)

    # caminho novo a cada execução, nada é sobrescrito
    uri = (
        f"gs://{settings.bucket}/bronze/{table}/"
        f"ingestion_date={date.today().isoformat()}/run_id={run_id}/*.parquet"
    )
    sql = f"""
        EXPORT DATA OPTIONS (
          uri = '{uri}', format = 'PARQUET', compression = 'SNAPPY', overwrite = false
        ) AS {select}"""
    job = client.query(sql)
    job.result()

    return {
        "table": table,
        "job_id": job.job_id,
        "bytes_processed": job.total_bytes_processed,
        "dry_run_bytes": scanned,
        "uri": uri,
    }
