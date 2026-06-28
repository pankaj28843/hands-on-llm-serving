# Agent Map

This repo is the target implementation for a macOS/Apple Silicon LLM serving
lab. Keep this file short; use the served docs for detail.

## Start Here

- `docs/development.md`: local setup, validation, and high-port run commands.
- `docs/operations.md`: Docker/Phoenix/PostgreSQL/Open WebUI runbook.
- `docs/vision.md`: project intent and learning goals.
- `docs/requirements.md`: current requirements and non-goals.
- `docs/design.md`: architecture and boundary map.

## Hard Rules

- Use local host ports in the `20000-50000` range for all local bindings.
- Do not commit `model-cache/`, `artifacts/runtime/`, `secrets/`, database
  files, logs, traces, or raw benchmark payloads.
- Treat the reference repository as reference-only; do not copy its code into
  this repo without an explicit, reviewed change.
- Prefer tests and saved runtime evidence over chat memory.
