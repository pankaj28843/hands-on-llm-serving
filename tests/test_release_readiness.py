import json
import subprocess
import sys
from pathlib import Path

from mac_llm_ops_lab.release_readiness import (
    scan_public_release_files,
    write_public_release_report,
)


def test_public_release_scan_passes_for_placeholder_only_docs() -> None:
    report = scan_public_release_files(
        {
            "docs/open-webui.md": "OPENAI_API_KEYS=local-dev-placeholder\n",
            "compose.yaml": "OPENAI_API_KEYS: local-dev-placeholder\n",
            "docs/index.md": "http://localhost:28000\n",
        },
        git_sha="abc1234",
    )

    assert report["passed"] is True
    assert report["findings"] == []
    assert report["schema_version"] == "public-release-check/v1"
    assert report["git_sha"] == "abc1234"


def test_public_release_scan_rejects_forbidden_paths_and_secret_text() -> None:
    private_export = (
        "local export: "
        + ("/" + "Users/example/")
        + ("Calibre" + " Library")
        + "/book.epub"
    )
    secret = "OPENAI_API_KEY=" + "sk-" + "1234567890abcdefghijklmnop"
    report = scan_public_release_files(
        {
            "artifacts/runtime/run/raw.json": "{}",
            "docs/private.md": private_export,
            "src/config.py": secret,
        },
        git_sha="abc1234",
    )

    assert report["passed"] is False
    assert {finding["kind"] for finding in report["findings"]} == {
        "forbidden_tracked_path",
        "private_machine_path",
        "secret_pattern",
    }


def test_public_release_report_writer_requires_ignored_runtime_output(tmp_path) -> None:
    report = scan_public_release_files({"README.md": "clean"}, git_sha="abc1234")

    output_path = write_public_release_report(
        report,
        output_root=tmp_path,
        output_path=Path("artifacts/runtime/release/public-release-check.json"),
    )

    assert output_path.read_text(encoding="utf-8").endswith("\n")
    assert json.loads(output_path.read_text(encoding="utf-8")) == report


def test_release_docs_makefile_and_mkdocs_nav_define_validation_path() -> None:
    release_docs = Path("docs/release-readiness.md").read_text(encoding="utf-8")
    makefile = Path("Makefile").read_text(encoding="utf-8")
    mkdocs_config = Path("mkdocs.yml").read_text(encoding="utf-8")

    for required in (
        "make validate",
        "uv run pytest",
        "uv run ruff check .",
        "uv run ruff format --check .",
        "docker compose -f compose.yaml config --format json",
        "uv run mkdocs build --strict",
        "scripts/validate-public-release.py",
        "public-release-check/v1",
        "artifacts/runtime/release-readiness/public-release-check.json",
        "Do not publish",
        "model-cache/",
        "secrets/",
        "traces/",
        "private EPUB exports",
        "local converted book trees",
    ):
        assert required in release_docs

    assert "validate:" in makefile
    assert "scripts/validate-public-release.py" in makefile
    assert "Release Readiness: release-readiness.md" in mkdocs_config


def test_public_release_cli_writes_clean_report(tmp_path) -> None:
    output = tmp_path / "artifacts/runtime/release/public-release-check.json"
    result = subprocess.run(
        [
            sys.executable,
            "scripts/validate-public-release.py",
            "--output",
            str(output),
        ],
        capture_output=True,
        check=False,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    report = json.loads(output.read_text(encoding="utf-8"))
    assert report["schema_version"] == "public-release-check/v1"
    assert report["passed"] is True
