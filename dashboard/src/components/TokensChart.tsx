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

export default function TokensChart({ data }: Props) {
  const chartData = {
    labels: data.timestamps,
    datasets: [
      {
        label: 'Tokens In',
        data: data.tokens.in,
        backgroundColor: 'rgba(14, 165, 233, 0.8)',
        borderRadius: 2,
      },
      {
        label: 'Tokens Out',
        data: data.tokens.out,
        backgroundColor: 'rgba(168, 85, 247, 0.8)',
        borderRadius: 2,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { position: 'top' as const, labels: { boxWidth: 12, font: { size: 11 } } },
      title: { display: true, text: 'Tokens In / Out', font: { size: 14, weight: 'bold' as const } },
      tooltip: {
        callbacks: {
          label: (ctx: any) => `${ctx.dataset.label}: ${Number(ctx.parsed.y).toLocaleString()}`,
        },
      },
    },
    scales: {
      x: { stacked: true },
      y: {
        stacked: true,
        title: { display: true, text: 'tokens' },
        beginAtZero: true,
      },
    },
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl shadow p-4 h-80">
      <Bar data={chartData} options={options} />
    </div>
  );
}
