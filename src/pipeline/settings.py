import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import yaml
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Settings:
    project_id: str
    region: str
    bq_location: str
    bucket: str
    topic: str
    subscription: str
    alert_webhook: str | None
    config: dict

    def table(self, layer: str, name: str) -> str:
        dataset = self.config["datasets"][layer]
        return f"{self.project_id}.{dataset}.{name}"

    def source_table(self, name: str) -> str:
        src = self.config["source"]
        return f"{src['project']}.{src['dataset']}.{name}"


def _required(var: str) -> str:
    value = os.getenv(var)
    if not value:
        raise RuntimeError(f"variável de ambiente {var} não definida (ver .env.example)")
    return value


@lru_cache
def get_settings() -> Settings:
    load_dotenv(ROOT / ".env")
    with open(ROOT / "config" / "pipeline.yaml", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    return Settings(
        project_id=_required("GCP_PROJECT_ID"),
        region=os.getenv("GCP_REGION", "southamerica-east1"),
        bq_location=os.getenv("BQ_LOCATION", "US"),
        bucket=_required("GCS_BUCKET"),
        topic=os.getenv("PUBSUB_TOPIC", "alfabetizacao-eventos"),
        subscription=os.getenv("PUBSUB_SUBSCRIPTION", "alfabetizacao-eventos-sub"),
        alert_webhook=os.getenv("ALERT_WEBHOOK_URL") or None,
        config=config,
    )
