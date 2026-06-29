# Benchmarks

Benchmarking is evidence collection, not decoration. The lab emphasizes
hardware inspection, representative traffic, explicit metrics, service setup,
repeated runs, and tradeoff analysis. Those rules are encoded as workload
policy and artifact manifests.

## Required Signals

- Workload name and prompt shape.
- Model id, model revision, quantization, backend, command, and git SHA.
- High local ports and hardware labels.
- TTFT, TPOT or ITL, end-to-end latency, throughput, token counts, error rate,
  Metal memory, cache metrics, and Phoenix spans.
- Raw benchmark rows, summarized JSON, backend metrics, logs, and a
  publish-safety scan.

See [Backend Contracts](backend-contracts.md) for the executable parser and
manifest rules.

## Current Boundary

The current MacBook baseline is local development evidence only. Do not
extrapolate it into Mac Studio cluster throughput, cluster latency, capacity
planning, failover behavior, queue depth targets, or Open WebUI multi-user UX
claims.

Mac Studio claims require Mac Studio hardware evidence with node inventory,
network topology, routing policy, identical model revision, identical benchmark
workload policy, per-node spans, routed-cluster spans, and publish-safe
artifacts.
