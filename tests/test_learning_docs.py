from pathlib import Path


def _read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def test_root_docs_are_short_routers_to_served_docs() -> None:
    required_root_docs = {
        "AGENTS.md": (
            "docs/development.md",
            "docs/operations.md",
            "docs/vision.md",
            "docs/requirements.md",
            "docs/design.md",
        ),
        "vision.md": ("docs/vision.md",),
        "requirements.md": ("docs/requirements.md",),
        "design.md": ("docs/design.md",),
    }

    for path, required_links in required_root_docs.items():
        text = _read(path)
        assert len(text.splitlines()) <= 80
        for required_link in required_links:
            assert required_link in text

    agents_text = _read("AGENTS.md")
    assert "/" + "Users/" not in agents_text
    assert "model-cache/" in agents_text
    assert "artifacts/runtime/" in agents_text
    assert "20000-50000" in agents_text


def test_mkdocs_config_serves_learning_docs_with_explicit_nav() -> None:
    config = _read("mkdocs.yml")

    for required in (
        "site_name: Mac LLM Ops Lab",
        "docs_dir: docs",
        "repo_url: https://github.com/pankaj28843/mac-llm-ops-lab",
        "theme:",
        "name: mkdocs",
        "nav:",
        "Home: index.md",
        "Vision: vision.md",
        "Requirements: requirements.md",
        "Design: design.md",
        "Development: development.md",
        "Operations: operations.md",
        "Backends: backends.md",
        "Benchmarks: benchmarks.md",
        "Mac Studio Cluster: mac-studio-cluster.md",
        "Runtime Stack: runtime-stack.md",
        "Observability: observability.md",
        "Open WebUI: open-webui.md",
    ):
        assert required in config


def test_learning_docs_cover_clone_and_run_path_without_private_paths() -> None:
    docs = {
        path.name: path.read_text(encoding="utf-8")
        for path in Path("docs").glob("*.md")
    }

    for required_page in (
        "index.md",
        "vision.md",
        "requirements.md",
        "design.md",
        "development.md",
        "operations.md",
        "backends.md",
        "benchmarks.md",
        "mac-studio-cluster.md",
    ):
        assert required_page in docs

    combined = "\n".join(docs.values())
    for required in (
        "uv sync",
        "uv run pytest",
        "uv run ruff check .",
        "uv run ruff format --check .",
        "docker compose -f compose.yaml config --format json",
        "uv run mkdocs build --strict",
        "http://localhost:28000",
        "http://localhost:23000",
        "http://localhost:26006",
        "PostgreSQL",
        "Phoenix",
        "OpenTelemetry",
        "Open WebUI",
        "vllm-mlx",
        "mlx-community/Qwen3-0.6B-8bit",
        "Mac Studio",
        "Do not extrapolate",
        "independent Mac-first learning lab",
        "reference-only background",
        "External references",
    ):
        assert required in combined

    public_learning_docs = "\n".join(
        text for name, text in docs.items() if name != "release-readiness.md"
    )
    forbidden_fragments = (
        "/" + "Users/",
        "Calibre" + " Library",
        "." + "books/",
        "secrets/postgres_password.txt contains",
        "HF_TOKEN",
        "OPENAI_API_KEY=",
    )
    for forbidden in forbidden_fragments:
        assert forbidden not in public_learning_docs

    for stale_branding in (
        "Hands-" + "On LLM Serving",
        "hands-" + "on-llm-serving",
        "hands_" + "on_llm_serving",
        "Mac LLM Ops Lab" + " and Optimization",
        "https://www.external_source.com/library/" + "view/",
        "https://github.com/pankaj28843/" + "mac-llm-ops-lab",
    ):
        assert stale_branding not in public_learning_docs


def test_readme_points_to_current_native_openwebui_answer_proof() -> None:
    readme = _read("README.md")

    for required in (
        "VLLM_MLX_MAX_TOKENS=512",
        "VLLM_MLX_MAX_REQUEST_TOKENS=1024",
        "VLLM_MLX_REASONING_PARSER=qwen3",
        "VLLM_MLX_DEFAULT_CHAT_TEMPLATE_KWARGS='{\"enable_thinking\": false}'",
        "artifacts/runtime/2026-06-28T195945+0200-open-webui-visible-answer-no-think/",
        "visible assistant answer",
    ):
        assert required in readme

    assert "limited visible answer text" not in readme


def test_readme_honesty_boundary_matches_current_release_status() -> None:
    readme = " ".join(_read("README.md").split())

    for stale in (
        "fuller benchmark qualification, MkDocs, cluster routing, and "
        "release/no-leak checks are still pending",
        "MkDocs, cluster routing, and release/no-leak checks are still pending",
        "release/no-leak checks are still pending",
    ):
        assert stale not in readme

    for required in (
        "MacBook proof, fake-backend Docker proof, Open WebUI proof, "
        "Phoenix tracing, MkDocs, release/no-leak checks, and benchmark "
        "structure are complete for local learning",
        "Mac Studio cluster capacity, failover, and multi-user performance "
        "remain pending until real cluster evidence exists",
        "test-double cluster routing contract is code-backed",
        "real multi-node proof",
    ):
        assert required in readme


def test_readme_points_to_published_docs_and_pages_workflow() -> None:
    readme = _read("README.md")

    for required in (
        "https://pankaj28843.github.io/mac-llm-ops-lab/",
        ".github/workflows/pages.yml",
        "Publish Docs",
        "uv run mkdocs build --strict",
        "make validate",
    ):
        assert required in readme


def test_mkdocs_is_declared_as_dev_dependency() -> None:
    pyproject = _read("pyproject.toml")

    assert '"mkdocs>=' in pyproject
