interface Props {
  lastUpdated: Date | null;
  loading: boolean;
}

export default function DashboardHeader({ lastUpdated, loading }: Props) {
  return (
    <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
          System Dashboard
        </h1>
        <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
          Time range: Last 1 hour &middot; Auto refresh: 15s
        </p>
      </div>
      <div className="flex items-center gap-3">
        {loading && (
          <span className="text-xs text-blue-500 dark:text-blue-400">
            Refreshing...
          </span>
        )}
        {lastUpdated && (
          <span className="text-xs text-gray-500 dark:text-gray-400">
            Last updated: {lastUpdated.toLocaleTimeString('vi-VN')}
          </span>
        )}
      </div>
    </div>
  );
}
