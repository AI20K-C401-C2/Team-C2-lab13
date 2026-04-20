import { useMetrics } from './hooks/useMetrics';
import DashboardHeader from './components/DashboardHeader';
import StatCards from './components/StatCards';
import LatencyChart from './components/LatencyChart';
import TrafficChart from './components/TrafficChart';
import ErrorRateChart from './components/ErrorRateChart';
import CostChart from './components/CostChart';
import TokensChart from './components/TokensChart';
import QualityScoreChart from './components/QualityScoreChart';

function App() {
  const { data, loading, error, lastUpdated } = useMetrics();

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 p-4 sm:p-6">
      <div className="max-w-7xl mx-auto">
        <DashboardHeader
          lastUpdated={lastUpdated}
          loading={loading}
        />

        {error && (
          <div className="mb-6 p-4 bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-300 rounded-xl">
            Error: {error}
          </div>
        )}

        {data && (
          <>
            <StatCards data={data} />

            <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
              <LatencyChart data={data} />
              <TrafficChart data={data} />
              <ErrorRateChart data={data} />
              <CostChart data={data} />
              <TokensChart data={data} />
              <QualityScoreChart data={data} />
            </div>
          </>
        )}

        {!data && !error && loading && (
          <div className="flex items-center justify-center h-64">
            <div className="text-gray-500 dark:text-gray-400">Loading metrics...</div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
