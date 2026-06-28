#!/usr/bin/env bash
set -euo pipefail

MODEL_ID="${MODEL_ID:-mlx-community/Qwen3-0.6B-8bit}"
SERVED_MODEL_NAME="${SERVED_MODEL_NAME:-$MODEL_ID}"
HOST="${VLLM_MLX_HOST:-127.0.0.1}"
PORT="${VLLM_MLX_PORT:-8100}"
HF_HOME="${HF_HOME:-$PWD/model-cache/huggingface}"
MAC_LLM_OPS_MODEL_DOWNLOAD_APPROVED="${MAC_LLM_OPS_MODEL_DOWNLOAD_APPROVED:-false}"
MODEL_DOWNLOAD_GATE_REPORT="${MODEL_DOWNLOAD_GATE_REPORT:-artifacts/runtime/vllm-mlx-model-download-gate.json}"

export HF_HOME
export MAC_LLM_OPS_MODEL_DOWNLOAD_APPROVED

uv run python -m mac_llm_ops_lab.model_catalog "$MODEL_ID" \
  --report-path "$MODEL_DOWNLOAD_GATE_REPORT"

uv tool run vllm-mlx serve "$MODEL_ID" \
  --served-model-name "$SERVED_MODEL_NAME" \
  --host "$HOST" \
  --port "$PORT" \
  --max-tokens "${VLLM_MLX_MAX_TOKENS:-64}" \
  --max-request-tokens "${VLLM_MLX_MAX_REQUEST_TOKENS:-128}" \
  --cache-memory-mb "${VLLM_MLX_CACHE_MEMORY_MB:-512}" \
  --enable-metrics
