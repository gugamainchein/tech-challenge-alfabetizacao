import json

from pipeline.ingestion.events import Event, parse


def valid_event(**overrides):
    data = dict(
        event_id="abc",
        event_type="nova_medicao",
        produced_at="2026-01-01T00:00:00+00:00",
        id_municipio="3550308",
        ano=2025,
        rede="publica",
        serie=2,
        valor=61.5,
    )
    data.update(overrides)
    return Event(**data)


def test_parse_valid():
    event, error = parse(valid_event().to_bytes())
    assert error is None
    assert event.origem == "simulado"


def test_parse_broken_json():
    event, error = parse(b"{nao e json")
    assert event is None and error


def test_parse_missing_fields():
    _, error = parse(json.dumps({"event_id": "x"}).encode())
    assert error


def test_parse_out_of_range():
    _, error = parse(valid_event(valor=140).to_bytes())
    assert "faixa" in error


def test_parse_bad_municipio():
    _, error = parse(valid_event(id_municipio="35").to_bytes())
    assert "id_municipio" in error
