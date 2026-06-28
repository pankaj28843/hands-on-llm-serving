# Open WebUI

Open WebUI is the local operator/user front end for this project. It connects
to the FastAPI service through the OpenAI-compatible API surface.

## Source Surface

Version/source-surface: local `docsearch` tenant `openwebui` from
`https://docs.openwebui.com`, fetched pages `OpenAI-Compatible / Open WebUI`,
`Environment Variable Configuration / Open WebUI`, and
`API Endpoints / Open WebUI`; local Open WebUI image version is `main`, so
runtime smoke evidence is required before claiming workflow compatibility.

The relevant Open WebUI contract is protocol-oriented:

- `GET /v1/models` is recommended for model discovery and UI model selection.
- `POST /v1/chat/completions` is required for chat.
- Chat requests can include standard OpenAI parameters such as `temperature`,
  `top_p`, `max_tokens`, `max_completion_tokens`, `stop`, `seed`, and
  `logit_bias`.
- Docker-hosted Open WebUI must use a container-reachable URL. In this Compose
  stack the API service URL is `http://api:8000/v1`; from a standalone Open
  WebUI container targeting a host process, use `host.docker.internal`. From
  the host browser, the default Compose URL is `http://localhost:23000`.

## Compose Configuration

`compose.yaml` starts Open WebUI with environment-owned local configuration:

```text
OPENAI_API_BASE_URLS=http://api:8000/v1
OPENAI_API_KEYS=local-dev-placeholder
WEBUI_AUTH=False
ENABLE_PERSISTENT_CONFIG=False
ENABLE_OLLAMA_API=False
```

`OPENAI_API_KEYS` is a local placeholder because this repository's local API
does not enforce provider authentication yet. Do not commit real provider keys.
When a real backend requires a key, pass it through local shell environment or a
secret manager, not through tracked files.

`ENABLE_PERSISTENT_CONFIG=False` keeps local container restarts aligned with
the environment variables instead of stale values saved in Open WebUI's data
volume. UI edits made in that mode are not the durable source of truth.

`WEBUI_AUTH=False` is only for this local single-user lab smoke. Production or
shared Mac Studio deployments need authentication, secret management, and a
separate operator access policy before exposing Open WebUI beyond localhost or
a private admin network.

`ENABLE_OLLAMA_API=False` disables Open WebUI's default Ollama probe. This
profile intentionally uses only this repository's OpenAI-compatible API, so
missing `host.docker.internal:11434` logs are not useful signal.

## API Compatibility

This project's API must stay compatible with the Open WebUI path:

```bash
curl http://localhost:28000/v1/models \
  -H 'Authorization: Bearer local-dev-placeholder'
```

```bash
curl http://localhost:28000/v1/chat/completions \
  -H 'Authorization: Bearer local-dev-placeholder' \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "fake-local-model",
    "messages": [{"role": "user", "content": "hello webui"}],
    "temperature": 0.2,
    "max_completion_tokens": 32,
    "stream": false
  }'
```

The API accepts the placeholder bearer token without treating it as a secret,
returns OpenAI-style model records, returns non-streaming `usage`, and forwards
standard generation parameters to an OpenAI-compatible native backend such as
`vllm-mlx`.

## Runtime Proof

Open WebUI workflow integration is complete for the Docker Compose fake-backend
stack. The current saved evidence bundle is:

```text
artifacts/runtime/2026-06-28T163030+0200-open-webui/
```

That bundle shows:

- Open WebUI container is healthy and reachable at `http://localhost:23000`.
- Open WebUI sees the API model through `/v1/models`.
- A chat request submitted through Open WebUI reaches
  `/v1/chat/completions`.
- The browser renders the fake-backend response for `fake-local-model`.
- The saved evidence is publish-safe: no real API keys, cookies, JWTs, prompts
  that should stay private, local home paths, model cache contents, or database
  files.

Open WebUI still needs a separate proof against the native `vllm-mlx` backend
before real-backend UX performance or cancellation behavior is claimed.
