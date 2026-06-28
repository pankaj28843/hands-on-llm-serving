# Design

## Architecture

The project keeps delivery, policy, backend execution, persistence, and
observability separated.

- FastAPI owns the HTTP/OpenAI-compatible surface.
- Application code owns request shaping, backend selection, streaming behavior,
  metrics, and errors.
- Backend adapters hide execution details behind a small generation interface.
- Persistence uses repository and unit-of-work ports, with SQLAlchemy as an
  adapter.
- Observability is app-local and explicit: importing the ASGI app does not start
  exporters, connect to Phoenix, or download models.
- Runtime artifacts are structured evidence bundles, not source files.

## Backend Boundary

The fake backend is the default for tests and Compose. The native backend is a
host process reached through the OpenAI-compatible adapter. That keeps Apple
GPU execution outside the API container while the Docker stack still provides
PostgreSQL, Phoenix, Open WebUI, and the API service.

## Evidence Boundary

Code changes need tests. Runtime claims need saved evidence. Performance claims
need benchmark workload policy, raw rows, summaries, backend metrics, Phoenix
spans, and publish-safety scans. A MacBook baseline can guide the plan, but it
cannot prove Mac Studio cluster behavior.

## Book Grounding

The design follows the book's progression from serving foundations to system
design, best practices, optimization, frameworks, and applied benchmarking. The
reference repository remains reference-only.
