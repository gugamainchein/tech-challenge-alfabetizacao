import logging

import requests

log = logging.getLogger(__name__)


def notify_failure(webhook_url: str | None, run_id: str, pipeline: str, error: str) -> None:
    # complementa a alert policy do Cloud Monitoring, não substitui
    if not webhook_url:
        log.warning("ALERT_WEBHOOK_URL vazio, notificação não enviada")
        return
    text = f"Pipeline `{pipeline}` falhou (run {run_id}): {error}"
    resp = requests.post(webhook_url, json={"content": text, "text": text}, timeout=10)
    resp.raise_for_status()
