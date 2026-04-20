export interface RawErrorEntry {
  timestamp?: string;
  name?: string;
  type?: string;
  detail?: string;
  message?: string;
  error_type?: string;
  category?: string;
  description?: string;
  [key: string]: unknown;
}

export interface ErrorLogEntry {
  id: string;
  timestamp: string;
  name: string;
  type: string;
  detail: string;
}

const ERRORS_API_URL = '/errors';

function normalizeError(raw: RawErrorEntry, fallbackTime: string): ErrorLogEntry {
  const timestamp = raw.timestamp || fallbackTime;
  const type = raw.type || raw.error_type || raw.category || 'unknown';
  const name = raw.name || raw.message || 'Error';
  const detail = raw.detail || raw.description || JSON.stringify(raw);

  return {
    id: `${timestamp}-${type}-${Math.random().toString(36).slice(2, 8)}`,
    timestamp,
    name,
    type,
    detail,
  };
}

export async function fetchErrors(): Promise<ErrorLogEntry[]> {
  const res = await fetch(ERRORS_API_URL, { method: 'GET' });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);

  const raw = await res.json();
  const now = new Date().toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit', second: '2-digit' });

  // Handle different response formats
  if (Array.isArray(raw)) {
    return raw.map((item) => normalizeError(item as RawErrorEntry, now));
  }

  if (raw.errors && Array.isArray(raw.errors)) {
    return raw.errors.map((item: RawErrorEntry) => normalizeError(item, now));
  }

  if (raw.error_logs && Array.isArray(raw.error_logs)) {
    return raw.error_logs.map((item: RawErrorEntry) => normalizeError(item, now));
  }

  // Single error object
  if (typeof raw === 'object' && raw !== null) {
    return [normalizeError(raw as RawErrorEntry, now)];
  }

  return [];
}
