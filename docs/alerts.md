# Alert Rules and Runbooks

## 1. High latency P95
- Severity: P2
- Trigger: `latency_p95_ms > 5000 for 30m`
- Impact: tail latency breaches SLO
- First checks:
  1. Open top slow traces in the last 1h
  2. Compare RAG span vs LLM span
  3. Check if incident toggle `rag_slow` is enabled
- Mitigation:
  - truncate long queries
  - fallback retrieval source
  - lower prompt size

## 2. High error rate
- Severity: P1
- Trigger: `error_rate_pct > 5 for 5m`
- Impact: users receive failed responses
- First checks:
  1. Group logs by `error_type`
  2. Inspect failed traces
  3. Determine whether failures are LLM, tool, or schema related
- Mitigation:
  - rollback latest change
  - disable failing tool
  - retry with fallback model

## 3. Cost budget spike
- Severity: P2
- Trigger: `hourly_cost_usd > 2x_baseline for 15m`
- Impact: burn rate exceeds budget
- First checks:
  1. Split traces by feature and model
  2. Compare tokens_in/tokens_out
  3. Check if `cost_spike` incident was enabled
- Mitigation:
  - shorten prompts
  - route easy requests to cheaper model
  - apply prompt cache

## 4. Low quality score
- Severity: P2
- Trigger: `quality_score_avg < 0.75 for 30m`
- Impact: answer quality drifts below acceptable user experience
- First checks:
  1. Inspect recent traces with low quality metadata and compare input/output pairs
  2. Check whether retrieval returned empty or low-relevance context (`doc_count` in trace metadata)
  3. Verify if any prompt, model, or feature routing change was deployed recently
- Mitigation:
  - tighten prompt instructions and enforce answer format constraints
  - add fallback retrieval strategy when doc relevance is low
  - route impacted feature to a higher-quality model temporarily
