from dataclasses import dataclass

DEFAULT_MEMORY_CEILING_GIB = 24.0


@dataclass(frozen=True)
class RuntimePreflightPlan:
    backend_id: str
    model_id: str
    explicitly_authorized: bool
    model_weights_gib: float
    kv_cache_gib: float
    runtime_overhead_gib: float
    service_overhead_gib: float
    memory_ceiling_gib: float = DEFAULT_MEMORY_CEILING_GIB

    @property
    def estimated_total_gib(self) -> float:
        return round(
            self.model_weights_gib
            + self.kv_cache_gib
            + self.runtime_overhead_gib
            + self.service_overhead_gib,
            3,
        )


@dataclass(frozen=True)
class RuntimePreflightDecision:
    allowed: bool
    reason_code: str
    message: str
    estimated_total_gib: float
    memory_ceiling_gib: float


def evaluate_runtime_preflight(
    plan: RuntimePreflightPlan,
) -> RuntimePreflightDecision:
    estimated_total_gib = plan.estimated_total_gib
    if _has_negative_memory_estimate(plan):
        return RuntimePreflightDecision(
            allowed=False,
            reason_code="invalid_memory_estimate",
            message="Runtime memory estimates must be non-negative.",
            estimated_total_gib=estimated_total_gib,
            memory_ceiling_gib=plan.memory_ceiling_gib,
        )
    if not plan.explicitly_authorized:
        return RuntimePreflightDecision(
            allowed=False,
            reason_code="runtime_not_authorized",
            message=(
                "Explicit authorization is required before real-model runtime "
                "execution."
            ),
            estimated_total_gib=estimated_total_gib,
            memory_ceiling_gib=plan.memory_ceiling_gib,
        )
    if estimated_total_gib > plan.memory_ceiling_gib:
        return RuntimePreflightDecision(
            allowed=False,
            reason_code="memory_ceiling_exceeded",
            message="Estimated runtime memory exceeds the configured ceiling.",
            estimated_total_gib=estimated_total_gib,
            memory_ceiling_gib=plan.memory_ceiling_gib,
        )
    return RuntimePreflightDecision(
        allowed=True,
        reason_code="runtime_preflight_passed",
        message="Runtime preflight passed.",
        estimated_total_gib=estimated_total_gib,
        memory_ceiling_gib=plan.memory_ceiling_gib,
    )


def _has_negative_memory_estimate(plan: RuntimePreflightPlan) -> bool:
    return any(
        value < 0
        for value in (
            plan.model_weights_gib,
            plan.kv_cache_gib,
            plan.runtime_overhead_gib,
            plan.service_overhead_gib,
            plan.memory_ceiling_gib,
        )
    )
