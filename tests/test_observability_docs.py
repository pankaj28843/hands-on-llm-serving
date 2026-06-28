from pathlib import Path


def test_observability_docs_describe_phoenix_and_prompt_safety() -> None:
    docs_path = Path("docs/observability.md")

    assert docs_path.exists()
    text = docs_path.read_text(encoding="utf-8")

    for required in (
        "OpenTelemetry",
        "Phoenix",
        "MAC_LLM_OPS_OTEL_ENABLED",
        "MAC_LLM_OPS_OTEL_EXPORTER_OTLP_TRACES_ENDPOINT",
        "http://phoenix:6006/v1/traces",
        "gen_ai.usage.input_tokens",
        "gen_ai.usage.output_tokens",
        "db.transaction.outcome",
        "does not capture prompts",
        "Do not claim the Phoenix slice complete",
    ):
        assert required in text
