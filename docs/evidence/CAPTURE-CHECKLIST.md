# Evidence Capture Checklist

Mo cac file duoi day va chup man hinh khi he thong dang chay on:

1. `docs/evidence/correlation-id-log.txt`
   Muc dich: chung minh log co `correlation_id`, `session_id`, `user_id_hash`.

2. `docs/evidence/pii-redaction-log.txt`
   Muc dich: chung minh email, so dien thoai, credit card da duoc redaction.

3. `docs/evidence/metrics-snapshot.json`
   Muc dich: chung minh he thong da co traffic, latency, token, cost va quality.

4. `docs/evidence/langfuse-trace-summary.txt`
   Muc dich: doi chieu voi trace list tren Langfuse. Nen chup them giao dien Langfuse de co bang chung manh hon.

5. `config/alert_rules.yaml`
   Muc dich: chup anh alert rules.

6. `docs/alerts.md`
   Muc dich: chup anh runbook.

7. Langfuse UI
   Muc dich:
   - chup trace list co >= 10 traces
   - chup 1 trace waterfall

8. Dashboard UI
   Muc dich: chup dashboard du 6 panel theo `docs/dashboard-spec.md`.

Luu y:
- Cac file trong `docs/evidence/` la bang chung dang text/json de chup nhanh trong editor.
- Anh cuoi cung nen luu vao `docs/evidence/` de de dien vao report.
