from pathlib import Path


def test_observability_docs_describe_phoenix_and_prompt_safety() -> None:
    docs_path = Path("docs/operations.md")

    assert docs_path.exists()
    text = docs_path.read_text(encoding="utf-8")
    text_flat = " ".join(text.split())

    for required in (
        "OpenTelemetry",
        "Phoenix",
        "MAC_LLM_OPS_OTEL_ENABLED",
        "MAC_LLM_OPS_OTEL_EXPORTER_OTLP_TRACES_ENDPOINT",
        "http://127.0.0.1:26006/v1/traces",
        "http://phoenix:6006/v1/traces",
        "does not capture prompts",
        "publish only sanitized summaries",
    ):
        assert required in text_flat

    assert "artifacts/runtime/2026-" not in text
