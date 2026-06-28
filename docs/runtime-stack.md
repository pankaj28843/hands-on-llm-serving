# Runtime Stack

This page separates static validation from runtime side effects.

## What Exists Now

The repo currently has:

- a fake-backend FastAPI API service
- a static runtime topology in `mac_llm_ops_lab.runtime_stack`
- `compose.yaml` wiring for PostgreSQL, Phoenix, Open WebUI, and the API
- a minimal API `Dockerfile`
- tests that validate the Compose file with `docker compose config`
- one local E2E proof run of the Docker-built fake-backend API stack

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

## Working Local E2E Proof

The first working local app/API proof used ignored local runtime inputs and
artifacts:

```bash
mkdir -p secrets artifacts/runtime/2026-06-28T145945+0200-e2e
# secrets/postgres_password.txt contains the local placeholder used by compose.
PHOENIX_HOST_PORT=16006 docker compose up -d --build
```

`PHOENIX_HOST_PORT=16006` was needed on this MacBook because another local
Docker project already owned `localhost:6006`. Without that collision, the
default Phoenix URL remains `http://localhost:6006`.

The saved evidence bundle is under:

```text
artifacts/runtime/2026-06-28T145945+0200-e2e/
```

The proof includes:

- Docker API image build with `uv sync --frozen --no-dev`
- Postgres container health via `pg_isready`
- API `GET /live`
- API `GET /ready`
- API `GET /v1/models`
- API non-streaming `POST /v1/chat/completions`
- API streaming `POST /v1/chat/completions`
- API `GET /metrics/snapshot`
- Phoenix HTTP `200 OK` on `http://localhost:16006/`
- Open WebUI healthy container and root HTML on `http://localhost:3000/`
- Open WebUI default embedding asset download into its Docker volume

Open WebUI root reachability is proven; its backend API probes returned `401`
for unauthenticated direct curl calls. A browser workflow or authenticated API
contract is still needed before claiming Open WebUI chat workflow integration.

## Still Not Complete

The local E2E proof is intentionally narrower than production readiness. These
claims are not complete yet:

- production secret management beyond the ignored local placeholder file
- PostgreSQL migration and sample persistence proof
- Phoenix OpenTelemetry trace export proof
- Open WebUI model listing and chat smoke proof through its UI/API workflow
- model-cache policy under ignored `model-cache/`
- runtime artifacts under ignored `artifacts/runtime/`
- Apple Silicon backend startup
- real model download and inference

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
