# Mac LLM Ops Lab

This repository is a Mac-first learning lab for production LLM serving. It is
grounded in the external source book
[Mac LLM Ops Lab](https://www.external_source.com/library/view/mac-llm-ops-lab/9798341621480/)
and its
[reference repository](https://github.com/pankaj28843/mac-llm-ops-lab/), but this
repo is a separate implementation focused on macOS, Apple Silicon, and future
Mac Studio clusters.

## Learning Path

1. Read [Vision](vision.md) to understand why the project exists.
2. Read [Requirements](requirements.md) for current scope and non-goals.
3. Read [Design](design.md) for the architecture and boundary map.
4. Follow [Development](development.md) to run tests, linting, docs, and static
   Compose validation.
5. Follow [Operations](operations.md) to run the local Docker stack on high
   local ports.
6. Use [Backends](backends.md), [Observability](observability.md), and
   [Benchmarks](benchmarks.md) to connect API calls to model runtime behavior,
   Phoenix traces, and benchmark evidence.
7. Read [Mac Studio Cluster](mac-studio-cluster.md) before making any cluster
   claim.
8. Run [Release Readiness](release-readiness.md) before publishing or handing
   the repo to someone else.

## Clone And Run

```bash
uv sync
uv run pytest
uv run ruff check .
uv run ruff format --check .
docker compose -f compose.yaml config --format json
uv run mkdocs build --strict
uv run mkdocs serve -a 127.0.0.1:28080
```

The default local service ports are intentionally high: API
`http://localhost:28000`, Open WebUI `http://localhost:23000`, Phoenix
`http://localhost:26006`, PostgreSQL `localhost:25432`, OTLP gRPC
`localhost:24317`, Phoenix Prometheus `http://localhost:29090`, native
`vllm-mlx` `http://127.0.0.1:28100`, and native model-backed API
`http://127.0.0.1:28020`.
