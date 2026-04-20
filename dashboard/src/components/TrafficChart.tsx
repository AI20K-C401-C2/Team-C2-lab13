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

const TRAFFIC_THRESHOLD = 2000;

export default function TrafficChart({ data }: Props) {
  const chartData = {
    labels: data.timestamps,
    datasets: [
      {
        label: 'Requests',
        data: data.traffic,
        backgroundColor: 'rgba(59, 130, 246, 0.7)',
        borderColor: '#3b82f6',
        borderWidth: 1,
        borderRadius: 4,
      },
      {
        label: 'Threshold',
        data: Array(data.timestamps.length).fill(TRAFFIC_THRESHOLD),
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
      title: { display: true, text: 'Traffic (Request Count)', font: { size: 14, weight: 'bold' as const } },
      tooltip: {
        callbacks: {
          label: (ctx: any) =>
            ctx.dataset.label === 'Threshold'
              ? `Threshold: ${ctx.parsed.y}`
              : `Requests: ${ctx.parsed.y}`,
        },
      },
    },
    scales: {
      y: {
        title: { display: true, text: 'requests' },
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
