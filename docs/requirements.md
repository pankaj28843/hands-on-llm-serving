# Requirements

## Functional Requirements

- Provide an OpenAI-compatible FastAPI API with `/live`, `/ready`,
  `/v1/models`, `/v1/chat/completions`, streaming chat, and metrics snapshots.
- Support a CPU-safe fake backend for tests and Docker smoke runs.
- Support a gated native Apple Silicon backend path through `vllm-mlx`.
- Store serving metadata, model catalog entries, node inventory, benchmark
  summaries, and artifact pointers through PostgreSQL-backed persistence.
- Emit prompt-safe OpenTelemetry spans to Phoenix for HTTP, scheduler, backend,
  streaming, cancellation, and database transaction paths.
- Run Open WebUI locally against the API through the OpenAI-compatible surface.
- Record benchmark evidence with workload metadata, high local ports, model
  revision, hardware labels, traces, raw rows, summaries, and publish-safety
  scans.
- Serve project learning docs through MkDocs.

## Operational Requirements

- All local host bindings must use ports in the `20000-50000` range.
- Model downloads require an explicit approval flag and must write under
  ignored `model-cache/`.
- Runtime evidence must write under ignored `artifacts/runtime/`.
- Local secrets must stay under ignored `secrets/` and never be committed.
- Real-model tests on this MacBook must pass the memory preflight before start.

## Non-Goals

- No Linux/NVIDIA production deployment is claimed by this repo.
- No Kubernetes, Triton, or cloud deployment is required for the current scope.
- No Mac Studio cluster throughput, latency, failover, queue-depth, or
  multi-user UX claim is supported until Mac Studio evidence exists.
