from __future__ import annotations

from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from dataclasses import dataclass

from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import ReadableSpan, TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, SpanExporter
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
from opentelemetry.trace import Span, SpanKind, Status, StatusCode, Tracer

from mac_llm_ops_lab.config import Settings

DEFAULT_OTLP_HTTP_TRACES_ENDPOINT = "http://localhost:4318/v1/traces"
INSTRUMENTATION_NAME = "mac_llm_ops_lab"
INSTRUMENTATION_VERSION = "0.1.0"
MAX_ATTRIBUTE_STRING_LENGTH = 256

AttributeValue = str | bool | int | float | tuple[str, ...]


class InMemorySpanRecorder(InMemorySpanExporter):
    def get_finished_spans(self) -> list[ReadableSpan]:
        return list(super().get_finished_spans())


@dataclass(frozen=True)
class NoopSpan:
    def set_attribute(self, key: str, value: object) -> None:
        return None

    def set_status(self, status: Status, description: str | None = None) -> None:
        return None


@dataclass
class Observability:
    enabled: bool
    endpoint: str | None
    resource_attributes: Mapping[str, str]
    tracer: Tracer | None = None
    provider: TracerProvider | None = None

    @contextmanager
    def start_span(
        self,
        name: str,
        *,
        attributes: Mapping[str, object] | None = None,
        kind: SpanKind = SpanKind.INTERNAL,
    ) -> Iterator[Span | NoopSpan]:
        if not self.enabled or self.tracer is None:
            yield NoopSpan()
            return

        with self.tracer.start_as_current_span(
            name,
            kind=kind,
            attributes=sanitize_attributes(attributes or {}),
            record_exception=False,
            set_status_on_exception=False,
        ) as span:
            yield span

    def force_flush(self) -> None:
        if self.provider is not None:
            self.provider.force_flush()

    def shutdown(self) -> None:
        if self.provider is not None:
            self.provider.shutdown()


def configure_observability(
    settings: Settings,
    *,
    span_exporter: SpanExporter | None = None,
) -> Observability:
    if not settings.otel_enabled:
        return Observability(
            enabled=False,
            endpoint=None,
            resource_attributes=_resource_attributes(settings),
        )

    endpoint = (
        settings.otel_exporter_otlp_traces_endpoint or DEFAULT_OTLP_HTTP_TRACES_ENDPOINT
    )
    provider = TracerProvider(resource=Resource.create(_resource_attributes(settings)))
    exporter = span_exporter or OTLPSpanExporter(
        endpoint=endpoint,
        timeout=settings.otel_export_timeout_seconds,
    )
    provider.add_span_processor(SimpleSpanProcessor(exporter))

    return Observability(
        enabled=True,
        endpoint=endpoint,
        resource_attributes=_resource_attributes(settings),
        tracer=provider.get_tracer(INSTRUMENTATION_NAME, INSTRUMENTATION_VERSION),
        provider=provider,
    )


def mark_span_error(span: Span | NoopSpan, error_type: str) -> None:
    span.set_attribute("error.type", error_type)
    span.set_status(Status(StatusCode.ERROR))


def safe_token_count(text: str) -> int:
    return max(len(text.split()), 0)


def sanitize_attributes(attributes: Mapping[str, object]) -> dict[str, AttributeValue]:
    safe: dict[str, AttributeValue] = {}
    for key, value in attributes.items():
        if value is None:
            continue
        safe_key = str(key)
        safe_value = _sanitize_attribute_value(value)
        if safe_value is not None:
            safe[safe_key] = safe_value
    return safe


def _resource_attributes(settings: Settings) -> dict[str, str]:
    return {
        "service.name": settings.service_name,
        "service.namespace": "mac-llm-ops-lab",
        "phoenix.project.name": settings.phoenix_project_name,
    }


def _sanitize_attribute_value(value: object) -> AttributeValue | None:
    if isinstance(value, bool | int | float):
        return value
    if isinstance(value, str):
        return value[:MAX_ATTRIBUTE_STRING_LENGTH]
    if isinstance(value, list | tuple):
        strings = tuple(str(item)[:MAX_ATTRIBUTE_STRING_LENGTH] for item in value)
        return strings
    return None
