# Vision

The goal is an almost production-ready LLM serving lab for macOS and Apple
Silicon. The project should let someone clone the repo, run the fake backend,
inspect the real-backend path, study the evidence, and build intuition about
the tradeoffs behind production serving.

The project now stands on its own as a Mac-first lab. External references are
treated as reference-only background; the implementation, naming, docs, and
validation path are specific to this repository's Apple Silicon operating model.

## What This Lab Should Teach

- How a model-facing API is separated from backend execution.
- Why prefill, decode, KV cache, batching, and streaming affect latency and
  throughput.
- How Docker services, PostgreSQL, Phoenix, OpenTelemetry, and Open WebUI fit
  around an LLM API.
- How benchmark traffic and traces become evidence, not anecdotes.
- Why a MacBook baseline is useful but does not prove Mac Studio cluster
  capacity.

## Platform Boundary

The target platform is macOS and Apple Silicon. The first real backend is
`vllm-mlx` with `mlx-community/Qwen3-0.6B-8bit` because it is small enough for
local smoke tests and uses the Apple GPU path. Future cluster work targets Mac
Studio nodes.
