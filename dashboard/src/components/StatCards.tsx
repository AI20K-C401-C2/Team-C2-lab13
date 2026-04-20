import type { MetricsData } from '../services/metricsApi';

interface Props {
  data: MetricsData;
}

export default function StatCards({ data }: Props) {
  const latestIdx = data.timestamps.length - 1;

  const stats = [
    {
      label: 'P95 Latency',
      value: `${data.latency.p95[latestIdx]} ms`,
      status: data.latency.p95[latestIdx] > 300 ? 'warning' : 'good',
    },
    {
      label: 'Requests',
      value: data.traffic[latestIdx].toLocaleString(),
      status: 'good' as const,
    },
    {
      label: 'Error Rate',
      value: `${data.errorRate.total[latestIdx]}%`,
      status: data.errorRate.total[latestIdx] > 2 ? 'warning' : 'good',
    },
    {
      label: 'Quality Score',
      value: `${data.qualityScore[latestIdx]}`,
      status: data.qualityScore[latestIdx] < 0.85 ? 'warning' : 'good',
    },
  ];

  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
      {stats.map((s) => (
        <div
          key={s.label}
          className="bg-white dark:bg-gray-800 rounded-xl shadow p-4"
        >
          <p className="text-xs text-gray-500 dark:text-gray-400 uppercase tracking-wide">
            {s.label}
          </p>
          <p
            className={`text-xl font-bold mt-1 ${
              s.status === 'warning'
                ? 'text-red-500'
                : 'text-gray-900 dark:text-white'
            }`}
          >
            {s.value}
          </p>
        </div>
      ))}
    </div>
  );
}
