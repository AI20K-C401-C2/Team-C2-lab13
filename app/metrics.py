from __future__ import annotations

from collections import Counter
from statistics import mean

REQUEST_LATENCIES: list[int] = []
REQUEST_COSTS: list[float] = []
REQUEST_TOKENS_IN: list[int] = []
REQUEST_TOKENS_OUT: list[int] = []
ERRORS: Counter[str] = Counter()
ERROR_DETAILS: list[dict] = []
TRAFFIC: int = 0
QUALITY_SCORES: list[float] = []
MAX_ERROR_DETAILS = 50


def record_request(latency_ms: int, cost_usd: float, tokens_in: int, tokens_out: int, quality_score: float) -> None:
    global TRAFFIC
    TRAFFIC += 1
    REQUEST_LATENCIES.append(latency_ms)
    REQUEST_COSTS.append(cost_usd)
    REQUEST_TOKENS_IN.append(tokens_in)
    REQUEST_TOKENS_OUT.append(tokens_out)
    QUALITY_SCORES.append(quality_score)



def record_error(error_type: str, correlation_id: str = "", detail: str = "", user_id_hash: str = "") -> None:
    ERRORS[error_type] += 1
    ERROR_DETAILS.append({
        "error_type": error_type,
        "correlation_id": correlation_id or "unknown",
        "detail": detail or "No detail provided",
        "user_id_hash": user_id_hash or "unknown",
        "timestamp": __import__("time").time(),
    })
    if len(ERROR_DETAILS) > MAX_ERROR_DETAILS:
        ERROR_DETAILS.pop(0)



def percentile(values: list[int], p: int) -> float:
    if not values:
        return 0.0
    items = sorted(values)
    idx = max(0, min(len(items) - 1, round((p / 100) * len(items) + 0.5) - 1))
    return float(items[idx])



def snapshot() -> dict:
    return {
        "traffic": TRAFFIC,
        "latency_p50": percentile(REQUEST_LATENCIES, 50),
        "latency_p95": percentile(REQUEST_LATENCIES, 95),
        "latency_p99": percentile(REQUEST_LATENCIES, 99),
        "avg_cost_usd": round(mean(REQUEST_COSTS), 4) if REQUEST_COSTS else 0.0,
        "total_cost_usd": round(sum(REQUEST_COSTS), 4),
        "tokens_in_total": sum(REQUEST_TOKENS_IN),
        "tokens_out_total": sum(REQUEST_TOKENS_OUT),
        "error_breakdown": dict(ERRORS),
        "quality_avg": round(mean(QUALITY_SCORES), 4) if QUALITY_SCORES else 0.0,
    }


def error_snapshot() -> list[dict]:
    return [
        {
            "error_type": e["error_type"],
            "correlation_id": e["correlation_id"],
            "detail": e["detail"],
            "user_id_hash": e["user_id_hash"],
            "timestamp": e["timestamp"],
        }
        for e in ERROR_DETAILS
    ]
