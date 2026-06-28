#!/usr/bin/env bash
set -euo pipefail

URL="${VLLM_MLX_URL:-http://127.0.0.1:28100}"
MODEL_ID="${MODEL_ID:-mlx-community/Qwen3-0.6B-8bit}"
RUN_ID="${RUN_ID:-$(date +%Y-%m-%dT%H%M%S%z)-vllm-mlx-contract}"
ARTIFACT_DIR="${ARTIFACT_DIR:-artifacts/runtime/$RUN_ID}"
PROMPTS="${VLLM_MLX_BENCH_PROMPTS:-short}"
CONCURRENCY="${VLLM_MLX_BENCH_CONCURRENCY:-1}"
MAX_TOKENS="${VLLM_MLX_BENCH_MAX_TOKENS:-4}"
REPETITIONS="${VLLM_MLX_BENCH_REPETITIONS:-1}"
WARMUP="${VLLM_MLX_BENCH_WARMUP:-0}"
VALIDATE="${VLLM_MLX_BENCH_VALIDATE:-false}"

mkdir -p "$ARTIFACT_DIR"

curl -fsS "$URL/metrics" > "$ARTIFACT_DIR/backend-metrics.prom"

uv tool run vllm-mlx bench-serve \
  --url "$URL" \
  --model "$MODEL_ID" \
  --prompts "$PROMPTS" \
  --concurrency "$CONCURRENCY" \
  --max-tokens "$MAX_TOKENS" \
  --repetitions "$REPETITIONS" \
  --warmup "$WARMUP" \
  --validate "$VALIDATE" \
  --format json \
  --output "$ARTIFACT_DIR/bench-smoke.json" \
  --tag "$RUN_ID"

uv run python -m mac_llm_ops_lab.backend_contracts \
  --metrics-path "$ARTIFACT_DIR/backend-metrics.prom" \
  --benchmark-path "$ARTIFACT_DIR/bench-smoke.json" \
  --report-path "$ARTIFACT_DIR/backend-contract-report.json"

printf '%s\n' "$ARTIFACT_DIR/backend-contract-report.json"
