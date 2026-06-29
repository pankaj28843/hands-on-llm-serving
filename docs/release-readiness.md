# Release Readiness

This page is the public-repo handoff checklist. It keeps the repository honest
about what is complete, what is still pending, and what must never be
published.

## One Command

Run the local validation entrypoint:

```bash
make validate
```

`make validate` runs:

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
docker compose -f compose.yaml config --format json
uv run mkdocs build --strict
uv run python scripts/validate-public-release.py --output artifacts/runtime/release-readiness/public-release-check.json
```

The public release scan writes `public-release-check/v1` JSON to:

```text
artifacts/runtime/release-readiness/public-release-check.json
```

That path is ignored by git and should be kept as local proof, not published as
source.

## Claim Checklist

| Claim | Validation |
| --- | --- |
| Fake-backend API works in tests and Docker Compose. | `uv run pytest`; Compose config validation. |
| PostgreSQL persistence is code-backed. | `tests/test_persistence_*`; Alembic migration tests. |
| Phoenix/OpenTelemetry is prompt-safe by default. | `tests/test_observability.py`; `docs/operations.md`. |
| Open WebUI reaches the API. | `tests/test_open_webui_integration.py`; `docs/operations.md`. |
| `vllm-mlx` can run the approved small MLX model locally. | `docs/development.md`; model catalog gate. |
| MacBook benchmark baseline exists. | Backend contract tests and local benchmark artifacts. |
| Mac Studio cluster readiness is not claimed. | `docs/mac-studio-cluster.md`; real multi-node proof remains pending. |

## Do Not Publish

Do not publish or commit:

- `model-cache/`
- `artifacts/runtime/`
- `secrets/`
- `traces/`
- `data/`
- raw benchmark payloads
- database files
- local logs
- private document exports from local library or note-management tools
- local source-material trees outside this repository
- real provider keys, Hugging Face tokens, cookies, JWTs, or SSH keys

The public repo should stand on its own. Do not brand the project after
external source material; do not vendor third-party source text, purchased
source files, third-party example code, model weights, local traces, or
machine-local paths without a reviewed license basis.

## Third-Party Content Guard

For this public repo and GitHub Pages site, the rule is: links and short
paraphrase are allowed; no source text, no images, no screenshots, no tables,
no copied copyright notice, no restricted reuse notice, no purchased source
export, and no copied third-party example code unless a future change records a
reviewed license basis.

## Current Honesty Boundary

This repo is production-style and validation-driven, not production-certified.
MacBook proof, fake-backend Docker proof, Open WebUI proof, Phoenix tracing,
and benchmark structure are complete for local learning. Mac Studio cluster
capacity, failover, and multi-user performance remain pending until real
cluster validation exists.
