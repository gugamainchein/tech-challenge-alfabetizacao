import logging
import random
import time
import uuid
from datetime import datetime, timezone

from google.cloud import pubsub_v1

from pipeline.ingestion.events import EVENT_TYPES, Event
from pipeline.settings import Settings

log = logging.getLogger(__name__)


def fake_event(municipios: list[str]) -> Event:
    return Event(
        event_id=str(uuid.uuid4()),
        event_type=random.choice(sorted(EVENT_TYPES)),
        produced_at=datetime.now(timezone.utc).isoformat(),
        id_municipio=random.choice(municipios),
        ano=2025,
        rede="publica",  # TODO usar os códigos do dicionário
        serie=2,
        valor=round(random.uniform(20, 95), 2),
    )


def produce(settings: Settings, municipios: list[str], n: int, dup_rate=0.05, bad_rate=0.03):
    publisher = pubsub_v1.PublisherClient()
    topic = publisher.topic_path(settings.project_id, settings.topic)
    last = None

    for _ in range(n):
        roll = random.random()
        if last is not None and roll < dup_rate:
            payload = last  # duplicado de propósito (simula entrega repetida)
        elif roll < dup_rate + bad_rate:
            payload = b'{"event_id": "x", "valor": "abc"}'
        else:
            payload = fake_event(municipios).to_bytes()
            last = payload

        publisher.publish(topic, payload).result()
        time.sleep(random.uniform(0.01, 0.2))

    log.info("%d eventos publicados em %s", n, topic)
