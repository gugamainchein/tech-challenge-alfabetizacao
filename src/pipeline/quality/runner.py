import logging

from google.cloud import bigquery

from pipeline.quality.checks import Check, CheckResult, enforce

log = logging.getLogger(__name__)


def run_checks(
    client: bigquery.Client, checks: list[Check], run_id: str, layer: str, results_table: str
) -> list[CheckResult]:
    results = []
    for check in checks:
        row = next(iter(client.query(check.sql).result()))
        result = check.evaluate(row["valor"])
        status = "ok" if result.passed else "FALHOU"
        log.info("%s %s -> %s (%s)", layer, check.name, result.value, status)
        results.append(result)

    # grava antes de aplicar o gate, senão a falha some junto com a execução
    errors = client.insert_rows_json(results_table, [r.to_row(run_id, layer) for r in results])
    if errors:
        raise RuntimeError(f"erro ao gravar resultados de qualidade: {errors}")

    enforce(results)
    return results
