import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';
import type { MetricsData } from '../services/metricsApi';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

interface Props {
  data: MetricsData;
}

const ERROR_THRESHOLD = 2;

export default function ErrorRateChart({ data }: Props) {
  const chartData = {
    labels: data.timestamps,
    datasets: [
      {
        label: '4xx Errors',
        data: data.errorRate.breakdown['4xx'],
        backgroundColor: 'rgba(245, 158, 11, 0.8)',
        borderRadius: 2,
      },
      {
        label: '5xx Errors',
        data: data.errorRate.breakdown['5xx'],
        backgroundColor: 'rgba(239, 68, 68, 0.8)',
        borderRadius: 2,
      },
      {
        label: 'Timeouts',
        data: data.errorRate.breakdown.timeout,
        backgroundColor: 'rgba(107, 114, 128, 0.8)',
        borderRadius: 2,
      },
      {
        label: 'SLO Threshold',
        data: Array(data.timestamps.length).fill(ERROR_THRESHOLD),
        type: 'line' as const,
        borderColor: '#ef4444',
        borderDash: [6, 4],
        borderWidth: 2,
        pointRadius: 0,
        fill: false,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { position: 'top' as const, labels: { boxWidth: 12, font: { size: 11 } } },
      title: { display: true, text: 'Error Rate Breakdown', font: { size: 14, weight: 'bold' as const } },
      tooltip: {
        callbacks: {
          label: (ctx: any) =>
            ctx.dataset.label === 'SLO Threshold'
              ? `SLO: ${ctx.parsed.y}%`
              : `${ctx.dataset.label}: ${ctx.parsed.y}%`,
        },
      },
    },
    scales: {
      x: { stacked: true },
      y: {
        stacked: true,
        title: { display: true, text: '%' },
        beginAtZero: true,
      },
    },
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl shadow p-4 h-80">
      <Bar data={chartData as any} options={options as any} />
    </div>
  );
}
