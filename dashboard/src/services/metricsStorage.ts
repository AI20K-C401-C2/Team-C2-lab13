import type { MetricsData, ErrorLogEntry } from './metricsApi';

const STORAGE_KEY = 'dashboard_metrics_history';
const LOGS_KEY = 'dashboard_error_logs';

export interface StoredData {
  history: MetricsData;
  savedAt: string;
}

export function saveMetrics(data: MetricsData): void {
  try {
    const payload: StoredData = {
      history: data,
      savedAt: new Date().toISOString(),
    };
    localStorage.setItem(STORAGE_KEY, JSON.stringify(payload));
  } catch {
    // localStorage might be full or unavailable
  }
}

export function loadMetrics(): MetricsData | null {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return null;
    const parsed: StoredData = JSON.parse(raw);
    return parsed.history;
  } catch {
    return null;
  }
}

export function saveErrorLogs(logs: ErrorLogEntry[]): void {
  try {
    localStorage.setItem(LOGS_KEY, JSON.stringify(logs));
  } catch {
    // ignore
  }
}

export function loadErrorLogs(): ErrorLogEntry[] {
  try {
    const raw = localStorage.getItem(LOGS_KEY);
    if (!raw) return [];
    return JSON.parse(raw);
  } catch {
    return [];
  }
}

export function clearStoredMetrics(): void {
  localStorage.removeItem(STORAGE_KEY);
  localStorage.removeItem(LOGS_KEY);
}
