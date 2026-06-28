from pathlib import Path


def test_runtime_stack_docs_define_static_and_runtime_boundaries() -> None:
    docs_path = Path("docs/runtime-stack.md")

    assert docs_path.exists()
    text = docs_path.read_text(encoding="utf-8")

    for required in (
        "docker compose config",
        "docker compose up",
        "Do not run",
        "secrets/",
        "model-cache/",
        "PostgreSQL",
        "Phoenix",
        "Open WebUI",
        "Apple Silicon backend",
    ):
        assert required in text
