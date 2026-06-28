.PHONY: validate

validate:
	uv run pytest
	uv run ruff check .
	uv run ruff format --check .
	docker compose -f compose.yaml config --format json | python3 -m json.tool >/dev/null
	uv run mkdocs build --strict
	uv run python scripts/validate-public-release.py --output artifacts/runtime/release-readiness/public-release-check.json
