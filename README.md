# Mac LLM Ops Lab

Mac-first LLM serving lab for learning production serving patterns on Apple
Silicon. The first implementation target is a FastAPI service with fake-backend
tests, then observable local backend adapters and Mac Studio cluster proof.

This repository does not vendor the book export, local model caches, traces, or
private benchmark payloads.

## Development

```bash
uv run pytest
```
