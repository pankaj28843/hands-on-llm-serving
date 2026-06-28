# Mac Studio Cluster

Mac Studio cluster support is the next platform goal, not a completed claim.
This page defines what must exist before the repo can say it supports cluster
operation.

## Required Evidence

- Node count, chip generation, unified memory, macOS version, thermal or power
  mode, and Apple GPU availability for each node.
- Network topology, service discovery, routing policy, health checks, retry
  behavior, and rollback behavior.
- Same model id, model revision, quantization, and benchmark workload policy
  across nodes unless a test explicitly varies one factor.
- Per-node API/backend logs, Phoenix/OpenTelemetry spans, benchmark rows,
  backend metrics, Metal memory/cache metrics, and publish-safety scans.
- A routed-cluster endpoint proof that separates single-node latency,
  aggregate throughput, failover behavior, and Open WebUI UX behavior.

## Current Status

The MacBook Pro baseline proves this repo can run an approved small MLX model,
serve through the native backend and project API on high local ports, emit
Phoenix traces, and produce a structurally valid benchmark bundle. It does not
prove Mac Studio cluster capacity.

## Planned Shape

The likely first cluster shape is a private Mac Studio LAN where each node runs
a native `vllm-mlx` backend and a local health endpoint, while a router exposes
one OpenAI-compatible API surface. PostgreSQL stores inventory and benchmark
metadata. Phoenix receives spans from the router and nodes.
