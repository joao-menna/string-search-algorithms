from __future__ import annotations

import atexit
import json
from collections.abc import Sequence
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from typing import Any

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import ReadableSpan, TracerProvider
from opentelemetry.sdk.trace.export import (
    SimpleSpanProcessor,
    SpanExporter,
    SpanExportResult,
)

SERVICE_NAME = "string-search-algorithms"
SPAN_NAME = "string_search.run"

_TRACER = trace.get_tracer(SERVICE_NAME)
_LOCK = Lock()
_CONFIGURED = False
_PROVIDER: TracerProvider | None = None
_EXPORT_PATH: Path | None = None


def _to_iso(timestamp_ns: int) -> str:
    return datetime.fromtimestamp(
        timestamp_ns / 1_000_000_000, tz=timezone.utc
    ).isoformat()


class JsonLinesSpanExporter(SpanExporter):
    def __init__(self, output_path: Path) -> None:
        self.output_path = output_path
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = Lock()

    def export(self, spans: Sequence[ReadableSpan]) -> SpanExportResult:
        records: list[dict[str, Any]] = []

        for span in spans:
            if span.name != SPAN_NAME or span.context is None:
                continue

            if span.start_time is None or span.end_time is None:
                continue

            attributes = dict(span.attributes or {})
            records.append(
                {
                    "trace_id": f"{span.context.trace_id:032x}",
                    "span_id": f"{span.context.span_id:016x}",
                    "parent_span_id": (
                        f"{span.parent.span_id:016x}" if span.parent else None
                    ),
                    "name": span.name,
                    "status": span.status.status_code.name,
                    "start_time": _to_iso(span.start_time),
                    "end_time": _to_iso(span.end_time),
                    **attributes,
                }
            )

        if not records:
            return SpanExportResult.SUCCESS

        with self._lock:
            with self.output_path.open("a", encoding="utf-8") as output_file:
                for record in records:
                    output_file.write(json.dumps(record, ensure_ascii=True) + "\n")

        return SpanExportResult.SUCCESS

    def shutdown(self) -> None:
        return None


def configure_telemetry(
    export_dir: str | Path = "telemetry_data", service_name: str = SERVICE_NAME
) -> Path:
    global _CONFIGURED, _PROVIDER, _EXPORT_PATH

    export_path = Path(export_dir).expanduser().resolve() / "search_runs.jsonl"

    with _LOCK:
        if _CONFIGURED:
            return _EXPORT_PATH if _EXPORT_PATH is not None else export_path

        provider = TracerProvider(
            resource=Resource.create(
                {
                    "service.name": service_name,
                    "service.version": "1.0.0",
                    "deployment.environment": "local",
                }
            )
        )
        provider.add_span_processor(
            SimpleSpanProcessor(JsonLinesSpanExporter(export_path))
        )
        trace.set_tracer_provider(provider)

        _PROVIDER = provider
        _EXPORT_PATH = export_path
        _CONFIGURED = True

    atexit.register(shutdown_telemetry)
    return export_path


def get_tracer():
    return _TRACER


def get_export_path() -> Path:
    if _EXPORT_PATH is None:
        return Path("telemetry_data").resolve() / "search_runs.jsonl"
    return _EXPORT_PATH


def shutdown_telemetry() -> None:
    global _CONFIGURED, _PROVIDER

    with _LOCK:
        if not _CONFIGURED or _PROVIDER is None:
            return

        _PROVIDER.shutdown()
        _PROVIDER = None
        _CONFIGURED = False
