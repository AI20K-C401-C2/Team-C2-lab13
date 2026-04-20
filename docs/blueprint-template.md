# Day 13 Observability Lab Report

> **Instruction**: Fill in all sections below. This report is designed to be parsed by an automated grading assistant. Ensure all tags (e.g., `[GROUP_NAME]`) are preserved.

## 1. Team Metadata
- <!-- -->[GROUP_NAME]: Team C2
- <!-- -->[REPO_URL]: https://github.com/AI20K-C401-C2/Team-C2-lab13
- <!-- -->[MEMBERS]:
  - Member A: Bùi Minh Ngọc | Role: Logging & PII
  - Member B: Phạm Việt Anh | Role: Tracing & Enrichment
  - Member C: Nguyễn Thùy Linh | Role: SLO & Alerts
  - Member D: Phạm Đình Trường | Role: Load Test & Incident Injection
  - Member E: Phạm Việt Hoàng | Role: Dashboard & Evidence
  - Member F: Lê Đức Thanh và Phan Tuấn Minh | Role: Blueprint Report & Demo Lead

---

## 2. Group Performance (Auto-Verified)
- <!-- -->[VALIDATE_LOGS_FINAL_SCORE]: 100/100. Nhóm đối chiếu từ `docs/screenshots/validate_logs.jpg`, trong đó missing required fields = 0 và missing enrichment = 0.
- <!-- -->[TOTAL_TRACES_COUNT]: 41 traces. Nhóm đối chiếu từ `docs/screenshots/trace_list.jpg`, có trace cho các session s01 đến s10 và nhiều request khác trong cùng khoảng thời gian.
- <!-- -->[PII_LEAKS_FOUND]: 0. Nhóm đối chiếu từ `docs/screenshots/validate_logs.jpg` và log đã redact trong `docs/evidence/pii-redaction-log.txt`.

---

## 3. Technical Evidence (Group)

### 3.1 Logging & Tracing
- <!-- -->[EVIDENCE_CORRELATION_ID_SCREENSHOT]: docs/screenshots/correlation_id in log.jpg
- <!-- -->[EVIDENCE_PII_REDACTION_SCREENSHOT]: docs/evidence/pii-redaction-evidence.svg
- <!-- -->[EVIDENCE_TRACE_WATERFALL_SCREENSHOT]: docs/evidence/trace-waterfall-evidence.svg
- <!-- -->[TRACE_WATERFALL_EXPLANATION]: Từ phần trace detail mà nhóm tổng hợp lại, tụi em thấy mỗi request đều có `user_id` đã băm, `session_id` và tag như `lab`, `qa`, `summary`, `claude-sonnet-4-5`. Nhờ vậy nhóm dùng trace để khoanh vùng đúng request đang bị lỗi theo thời gian và session, sau đó đối chiếu qua log JSON để tìm nguyên nhân cuối cùng. Cách làm của nhóm là đi theo thứ tự: thấy metrics tăng bất thường, mở trace đúng thời điểm để xác định request bị ảnh hưởng, rồi xem log để chốt lỗi `RuntimeError: Vector store timeout`.

### 3.2 Dashboard & SLOs
- <!-- -->[DASHBOARD_6_PANELS_SCREENSHOT]: docs/screenshots/dashboard.png
- <!-- -->[SLO_TABLE]:
| SLI | Target | Window | Current Value |
|---|---:|---|---:|
| Latency P95 | < 3000ms | 28d | 151ms |
| Error Rate | < 2% | 28d | 0% (trạng thái bình thường) |
| Cost Budget | < $2.5/day | 1d | $0.0221 (tổng chi phí của lần chạy hiện tại) |
| Quality Avg | > 0.75 | 28d | 0.88 |

### 3.3 Alerts & Runbook
- <!-- -->[ALERT_RULES_SCREENSHOT]: docs/screenshots/alert-rules.png. Nhóm hiện có 4 alert là `high_latency_p95`, `high_error_rate`, `cost_budget_spike`, `low_quality_score`.
- <!-- -->[SAMPLE_RUNBOOK_LINK]: docs/alerts.md#2-high-error-rate. Runbook này dùng khi error rate tăng, hướng dẫn kiểm tra trace lỗi, nhóm log theo `error_type` và chọn hướng xử lý như rollback, disable tool hoặc fallback model.

---

## 4. Incident Response (Group)
- <!-- -->[SCENARIO_NAME]: tool_fail
- <!-- -->[SYMPTOMS_OBSERVED]: Khi chạy load test, nhiều request tới `/chat` bị trả về HTTP 500 liên tục. Trên dashboard thì phần error rate tăng lên 2%, còn trong log xuất hiện `request_failed` thay vì `response_sent` như lúc hệ thống chạy bình thường.
- <!-- -->[ROOT_CAUSE_PROVED_BY]: Nhóm đi theo flow `Metrics -> Traces -> Logs`. Đầu tiên dashboard cho thấy error rate tăng lên 2%. Sau đó nhóm mở trace đúng thời điểm bị lỗi để xác định request/session bị ảnh hưởng. Cuối cùng log trong `docs/screenshots/tool_fail.jpg` cho thấy rõ `error_type: "RuntimeError"` với `detail: "Vector store timeout"`, kèm các dòng load test `[500] None`, nên nhóm kết luận lỗi nằm ở phần tool/retrieval bị timeout.
- <!-- -->[FIX_ACTION]: Tắt incident `tool_fail`, chạy lại load test và kiểm tra xem API trả về HTTP 200 bình thường, đồng thời error rate quay về mức ổn định.
- <!-- -->[PREVENTIVE_MEASURE]: Giữ alert error rate để phát hiện sớm, thêm hướng fallback khi retrieval bị lỗi và tiếp tục giữ correlation ID cùng trace tag để lần sau debug nhanh hơn.

---

## 5. Individual Contributions & Evidence

### <!-- -->[MEMBER_A_NAME]
- <!-- -->[TASKS_COMPLETED]: Bùi Minh Ngọc hoàn thành phần ẩn thông tin nhạy cảm trong log bằng cách bật `scrub_event`, thêm các mẫu PII mới và viết thêm test trong `tests/test_pii.py` để kiểm tra việc che email, số điện thoại, CCCD, thẻ.
- <!-- -->[EVIDENCE_LINK]: https://github.com/AI20K-C401-C2/Team-C2-lab13/commit/1608cb8

### <!-- -->[MEMBER_B_NAME]
- <!-- -->[TASKS_COMPLETED]: Phạm Việt Anh làm phần correlation ID trong middleware, bổ sung thông tin ngữ cảnh cho log như `user_id_hash`, `session_id`, `feature`, `model` và hỗ trợ phần hướng dẫn luồng observability của nhóm.
- <!-- -->[EVIDENCE_LINK]: https://github.com/AI20K-C401-C2/Team-C2-lab13/commit/98645a1

### <!-- -->[MEMBER_C_NAME]
- <!-- -->[TASKS_COMPLETED]: Nguyễn Thùy Linh cập nhật SLO, bổ sung alert `low_quality_score`, hoàn thiện runbook trong `docs/alerts.md` và chuẩn bị ảnh minh chứng cho phần alert rules.
- <!-- -->[EVIDENCE_LINK]: https://github.com/AI20K-C401-C2/Team-C2-lab13/commit/89d326a

### <!-- -->[MEMBER_D_NAME]
- <!-- -->[TASKS_COMPLETED]: Phạm Đình Trường chuẩn bị môi trường test, chạy load test, bật các incident để kiểm tra hệ thống và thu thập log, screenshot khi hệ thống bị lỗi để nhóm dùng trong báo cáo.
- <!-- -->[EVIDENCE_LINK]: https://github.com/AI20K-C401-C2/Team-C2-lab13/pull/3

### <!-- -->[MEMBER_E_NAME]
- <!-- -->[TASKS_COMPLETED]: Phạm Việt Hoàng xây dựng dashboard, kết nối dữ liệu metrics và làm đủ 6 panel theo yêu cầu để theo dõi latency, traffic, error rate, cost, tokens và quality score.
- <!-- -->[EVIDENCE_LINK]: https://github.com/AI20K-C401-C2/Team-C2-lab13/commit/29b07ec

### <!-- -->[MEMBER_F_NAME]
- <!-- -->[TASKS_COMPLETED]: Lê Đức Thanh và Phan Tuấn Minh tổng hợp báo cáo blueprint, gom evidence của cả nhóm, tóm tắt thông tin trace và metrics, đồng thời chuẩn bị kịch bản demo để thuyết trình.
- <!-- -->[EVIDENCE_LINK]: https://github.com/AI20K-C401-C2/Team-C2-lab13/commit/e763753

---

## 6. Bonus Items (Optional)
- <!-- -->[BONUS_COST_OPTIMIZATION]: Nhóm có thử scenario `cost_spike` để quan sát chi phí tăng như thế nào và lưu lại kết quả ở `docs/screenshots/Cost_Spike.jpg`.
- <!-- -->[BONUS_AUDIT_LOGS]: Log JSON của nhóm có `correlation_id`, `user_id` đã băm và nội dung nhạy cảm đã được che bớt. Có thể xem ở `docs/screenshots/correlation_id in log.jpg` và `docs/evidence/pii-redaction-log.txt`.
- <!-- -->[BONUS_CUSTOM_METRIC]: Dashboard không chỉ có latency mà còn theo dõi thêm `quality_avg` và số lượng token in/out, thể hiện trong `docs/screenshots/dashboard.png`.
