from collections.abc import Mapping, Sequence

RUNTIME_EVIDENCE_MANIFEST_SCHEMA_VERSION = "runtime-evidence-manifest/v1"


def build_runtime_evidence_manifest(
    *,
    git_sha: str,
    command: Sequence[str],
    artifact_dir: str,
    log_path: str,
    host: Mapping[str, object],
    backend_id: str,
    model_id: str,
    runtime_config: Mapping[str, object],
    ports: Mapping[str, int],
) -> dict[str, object]:
    return {
        "schema_version": RUNTIME_EVIDENCE_MANIFEST_SCHEMA_VERSION,
        "git_sha": git_sha,
        "command": list(command),
        "artifact_dir": artifact_dir,
        "log_path": log_path,
        "host": dict(host),
        "backend": {
            "id": backend_id,
            "model_id": model_id,
        },
        "runtime_config": dict(runtime_config),
        "ports": dict(ports),
    }
