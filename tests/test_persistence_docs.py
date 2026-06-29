from pathlib import Path


def test_public_docs_keep_persistence_claim_source_concise() -> None:
    docs_path = Path("docs/release-readiness.md")

    assert docs_path.exists()
    text = docs_path.read_text(encoding="utf-8")

    for required in (
        "Alembic",
        "tests/test_persistence_*",
        "PostgreSQL",
    ):
        assert required in text

    assert "artifacts/runtime/2026-" not in text
