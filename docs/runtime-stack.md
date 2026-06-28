# Runtime Stack

This page separates static validation from runtime side effects.

## What Exists Now

The repo currently has:

- a fake-backend FastAPI API service
- a static runtime topology in `mac_llm_ops_lab.runtime_stack`
- `compose.yaml` wiring for PostgreSQL, Phoenix, Open WebUI, and the API
- a minimal API `Dockerfile`
- tests that validate the Compose file with `docker compose config`

The Apple Silicon backend is intentionally native and gated. It is not a
Compose service yet. The first candidate is `vllm-mlx`, but it must pass model
download, memory preflight, install/import/version, streaming, telemetry, and
benchmark gates before it can be treated as a runtime backend.

## Safe Static Checks

These commands do not start containers, create volumes, use real secrets, or
download models:

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
docker compose -f compose.yaml config --format json
```

## Do Not Run Yet

Do not run `docker compose up` yet as a readiness claim. The Compose file has
passed static validation only. A real service run still needs a scoped evidence
plan for:

- local `secrets/` files, especially `secrets/postgres_password.txt`
- container logs and cleanup
- PostgreSQL migration and sample persistence proof
- Phoenix trace export proof
- Open WebUI model listing and chat smoke proof
- model-cache policy under ignored `model-cache/`
- runtime artifacts under ignored `artifacts/runtime/`

`secrets/`, `model-cache/`, traces, logs, raw benchmarks, database files, and
runtime artifacts must stay out of git.

## Current Service Intent

PostgreSQL stores future model catalog, run metadata, benchmark, and node
inventory records.

Phoenix receives OpenTelemetry traces for HTTP, scheduling, backend calls,
streaming, database writes, and benchmark runs.

Open WebUI connects to the local OpenAI-compatible API. In Compose, it uses
`http://api:8000/v1`; when running Open WebUI outside Compose against a host
API process, use the appropriate host URL.

The API service is still safe to import and test without Docker, PostgreSQL,
Phoenix, Open WebUI, or model downloads.
