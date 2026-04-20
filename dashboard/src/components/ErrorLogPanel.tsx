import type { ErrorLogEntry } from '../services/errorsApi';

interface Props {
  logs: ErrorLogEntry[];
}

function getTypeColor(type: string): string {
  switch (type) {
    case '4xx': return 'text-yellow-400';
    case '5xx': return 'text-red-400';
    case 'timeout': return 'text-fuchsia-400';
    case 'other': return 'text-cyan-400';
    default: return 'text-red-400';
  }
}

export default function ErrorLogPanel({ logs }: Props) {
  return (
    <div className="rounded-lg shadow-2xl overflow-hidden border border-gray-700">
      {/* Terminal Header */}
      <div className="bg-gray-800 px-4 py-2 flex items-center gap-2 border-b border-gray-700">
        <div className="flex gap-1.5">
          <div className="w-3 h-3 rounded-full bg-red-500" />
          <div className="w-3 h-3 rounded-full bg-yellow-500" />
          <div className="w-3 h-3 rounded-full bg-green-500" />
        </div>
        <span className="text-xs text-gray-400 ml-2 font-mono">error-log — bash — 80x24</span>
      </div>

      {/* Terminal Body */}
      <div className="bg-gray-900 p-4 font-mono text-sm min-h-[200px] max-h-[400px] overflow-y-auto">
        {/* Prompt line */}
        <div className="text-green-400 mb-2">
          <span className="text-blue-400">user@dashboard</span>
          <span className="text-gray-400">:</span>
          <span className="text-blue-300">~/logs</span>
          <span className="text-gray-400">$</span>
          <span className="text-gray-300 ml-1">curl http://127.0.0.1:8000/errors</span>
        </div>

        {logs.length === 0 ? (
          <div className="text-green-500">
            <span className="text-gray-500">[</span>
            <span className="text-blue-400">INFO</span>
            <span className="text-gray-500">]</span>
            <span className="text-gray-400"> {new Date().toLocaleTimeString('vi-VN')} </span>
            <span className="text-green-400">No errors detected. All systems operational.</span>
          </div>
        ) : (
          <div className="space-y-1">
            {[...logs].reverse().map((log, idx) => (
              <div key={log.id} className="flex gap-2 hover:bg-gray-800/50 px-1 -mx-1 rounded">
                {/* Line number */}
                <span className="text-gray-600 select-none w-8 text-right shrink-0">
                  {idx + 1}
                </span>

                {/* Log content */}
                <div className="flex-1 break-all">
                  {/* Timestamp bracket */}
                  <span className="text-gray-500">[</span>
                  <span className="text-gray-400">{log.timestamp}</span>
                  <span className="text-gray-500">]</span>
                  <span className="mx-1" />

                  {/* Level badge */}
                  <span className="text-gray-500">[</span>
                  <span className={getTypeColor(log.type)}>
                    {log.type.toUpperCase()}
                  </span>
                  <span className="text-gray-500">]</span>
                  <span className="mx-1" />

                  {/* Error name */}
                  <span className="text-red-400 font-bold">{log.name}</span>
                  <span className="mx-1 text-gray-500">—</span>

                  {/* Detail */}
                  <span className="text-gray-300">{log.detail}</span>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Blinking cursor */}
        <div className="mt-2 flex items-center">
          <span className="text-green-400">➜</span>
          <span className="text-gray-400 ml-1">~</span>
          <span className="ml-1 w-2 h-4 bg-green-400 animate-pulse" />
        </div>
      </div>
    </div>
  );
}
