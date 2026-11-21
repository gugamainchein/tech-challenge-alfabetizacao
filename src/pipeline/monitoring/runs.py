import time
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone

from google.cloud import bigquery


def new_run_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S") + "-" + uuid.uuid4().hex[:6]


class RunTracker:
    """Acumula métricas por etapa e grava em ops.pipeline_runs (append)."""

    def __init__(self, client: bigquery.Client, table: str, run_id: str, pipeline: str):
        self.client = client
        self.table = table
        self.run_id = run_id
        self.pipeline = pipeline

    @contextmanager
    def step(self, name: str):
        metrics = {"rows_in": None, "rows_out": None, "bytes_processed": None}
        started = datetime.now(timezone.utc)
        t0 = time.perf_counter()
        status, error = "success", None
        try:
            yield metrics
        except Exception as exc:
            status, error = "failed", f"{type(exc).__name__}: {exc}"[:1000]
            raise
        finally:
            self._save(name, started, time.perf_counter() - t0, status, error, metrics)

    def _save(self, step, started, duration, status, error, metrics):
        row = {
            "run_id": self.run_id,
            "pipeline": self.pipeline,
            "step": step,
            "started_at": started.isoformat(),
            "duration_s": round(duration, 3),
            "status": status,
            "error": error,
            **metrics,
        }
        errors = self.client.insert_rows_json(self.table, [row])
        if errors:
            raise RuntimeError(f"erro ao gravar métricas de execução: {errors}")
