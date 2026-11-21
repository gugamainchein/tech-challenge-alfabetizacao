import logging
from dataclasses import asdict
from datetime import datetime, timezone

from google.cloud import bigquery, pubsub_v1

from pipeline.ingestion.events import parse
from pipeline.settings import Settings

log = logging.getLogger(__name__)


def consume_batch(settings: Settings, bq: bigquery.Client, max_messages: int = 200) -> dict:
    """Puxa um micro-lote do Pub/Sub, valida e grava na bronze de streaming.

    Dedup aqui é só dentro do lote; a dedup entre lotes fica no MERGE da silver,
    porque o Pub/Sub entrega pelo menos uma vez.
    """
    subscriber = pubsub_v1.SubscriberClient()
    sub = subscriber.subscription_path(settings.project_id, settings.subscription)
    resp = subscriber.pull(request={"subscription": sub, "max_messages": max_messages}, timeout=30)

    ingested_at = datetime.now(timezone.utc).isoformat()
    valid, invalid, seen, ack_ids = [], [], set(), []

    for msg in resp.received_messages:
        ack_ids.append(msg.ack_id)
        event, error = parse(msg.message.data)
        if error:
            invalid.append({
                "message_id": msg.message.message_id,
                "payload": msg.message.data.decode("utf-8", "replace"),
                "error": error,
                "ingested_at": ingested_at,
            })
            continue
        if event.event_id in seen:
            continue
        seen.add(event.event_id)
        valid.append({**asdict(event), "ingested_at": ingested_at})

    if valid:
        _insert(bq, settings.table("bronze", "eventos_stream"), valid)
    if invalid:
        _insert(bq, settings.table("bronze", "eventos_invalidos"), invalid)

    # só confirma depois de gravar; se cair antes, a mensagem volta
    if ack_ids:
        subscriber.acknowledge(request={"subscription": sub, "ack_ids": ack_ids})

    return {"received": len(ack_ids), "valid": len(valid), "invalid": len(invalid)}


def _insert(bq: bigquery.Client, table: str, rows: list[dict]) -> None:
    errors = bq.insert_rows_json(table, rows)
    if errors:
        raise RuntimeError(f"falha ao inserir em {table}: {errors[:3]}")
