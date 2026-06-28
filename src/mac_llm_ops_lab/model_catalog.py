import argparse
import json
import os
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

from mac_llm_ops_lab.runtime_guard import (
    RuntimePreflightPlan,
    build_runtime_preflight_report,
)

APPROVED_MODEL_CATALOG_SCHEMA_VERSION = "approved-model-catalog/v1"
_CACHE_IGNORE_PATTERNS = ("model-cache/", "models/")


@dataclass(frozen=True)
class ApprovedModelEntry:
    model_id: str
    backend_id: str
    display_name: str
    source_url: str
    revision: str
    license: str
    library_name: str
    pipeline_tag: str
    tags: tuple[str, ...]
    cache_root: str
    model_weights_gib: float
    kv_cache_gib: float
    runtime_overhead_gib: float
    service_overhead_gib: float

    @property
    def estimated_runtime_total_gib(self) -> float:
        return round(
            self.model_weights_gib
            + self.kv_cache_gib
            + self.runtime_overhead_gib
            + self.service_overhead_gib,
            3,
        )


_APPROVED_MODELS = {
    "mlx-community/Qwen3-0.6B-8bit": ApprovedModelEntry(
        model_id="mlx-community/Qwen3-0.6B-8bit",
        backend_id="vllm-mlx",
        display_name="Qwen3 0.6B 8-bit MLX",
        source_url="https://huggingface.co/mlx-community/Qwen3-0.6B-8bit",
        revision="11de96878523501bcaa86104e3c186de07ff9068",
        license="apache-2.0",
        library_name="mlx",
        pipeline_tag="text-generation",
        tags=("8-bit", "conversational", "mlx", "qwen3", "text-generation"),
        cache_root="model-cache/huggingface",
        model_weights_gib=1.2,
        kv_cache_gib=2.0,
        runtime_overhead_gib=1.0,
        service_overhead_gib=0.5,
    )
}


def get_approved_model_entry(model_id: str) -> ApprovedModelEntry:
    return _APPROVED_MODELS[model_id]


def build_model_download_gate_report(
    *,
    model_id: str,
    explicitly_approved: bool,
    gitignore_text: str,
) -> dict[str, object]:
    entry = _APPROVED_MODELS.get(model_id)
    report: dict[str, object] = {
        "schema_version": APPROVED_MODEL_CATALOG_SCHEMA_VERSION,
        "model_id": model_id,
    }
    if entry is None:
        report["decision"] = _decision(
            allowed=False,
            reason_code="model_not_in_catalog",
            message="Model is not in the approved local catalog.",
        )
        return report

    report["model_card"] = _model_card(entry)
    missing_ignore_patterns = _missing_cache_ignore_patterns(gitignore_text)
    report["missing_ignore_patterns"] = missing_ignore_patterns
    preflight_report = build_runtime_preflight_report(
        RuntimePreflightPlan(
            backend_id=entry.backend_id,
            model_id=entry.model_id,
            explicitly_authorized=explicitly_approved,
            model_weights_gib=entry.model_weights_gib,
            kv_cache_gib=entry.kv_cache_gib,
            runtime_overhead_gib=entry.runtime_overhead_gib,
            service_overhead_gib=entry.service_overhead_gib,
        )
    )
    report["preflight_report"] = preflight_report

    if missing_ignore_patterns:
        report["decision"] = _decision(
            allowed=False,
            reason_code="runtime_cache_not_ignored",
            message="Runtime model cache paths must be excluded from git.",
        )
        return report

    preflight_decision = preflight_report["decision"]
    if not preflight_decision["allowed"]:
        report["decision"] = dict(preflight_decision)
        return report

    report["decision"] = _decision(
        allowed=True,
        reason_code="model_download_gate_passed",
        message="Model catalog, approval, memory, and cache policy passed.",
    )
    return report


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate that a local MLX model download/run is approved.",
    )
    parser.add_argument("model_id")
    parser.add_argument("--gitignore", default=".gitignore")
    parser.add_argument(
        "--report-path",
        default=os.environ.get("MODEL_DOWNLOAD_GATE_REPORT", ""),
    )
    args = parser.parse_args(argv)

    report = build_model_download_gate_report(
        model_id=args.model_id,
        explicitly_approved=_parse_bool(
            os.environ.get("MAC_LLM_OPS_MODEL_DOWNLOAD_APPROVED", "false")
        ),
        gitignore_text=Path(args.gitignore).read_text(encoding="utf-8"),
    )
    payload = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.report_path:
        report_path = Path(args.report_path)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0 if report["decision"]["allowed"] else 2


def _model_card(entry: ApprovedModelEntry) -> dict[str, object]:
    return {
        "model_id": entry.model_id,
        "source_url": entry.source_url,
        "revision": entry.revision,
        "license": entry.license,
        "library_name": entry.library_name,
        "pipeline_tag": entry.pipeline_tag,
        "tags": list(entry.tags),
        "cache_root": entry.cache_root,
    }


def _missing_cache_ignore_patterns(gitignore_text: str) -> list[str]:
    configured_patterns = {
        line.strip()
        for line in gitignore_text.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }
    return [
        pattern
        for pattern in _CACHE_IGNORE_PATTERNS
        if pattern not in configured_patterns
    ]


def _decision(*, allowed: bool, reason_code: str, message: str) -> dict[str, object]:
    return {
        "allowed": allowed,
        "reason_code": reason_code,
        "message": message,
    }


def _parse_bool(value: str) -> bool:
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off", ""}:
        return False
    raise ValueError(f"Invalid boolean setting: {value!r}")


if __name__ == "__main__":
    raise SystemExit(main())
