# Demo Script

## Demo Goal

Show that the team completed the observability lab end to end: structured logging, correlation IDs, PII scrubbing, Langfuse traces, SLO-aware dashboarding, alert/runbook readiness, and incident debugging.

## Presenter Plan

- Lead host: Lê Đức Thanh
- Backup host and Q&A support: Phan Tuấn Minh
- Logging & PII demo: Bùi Minh Ngọc
- Tracing & request context demo: Phạm Việt Anh
- SLOs, alerts, and runbook demo: Nguyễn Thùy Linh
- Incident injection and debugging demo: Phạm Đình Trường
- Dashboard walkthrough: Phạm Việt Hoàng

## Demo Flow

1. Health check and intro
   - Speaker: Lê Đức Thanh
   - Command: `curl http://127.0.0.1:8000/health`
   - Expected outcome: app responds `{"ok": true, ...}` and the team explains the system modules quickly.

2. Send one normal request
   - Speaker: Phạm Việt Anh
   - Command:
     ```bash
     curl -X POST http://127.0.0.1:8000/chat \
       -H "Content-Type: application/json" \
       -d "{\"user_id\":\"u01\",\"session_id\":\"s01\",\"feature\":\"qa\",\"message\":\"What is the refund policy?\"}"
     ```
   - Expected outcome: response includes `correlation_id`, latency, tokens, cost, and quality score.

3. Show logs with correlation ID and PII protection
   - Speaker: Bùi Minh Ngọc
   - Evidence:
     - `docs/screenshots/correlation_id in log.jpg`
     - `docs/evidence/pii-redaction-log.txt`
   - Talking points:
     - every request gets `correlation_id`
     - `user_id` is hashed
     - email, phone, and credit card patterns are redacted before writing logs

4. Show Langfuse traces
   - Speaker: Phạm Việt Anh, support by Phạm Đình Trường
   - Evidence:
     - `docs/screenshots/trace_list.jpg`
     - `docs/screenshots/trace_check.jpg`
     - `docs/evidence/langfuse-trace-summary.txt`
   - Talking points:
     - there are at least 10 traces; the captured set shows 41 traces
     - tags include `lab`, feature name, and model name
     - trace context matches log context for faster debugging

5. Show dashboard and SLO alignment
   - Speaker: Phạm Việt Hoàng
   - Evidence: `docs/screenshots/dashboard.png`
   - Talking points:
     - 6 required panels are present
     - default range is 1 hour and auto refresh is 15 seconds
     - current steady-state snapshot: P95 `151ms`, error rate `0%`, total cost `$0.0221`, quality `0.88`

6. Show alerts and runbook
   - Speaker: Nguyễn Thùy Linh
   - Evidence:
     - `docs/screenshots/alert-rules.png`
     - `docs/alerts.md`
   - Talking points:
     - alert coverage includes latency, error rate, cost spike, and low quality
     - each alert is mapped to a runbook section

7. Inject one incident and debug it
   - Speaker: Phạm Đình Trường
   - Scenario: `tool_fail`
   - Commands:
     ```bash
     python scripts/inject_incident.py --scenario tool_fail
     python scripts/load_test.py
     ```
   - Evidence:
     - `docs/screenshots/tool_fail.jpg`
     - `docs/screenshots/validate_logs.jpg`
   - Talking points:
     - load test starts returning HTTP 500
     - logs show `RuntimeError: Vector store timeout`
     - root cause is the retrieval/tool layer, not log formatting or the dashboard

8. Explain recovery
   - Speaker: Lê Đức Thanh
   - Command:
     ```bash
     python scripts/inject_incident.py --scenario tool_fail --disable
     ```
   - Expected outcome: team explains that traffic should return to normal and alerts should clear once the failure toggle is removed.

9. Close with validation score
   - Speaker: Phan Tuấn Minh
   - Evidence: `docs/screenshots/validate_logs.jpg`
   - Talking points:
     - validate score is `100/100`
     - correlation ID, enrichment, and PII scrubbing all passed
     - final report and evidence paths are ready in `docs/`

## Quick Q&A

- Why do we need `correlation_id`?
  - It ties one request across logs, headers, traces, and incident debugging.
- How do we prove PII is not leaked?
  - By showing redacted previews in logs and the validate score with `PII leaks detected: 0`.
- Why is the dashboard useful if logs already exist?
  - Logs explain single events, while the dashboard shows system trends, thresholds, and budget signals over time.
- How did the team isolate `tool_fail` quickly?
  - Error-rate spike on the dashboard plus `RuntimeError: Vector store timeout` in structured logs narrowed the issue to retrieval/tooling immediately.
