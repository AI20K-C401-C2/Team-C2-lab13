import { loadMetrics, saveMetrics, loadErrorLogs, saveErrorLogs } from './metricsStorage';
import { fetchErrors } from './errorsApi';
import type { ErrorLogEntry } from './errorsApi';

export interface RawMetrics {
  traffic: number;
  latency_p50: number;
  latency_p95: number;
  latency_p99: number;
  avg_cost_usd: number;
  total_cost_usd: number;
  tokens_in_total: number;
  tokens_out_total: number;
  error_breakdown: Record<string, number>;
  quality_avg: number;
}

export interface MetricsData {
  timestamps: string[];
  latency: {
    p50: number[];
    p95: number[];
    p99: number[];
  };
  traffic: number[];
  errorRate: {
    total: number[];
    breakdown: {
      '4xx': number[];
      '5xx': number[];
      timeout: number[];
    };
  };
  cost: number[];
  tokens: {
    in: number[];
    out: number[];
  };
  qualityScore: number[];
  errorLogs: ErrorLogEntry[];
}

const API_URL = '/metrics';
const MAX_POINTS = 240; // 1 hour at 15s intervals
const MAX_ERROR_LOGS = 100;

// Load from localStorage on init
const stored = loadMetrics();
const storedLogs = loadErrorLogs();

let history: MetricsData = stored || {
  timestamps: [],
  latency: { p50: [], p95: [], p99: [] },
  traffic: [],
  errorRate: { total: [], breakdown: { '4xx': [], '5xx': [], timeout: [] } },
  cost: [],
  tokens: { in: [], out: [] },
  qualityScore: [],
  errorLogs: storedLogs || [],
};

function shiftArray<T>(arr: T[], val: T, max: number): T[] {
  const next = [...arr, val];
  if (next.length > max) next.shift();
  return next;
}

function calcErrorTotal(breakdown: Record<string, number>): number {
  return Object.values(breakdown).reduce((sum, v) => sum + (v || 0), 0);
}

export async function fetchMetrics(): Promise<MetricsData> {
  // Fetch both metrics and errors in parallel
  const [metricsRes, errors] = await Promise.all([
    fetch(API_URL, { method: 'GET' }),
    fetchErrors().catch(() => [] as ErrorLogEntry[]),
  ]);

  if (!metricsRes.ok) throw new Error(`HTTP ${metricsRes.status}`);
  const raw: RawMetrics = await metricsRes.json();

  const now = new Date();
  const timeLabel = now.toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit', second: '2-digit' });

  const errTotal = calcErrorTotal(raw.error_breakdown || {});

  // Merge new error logs from /errors endpoint
  const mergedLogs = [...history.errorLogs, ...errors];
  if (mergedLogs.length > MAX_ERROR_LOGS) {
    mergedLogs.splice(0, mergedLogs.length - MAX_ERROR_LOGS);
  }

  history = {
    timestamps: shiftArray(history.timestamps, timeLabel, MAX_POINTS),
    latency: {
      p50: shiftArray(history.latency.p50, raw.latency_p50, MAX_POINTS),
      p95: shiftArray(history.latency.p95, raw.latency_p95, MAX_POINTS),
      p99: shiftArray(history.latency.p99, raw.latency_p99, MAX_POINTS),
    },
    traffic: shiftArray(history.traffic, raw.traffic, MAX_POINTS),
    errorRate: {
      total: shiftArray(history.errorRate.total, errTotal, MAX_POINTS),
      breakdown: {
        '4xx': shiftArray(history.errorRate.breakdown['4xx'], raw.error_breakdown?.['4xx'] || 0, MAX_POINTS),
        '5xx': shiftArray(history.errorRate.breakdown['5xx'], raw.error_breakdown?.['5xx'] || 0, MAX_POINTS),
        timeout: shiftArray(history.errorRate.breakdown.timeout, raw.error_breakdown?.timeout || 0, MAX_POINTS),
      },
    },
    cost: shiftArray(history.cost, raw.total_cost_usd, MAX_POINTS),
    tokens: {
      in: shiftArray(history.tokens.in, raw.tokens_in_total, MAX_POINTS),
      out: shiftArray(history.tokens.out, raw.tokens_out_total, MAX_POINTS),
    },
    qualityScore: shiftArray(history.qualityScore, raw.quality_avg, MAX_POINTS),
    errorLogs: mergedLogs,
  };

  // Save to localStorage after each fetch
  saveMetrics(history);
  saveErrorLogs(mergedLogs);

  return history;
}

export type { ErrorLogEntry };
