import { Chart } from "components/ui/Charts";
import { useState } from "react";

const HomeView = () => {
  const [symbol, setSymbol] = useState('BTCUSDT');
  const [timeframe, setTimeframe] = useState('1d');
  const [timerange, setTimerange] = useState(3);

  return (
    <div className="grid grid-cols-[1fr_25%] h-screen">
      {/* Chart */}
      <Chart
        symbol={symbol}
        timeframe={timeframe}
        timerange={timerange}
      />
      <div className="flex items-center gap-4">
        {/* Timeframe */}
        <div className="flex flex-col">
          <label htmlFor="timeframe" className="text-sm font-medium text-gray-700">
            Timeframe
          </label>
          <select
            id="timeframe"
            className="border border-gray-300 rounded-md px-3 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={timeframe}
            onChange={(e) => setTimeframe(e.target.value)}
          >
            {['1m', '5m', '15m', '1h', '4h', '1d', '1w'].map((tf) => (
              <option key={tf} value={tf}>{tf}</option>
            ))}
          </select>
        </div>

        {/* Timerange */}
        <div className="flex flex-col">
          <label htmlFor="timerange" className="text-sm font-medium text-gray-700">
            Timerange (meses)
          </label>
          <select
            id="timerange"
            className="border border-gray-300 rounded-md px-3 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={timerange}
            onChange={(e) => setTimerange(Number(e.target.value))}
          >
            {[1, 3, 6, 12].map((range) => (
              <option key={range} value={range}>{range} mês{range > 1 ? 'es' : ''}</option>
            ))}
          </select>
        </div>
      </div>
    </div>
  );
};

export { HomeView };
