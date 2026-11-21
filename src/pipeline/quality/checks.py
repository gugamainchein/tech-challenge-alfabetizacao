from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from enum import Enum


class Severity(str, Enum):
    BLOCKING = "bloqueante"
    INFO = "informativa"


class QualityGateError(Exception):
    pass


@dataclass(frozen=True)
class Check:
    name: str
    table: str
    sql: str  # precisa retornar uma única coluna chamada "valor"
    severity: Severity
    min_value: float | None = None
    max_value: float | None = None

    def evaluate(self, value: float | None) -> "CheckResult":
        passed = value is not None
        if passed and self.min_value is not None:
            passed = value >= self.min_value
        if passed and self.max_value is not None:
            passed = value <= self.max_value
        return CheckResult(
            check=self.name,
            table=self.table,
            severity=self.severity.value,
            passed=passed,
            value=value,
            min_value=self.min_value,
            max_value=self.max_value,
        )


@dataclass
class CheckResult:
    check: str
    table: str
    severity: str
    passed: bool
    value: float | None
    min_value: float | None
    max_value: float | None

    def to_row(self, run_id: str, layer: str) -> dict:
        row = asdict(self)
        row.update(
            run_id=run_id,
            layer=layer,
            checked_at=datetime.now(timezone.utc).isoformat(),
        )
        return row


def duplicates(table: str, keys: list[str], severity=Severity.BLOCKING) -> Check:
    cols = ", ".join(keys)
    sql = f"""
        SELECT COUNT(*) AS valor FROM (
          SELECT {cols} FROM `{table}` GROUP BY {cols} HAVING COUNT(*) > 1
        )"""
    return Check(f"duplicidade[{cols}]", table, sql, severity, max_value=0)


def null_ratio(table: str, column: str, max_ratio: float, severity=Severity.INFO) -> Check:
    sql = f"SELECT SAFE_DIVIDE(COUNTIF({column} IS NULL), COUNT(*)) AS valor FROM `{table}`"
    return Check(f"nulos[{column}]", table, sql, severity, max_value=max_ratio)


def unknown_category(table: str, column: str, label: str = "desconhecido") -> Check:
    sql = f"SELECT COUNTIF({column} = '{label}') AS valor FROM `{table}`"
    return Check(f"categoria_desconhecida[{column}]", table, sql, Severity.BLOCKING, max_value=0)


def join_match_rate(
    left: str, right: str, keys: list[str], min_rate: float, severity=Severity.BLOCKING
) -> Check:
    on = " AND ".join(f"l.{k} = r.{k}" for k in keys)
    first = keys[0]
    sql = f"""
        SELECT SAFE_DIVIDE(COUNTIF(r.{first} IS NOT NULL), COUNT(*)) AS valor
        FROM `{left}` l
        LEFT JOIN (SELECT DISTINCT {", ".join(keys)} FROM `{right}`) r ON {on}"""
    name = f"match_join[{left.split('.')[-1]}->{right.split('.')[-1]}]"
    return Check(name, left, sql, severity, min_value=min_rate)


def enforce(results: list[CheckResult]) -> None:
    failed = [r for r in results if not r.passed and r.severity == Severity.BLOCKING.value]
    if failed:
        names = ", ".join(f"{r.check} ({r.table}) = {r.value}" for r in failed)
        raise QualityGateError(f"{len(failed)} regra(s) bloqueante(s) falharam: {names}")
