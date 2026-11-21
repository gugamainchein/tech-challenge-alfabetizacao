import json
from dataclasses import asdict, dataclass

EVENT_TYPES = {"atualizacao_indicador", "nova_medicao", "atualizacao_meta"}


@dataclass
class Event:
    event_id: str
    event_type: str
    produced_at: str  # momento em que o evento foi gerado no produtor
    id_municipio: str
    ano: int
    rede: str
    serie: int
    valor: float
    origem: str = "simulado"

    def to_bytes(self) -> bytes:
        return json.dumps(asdict(self)).encode("utf-8")


def parse(payload: bytes) -> tuple[Event | None, str | None]:
    try:
        data = json.loads(payload)
        event = Event(**data)
    except (ValueError, TypeError) as exc:
        return None, f"payload inválido: {exc}"

    if event.event_type not in EVENT_TYPES:
        return None, f"event_type desconhecido: {event.event_type}"
    if not (0 <= float(event.valor) <= 100):
        return None, f"valor fora da faixa: {event.valor}"
    if not event.id_municipio or len(str(event.id_municipio)) != 7:
        return None, f"id_municipio inválido: {event.id_municipio}"
    return event, None
