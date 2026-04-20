from __future__ import annotations


def render_dashboard() -> str:
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Day 13 Observability Dashboard</title>
  <style>
    :root {
      --bg: #f5efe5;
      --panel: rgba(255, 250, 242, 0.92);
      --ink: #1f2933;
      --muted: #5c6b73;
      --line: rgba(31, 41, 51, 0.12);
      --accent: #0f766e;
      --accent-soft: rgba(15, 118, 110, 0.14);
      --warm: #c26d2d;
      --rose: #b8455b;
      --ok: #2f855a;
      --shadow: 0 18px 40px rgba(91, 65, 41, 0.12);
    }

    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      min-height: 100vh;
      font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
      color: var(--ink);
      background:
        radial-gradient(circle at top left, rgba(194, 109, 45, 0.18), transparent 28%),
        radial-gradient(circle at top right, rgba(15, 118, 110, 0.14), transparent 24%),
        linear-gradient(135deg, #fbf7f2 0%, #efe7da 52%, #e7e2d9 100%);
      padding: 20px;
    }

    .shell {
      max-width: 1240px;
      margin: 0 auto;
    }

    .hero {
      display: grid;
      grid-template-columns: 1.45fr 0.95fr;
      gap: 18px;
      margin-bottom: 18px;
    }

    .hero-card,
    .panel {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 24px;
      box-shadow: var(--shadow);
      backdrop-filter: blur(10px);
    }

    .hero-card {
      padding: 28px;
    }

    .kicker {
      text-transform: uppercase;
      letter-spacing: 0.18em;
      font-size: 12px;
      color: var(--warm);
      margin-bottom: 10px;
      font-weight: 700;
    }

    h1 {
      margin: 0;
      font-size: clamp(34px, 4vw, 54px);
      line-height: 0.95;
    }

    .hero-copy {
      margin: 16px 0 0;
      color: var(--muted);
      max-width: 62ch;
      line-height: 1.5;
      font-size: 16px;
    }

    .hero-stats {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 12px;
      margin-top: 22px;
    }

    .mini {
      padding: 16px 18px;
      border-radius: 20px;
      background: rgba(255, 255, 255, 0.55);
      border: 1px solid rgba(31, 41, 51, 0.08);
    }

    .mini-label {
      color: var(--muted);
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      margin-bottom: 10px;
    }

    .mini-value {
      font-size: 26px;
      font-weight: 800;
    }

    .meta-card {
      padding: 24px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 18px;
    }

    .status-pill {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      width: fit-content;
      padding: 10px 14px;
      border-radius: 999px;
      background: rgba(47, 133, 90, 0.1);
      color: var(--ok);
      font-weight: 700;
      font-size: 14px;
    }

    .status-dot {
      width: 10px;
      height: 10px;
      border-radius: 999px;
      background: currentColor;
      box-shadow: 0 0 0 6px rgba(47, 133, 90, 0.14);
    }

    .meta-list {
      display: grid;
      gap: 14px;
      margin-top: 8px;
    }

    .meta-row {
      display: flex;
      justify-content: space-between;
      gap: 12px;
      color: var(--muted);
      border-bottom: 1px dashed rgba(31, 41, 51, 0.12);
      padding-bottom: 12px;
      font-size: 16px;
    }

    .meta-row strong {
      color: var(--ink);
      font-weight: 800;
    }

    .meta-badges {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
    }

    .badge {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 10px 14px;
      border-radius: 999px;
      background: rgba(47, 133, 90, 0.08);
      color: var(--ok);
      border: 1px solid rgba(31, 41, 51, 0.08);
      font-size: 13px;
      font-weight: 700;
    }

    .badge-dot {
      width: 8px;
      height: 8px;
      border-radius: 999px;
      background: currentColor;
    }

    .grid {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 18px;
    }

    .panel {
      padding: 20px;
      min-height: 270px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      overflow: hidden;
      position: relative;
    }

    .panel::after {
      content: "";
      position: absolute;
      inset: auto -30px -30px auto;
      width: 120px;
      height: 120px;
      border-radius: 999px;
      background: linear-gradient(135deg, rgba(15, 118, 110, 0.12), rgba(194, 109, 45, 0.08));
      filter: blur(10px);
    }

    .panel-head {
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 12px;
    }

    .panel-title {
      margin: 0;
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.14em;
      color: var(--muted);
    }

    .panel-value {
      margin-top: 12px;
      font-size: clamp(34px, 4vw, 42px);
      font-weight: 800;
      line-height: 1;
    }

    .panel-caption {
      margin-top: 12px;
      color: var(--muted);
      line-height: 1.45;
      font-size: 14px;
    }

    .bar-group {
      display: grid;
      gap: 10px;
      margin-top: 14px;
    }

    .bar-row {
      display: grid;
      grid-template-columns: 55px 1fr auto;
      align-items: center;
      gap: 10px;
      font-size: 14px;
      color: var(--muted);
    }

    .bar {
      height: 10px;
      background: rgba(31, 41, 51, 0.08);
      border-radius: 999px;
      overflow: hidden;
    }

    .bar > span {
      display: block;
      height: 100%;
      border-radius: 999px;
      background: linear-gradient(90deg, var(--accent), #2ab3a6);
    }

    .split {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 12px;
      margin-top: 12px;
    }

    .stat-box {
      border-radius: 18px;
      padding: 14px;
      background: rgba(255, 255, 255, 0.6);
      border: 1px solid rgba(31, 41, 51, 0.08);
    }

    .stat-box .label {
      font-size: 12px;
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: 0.08em;
      margin-bottom: 8px;
    }

    .stat-box .value {
      font-size: 24px;
      font-weight: 700;
    }

    .error-empty {
      margin-top: 16px;
      padding: 16px 18px;
      border-radius: 18px;
      background: rgba(47, 133, 90, 0.08);
      color: var(--ok);
      font-weight: 700;
      width: fit-content;
    }

    .quality-ring {
      width: 130px;
      height: 130px;
      margin: 8px auto 0;
      border-radius: 999px;
      display: grid;
      place-items: center;
      background: conic-gradient(var(--warm) 0deg, var(--warm) calc(var(--score) * 360deg), rgba(31, 41, 51, 0.08) 0deg);
    }

    .quality-core {
      width: 90px;
      height: 90px;
      border-radius: 999px;
      background: #fffaf4;
      display: grid;
      place-items: center;
      text-align: center;
      box-shadow: inset 0 0 0 1px rgba(31, 41, 51, 0.08);
    }

    .quality-core strong {
      display: block;
      font-size: 26px;
    }

    .quality-core span {
      font-size: 12px;
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }

    @media (max-width: 960px) {
      body {
        padding: 14px;
      }

      .hero,
      .grid {
        grid-template-columns: 1fr;
      }
    }
  </style>
</head>
<body>
  <main class="shell">
    <section class="hero">
      <div class="hero-card">
        <div class="kicker">Day 13 Observability Lab</div>
        <h1>AI Service Dashboard</h1>
        <p class="hero-copy">
          Bang theo doi nay tong hop 6 panel quan trong nhat de nhom nhin nhanh tinh trang cua he thong:
          do tre, luu luong, loi, chi phi, token va quality. Du lieu duoc lay truc tiep tu endpoint <code>/metrics</code>.
        </p>
        <div class="hero-stats">
          <div class="mini">
            <div class="mini-label">Refresh</div>
            <div class="mini-value">15s</div>
          </div>
          <div class="mini">
            <div class="mini-label">SLO P95</div>
            <div class="mini-value">&lt; 3000ms</div>
          </div>
          <div class="mini">
            <div class="mini-label">Budget / Day</div>
            <div class="mini-value">$2.5</div>
          </div>
          <div class="mini">
            <div class="mini-label">Quality Goal</div>
            <div class="mini-value">0.75+</div>
          </div>
        </div>
      </div>

      <aside class="hero-card meta-card">
        <div class="status-pill">
          <span class="status-dot"></span>
          Metrics Live
        </div>
        <div class="meta-list">
          <div class="meta-row"><span>App</span><strong>day13-observability-lab</strong></div>
          <div class="meta-row"><span>Source</span><strong>/metrics</strong></div>
          <div class="meta-row"><span>Range</span><strong>Current in-memory snapshot</strong></div>
          <div class="meta-row"><span>Updated</span><strong id="updated-at">Loading...</strong></div>
        </div>
        <div class="meta-badges">
          <div class="badge"><span class="badge-dot"></span>P95 SLO PASS</div>
          <div class="badge"><span class="badge-dot"></span>Budget Safe</div>
          <div class="badge"><span class="badge-dot"></span>Tracing On</div>
        </div>
      </aside>
    </section>

    <section class="grid">
      <article class="panel">
        <div>
          <div class="panel-head">
            <p class="panel-title">Latency P50 / P95 / P99</p>
            <div class="badge"><span class="badge-dot"></span>Within SLO</div>
          </div>
          <div class="panel-value" id="latency-p95">0ms</div>
          <p class="panel-caption">P95 la chi so quan trong nhat de theo doi tail latency. Muc tieu la duoi 3000ms.</p>
        </div>
        <div class="bar-group">
          <div class="bar-row"><span>P50</span><div class="bar"><span id="bar-p50"></span></div><strong id="latency-p50">0ms</strong></div>
          <div class="bar-row"><span>P95</span><div class="bar"><span id="bar-p95"></span></div><strong id="latency-p95-small">0ms</strong></div>
          <div class="bar-row"><span>P99</span><div class="bar"><span id="bar-p99"></span></div><strong id="latency-p99">0ms</strong></div>
        </div>
      </article>

      <article class="panel">
        <div>
          <p class="panel-title">Traffic</p>
          <div class="panel-value" id="traffic">0</div>
          <p class="panel-caption">Tong so request da duoc xu ly tu khi app khoi dong. Dung de doi chieu voi trace va load test.</p>
        </div>
        <div class="split">
          <div class="stat-box">
            <div class="label">Request Count</div>
            <div class="value" id="traffic-count">0</div>
          </div>
          <div class="stat-box">
            <div class="label">Traffic Health</div>
            <div class="value" id="traffic-health">Idle</div>
          </div>
        </div>
      </article>

      <article class="panel">
        <div>
          <p class="panel-title">Error Rate Breakdown</p>
          <div class="panel-value" id="error-rate">0.0%</div>
          <p class="panel-caption">Neu co loi, panel nay se cho thay ti le loi va nhom loi chinh de debug nhanh hon.</p>
        </div>
        <div id="error-breakdown">
          <div class="error-empty">Khong co loi trong batch hien tai</div>
        </div>
      </article>

      <article class="panel">
        <div>
          <div class="panel-head">
            <p class="panel-title">Cost Over Time</p>
            <div class="badge"><span class="badge-dot"></span>Under Budget</div>
          </div>
          <div class="panel-value" id="total-cost">$0.0000</div>
          <p class="panel-caption">Theo doi tong cost va average cost cua moi request de so sanh voi budget hang ngay.</p>
        </div>
        <div class="split">
          <div class="stat-box">
            <div class="label">Avg / Request</div>
            <div class="value" id="avg-cost">$0.0000</div>
          </div>
          <div class="stat-box">
            <div class="label">Budget Status</div>
            <div class="value" id="budget-status">Safe</div>
          </div>
        </div>
      </article>

      <article class="panel">
        <div>
          <p class="panel-title">Tokens In / Out</p>
          <div class="panel-value" id="tokens-out">0</div>
          <p class="panel-caption">Token output thuong cao hon token input. Chi so nay giup nhom hieu vi sao cost thay doi.</p>
        </div>
        <div class="split">
          <div class="stat-box">
            <div class="label">Tokens In</div>
            <div class="value" id="tokens-in">0</div>
          </div>
          <div class="stat-box">
            <div class="label">Tokens Out</div>
            <div class="value" id="tokens-out-small">0</div>
          </div>
        </div>
      </article>

      <article class="panel">
        <div>
          <p class="panel-title">Quality Proxy</p>
          <div class="quality-ring" id="quality-ring" style="--score: 0;">
            <div class="quality-core">
              <div>
                <strong id="quality-score">0.00</strong>
                <span>quality</span>
              </div>
            </div>
          </div>
          <p class="panel-caption">Diem quality la heuristic nhe de nhom co cai nhin nhanh xem response co dang on dinh hay khong.</p>
        </div>
      </article>
    </section>
  </main>

  <script>
    const formatMs = (value) => `${Number(value || 0).toFixed(0)}ms`;
    const formatMoney = (value) => `$${Number(value || 0).toFixed(4)}`;

    function safePercent(value, maxValue) {
      if (maxValue <= 0) return "0%";
      const ratio = Math.max(0, Math.min(100, (value / maxValue) * 100));
      return `${ratio}%`;
    }

    function renderErrors(errorBreakdown, traffic) {
      const mount = document.getElementById("error-breakdown");
      mount.innerHTML = "";

      const entries = Object.entries(errorBreakdown || {});
      const totalErrors = entries.reduce((sum, [, count]) => sum + Number(count || 0), 0);
      const errorRate = traffic > 0 ? (totalErrors / traffic) * 100 : 0;
      document.getElementById("error-rate").textContent = `${errorRate.toFixed(1)}%`;

      if (!entries.length) {
        mount.innerHTML = '<div class="error-empty">Khong co loi trong batch hien tai</div>';
        return;
      }

      entries.forEach(([name, count]) => {
        const row = document.createElement("div");
        row.className = "stat-box";
        row.innerHTML = `<div class="label">${name}</div><div class="value">${count}</div>`;
        mount.appendChild(row);
      });
    }

    function renderMetrics(data) {
      const p50 = Number(data.latency_p50 || 0);
      const p95 = Number(data.latency_p95 || 0);
      const p99 = Number(data.latency_p99 || 0);
      const maxLatencyScale = Math.max(3000, p50, p95, p99);
      const traffic = Number(data.traffic || 0);
      const avgCost = Number(data.avg_cost_usd || 0);
      const totalCost = Number(data.total_cost_usd || 0);
      const tokensIn = Number(data.tokens_in_total || 0);
      const tokensOut = Number(data.tokens_out_total || 0);
      const quality = Number(data.quality_avg || 0);

      document.getElementById("updated-at").textContent = new Date().toLocaleTimeString();

      document.getElementById("latency-p95").textContent = formatMs(p95);
      document.getElementById("latency-p50").textContent = formatMs(p50);
      document.getElementById("latency-p95-small").textContent = formatMs(p95);
      document.getElementById("latency-p99").textContent = formatMs(p99);
      document.getElementById("bar-p50").style.width = safePercent(p50, maxLatencyScale);
      document.getElementById("bar-p95").style.width = safePercent(p95, maxLatencyScale);
      document.getElementById("bar-p99").style.width = safePercent(p99, maxLatencyScale);

      document.getElementById("traffic").textContent = traffic;
      document.getElementById("traffic-count").textContent = traffic;
      document.getElementById("traffic-health").textContent = traffic > 0 ? "Active" : "Idle";

      document.getElementById("total-cost").textContent = formatMoney(totalCost);
      document.getElementById("avg-cost").textContent = formatMoney(avgCost);
      document.getElementById("budget-status").textContent = totalCost < 2.5 ? "Safe" : "Review";

      document.getElementById("tokens-in").textContent = tokensIn.toLocaleString();
      document.getElementById("tokens-out").textContent = tokensOut.toLocaleString();
      document.getElementById("tokens-out-small").textContent = tokensOut.toLocaleString();

      document.getElementById("quality-score").textContent = quality.toFixed(2);
      document.getElementById("quality-ring").style.setProperty("--score", Math.max(0, Math.min(1, quality)));

      renderErrors(data.error_breakdown, traffic);
    }

    async function refreshDashboard() {
      const response = await fetch("/metrics", { cache: "no-store" });
      const payload = await response.json();
      renderMetrics(payload);
    }

    refreshDashboard();
    setInterval(refreshDashboard, 15000);
  </script>
</body>
</html>
"""
