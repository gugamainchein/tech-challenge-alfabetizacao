import pytest

from pipeline.quality.checks import (
    Check,
    QualityGateError,
    Severity,
    duplicates,
    enforce,
    join_match_rate,
)


def make_check(severity=Severity.BLOCKING, min_value=None, max_value=None):
    return Check("teste", "p.d.t", "SELECT 1 AS valor", severity, min_value, max_value)


def test_max_value():
    check = make_check(max_value=0)
    assert check.evaluate(0).passed
    assert not check.evaluate(3).passed


def test_min_value():
    check = make_check(min_value=0.98)
    assert check.evaluate(0.99).passed
    assert not check.evaluate(0.97).passed


def test_null_value_fails():
    assert not make_check(max_value=0).evaluate(None).passed


def test_enforce_blocks_on_blocking_failure():
    results = [make_check(max_value=0).evaluate(5)]
    with pytest.raises(QualityGateError):
        enforce(results)


def test_enforce_ignores_informative_failure():
    results = [make_check(Severity.INFO, max_value=0).evaluate(5)]
    enforce(results)


def test_duplicates_sql_groups_by_keys():
    check = duplicates("p.silver.municipio", ["id_municipio", "ano"])
    assert "GROUP BY id_municipio, ano" in check.sql
    assert check.max_value == 0


def test_join_match_rate_threshold():
    check = join_match_rate("p.silver.a", "p.silver.b", ["id_municipio"], 0.98)
    assert check.min_value == 0.98
    assert "LEFT JOIN" in check.sql
