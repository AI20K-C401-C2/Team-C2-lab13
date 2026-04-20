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

const QUALITY_THRESHOLD = 0.85;

export default function QualityScoreChart({ data }: Props) {
  const chartData = {
    labels: data.timestamps,
    datasets: [
      {
        label: 'Quality Score',
        data: data.qualityScore,
        borderColor: '#10b981',
        backgroundColor: 'rgba(16, 185, 129, 0.15)',
        tension: 0.3,
        fill: true,
        pointRadius: 3,
      },
      {
        label: 'Min Threshold',
        data: Array(data.timestamps.length).fill(QUALITY_THRESHOLD),
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
      title: { display: true, text: 'Quality Score (0 - 1)', font: { size: 14, weight: 'bold' as const } },
      tooltip: {
        callbacks: {
          label: (ctx: any) =>
            ctx.dataset.label === 'Min Threshold'
              ? `Threshold: ${ctx.parsed.y}`
              : `Score: ${ctx.parsed.y}`,
        },
      },
    },
    scales: {
      y: {
        min: 0.6,
        max: 1.0,
        title: { display: true, text: 'score' },
      },
    },
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl shadow p-4 h-80">
      <Line data={chartData} options={options} />
    </div>
  );
}
