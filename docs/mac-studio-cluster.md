# Mac Studio Cluster

Mac Studio cluster support is the next platform goal, not a completed claim.
The current MacBook baseline proves the local Apple Silicon path; it does not
prove Mac Studio cluster capacity, failover, or multi-user behavior.

## Required Validation

Before this repo can claim Mac Studio cluster readiness, a real cluster run
must cover:

- Node count, chip generation, unified memory, macOS version, and Apple GPU
  availability for each node.
- Network topology, service discovery, routing policy, health checks, retry
  behavior, and rollback behavior.
- Same model id, model revision, quantization, and benchmark workload policy
  across nodes unless a test explicitly varies one factor.
- Per-node API/backend logs, Phoenix/OpenTelemetry spans, benchmark rows,
  backend metrics, Metal memory/cache metrics, and publish-safety scans.
- A routed-cluster endpoint validation that separates single-node latency,
  aggregate throughput, failover behavior, and Open WebUI UX behavior.

## Current Contract

The current code-backed preparation lives in `mac_llm_ops_lab.cluster`. It is
side-effect-free so routing logic can be tested before real Mac Studio hardware
exists.

`route_to_model` is conservative. It only routes to registered nodes that are
both healthy and ready and that explicitly list the requested model. Among
eligible nodes, it selects `least_queue_depth`. If no registered node can serve
the model, it returns the local rollback decision with
`no_healthy_registered_node` and `fallback: true`.

Every local binding must stay in the `20000-50000` range. A single-node local
report is useful setup validation, but it is not real multi-node proof.

## Planned Shape

The likely first cluster shape is a private Mac Studio LAN where each node runs
a native `vllm-mlx` backend and a local health endpoint, while a router exposes
one OpenAI-compatible API surface. PostgreSQL stores inventory and benchmark
metadata. Phoenix receives spans from the router and nodes.
