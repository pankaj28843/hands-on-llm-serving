# Operations

## Local Docker Stack

The local stack runs PostgreSQL, Phoenix, Open WebUI, and the fake-backend API.
Create a local placeholder password file before starting Compose:

```bash
mkdir -p secrets artifacts/runtime
printf 'local-dev-password\n' > secrets/postgres_password.txt
docker compose up -d --build
```

The default local endpoints are:

- API: `http://localhost:28000`
- Open WebUI: `http://localhost:23000`
- Phoenix: `http://localhost:26006`
- PostgreSQL: `localhost:25432`
- OTLP gRPC: `localhost:24317`
- Phoenix Prometheus: `http://localhost:29090`

All host bindings stay in the `20000-50000` range. Override them with the
Compose environment variables documented in [Runtime Stack](runtime-stack.md)
when a local port is already in use.

## Probes

```bash
curl -fsS http://localhost:28000/live
curl -fsS http://localhost:28000/ready
curl -fsS http://localhost:28000/v1/models \
  -H 'Authorization: Bearer local-dev-placeholder'
curl -fsS http://localhost:26006/ >/dev/null
```

Use [Observability](observability.md) to verify Phoenix spans and
[Open WebUI](open-webui.md) to verify the UI workflow.

## Safety

Never commit local secrets, model caches, runtime evidence, database files,
logs, traces, or raw benchmark payloads. Keep those under ignored directories
and summarize only publish-safe evidence in docs.
