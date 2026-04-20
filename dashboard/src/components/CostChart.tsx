import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import type { MetricsData } from '../services/metricsApi';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler);

interface Props {
  data: MetricsData;
}

const COST_BUDGET = 2.5;

export default function CostChart({ data }: Props) {
  const chartData = {
    labels: data.timestamps,
    datasets: [
      {
        label: 'Cost',
        data: data.cost,
        borderColor: '#8b5cf6',
        backgroundColor: 'rgba(139, 92, 246, 0.15)',
        tension: 0.3,
        fill: true,
        pointRadius: 3,
      },
      {
        label: 'Budget',
        data: Array(data.timestamps.length).fill(COST_BUDGET),
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
      title: { display: true, text: 'Cost Over Time', font: { size: 14, weight: 'bold' as const } },
      tooltip: {
        callbacks: {
          label: (ctx: any) =>
            ctx.dataset.label === 'Budget'
              ? `Budget: $${ctx.parsed.y}`
              : `Cost: $${ctx.parsed.y}`,
        },
      },
    },
    scales: {
      y: {
        title: { display: true, text: 'USD' },
        beginAtZero: true,
      },
    },
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl shadow p-4 h-80">
      <Line data={chartData} options={options} />
    </div>
  );
}
