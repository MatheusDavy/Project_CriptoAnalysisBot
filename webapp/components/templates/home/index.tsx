import { Chart } from "components/ui/Charts";
import { useState } from "react";

const HomeView = () => {
  const [symbol, setSymbol] = useState("BTCUSDT");
  const [timeframe, setTimeframe] = useState("1d");
  const [timerange, setTimerange] = useState(3);

  const allSymbols = ["BTCUSDT", "ETHUSDT"];
  const timeframes = ["1m", "5m", "15m", "1h", "4h", "1d", "1w"];
  const timeranges = [1, 3, 6, 12];

  return (
    <div className="grid grid-cols-[1fr_25%] items-start h-screen">
      {/* Chart */}
      <Chart symbol={symbol} timeframe={timeframe} timerange={timerange} />

      {/* Sidebar */}
      <div className="flex flex-col bg-[#0f0f0f] h-full p-4 gap-4 text-white text-sm">

        {/* Timeframe */}
        <div className="flex flex-col gap-2">
          <p className="font-semibold">Timeframe</p>
          <div className="flex flex-wrap gap-2">
            {timeframes.map((tf) => (
              <button
                key={tf}
                onClick={() => setTimeframe(tf)}
                className={`px-3 py-1 rounded-md border ${
                  timeframe === tf
                    ? "bg-blue-600 text-white border-blue-600"
                    : "bg-transparent border-gray-500 hover:bg-gray-700"
                }`}
              >
                {tf}
              </button>
            ))}
          </div>
        </div>

        {/* Timerange */}
        <div className="flex flex-col gap-2">
          <p className="font-semibold">Timerange (meses)</p>
          <div className="flex flex-wrap gap-2">
            {timeranges.map((range) => (
              <button
                key={range}
                onClick={() => setTimerange(range)}
                className={`px-3 py-1 rounded-md border ${
                  timerange === range
                    ? "bg-blue-600 text-white border-blue-600"
                    : "bg-transparent border-gray-500 hover:bg-gray-700"
                }`}
              >
                {range}m
              </button>
            ))}
          </div>
        </div>

        {/* Symbols */}
        <div className="flex flex-col gap-2 mt-6">
          <p className="font-semibold">Currency</p>
          <div className="flex flex-col gap-1">
            {allSymbols.map((sbl) => (
              <button
                key={sbl}
                onClick={() => setSymbol(sbl)}
                className={`px-3 py-2 text-left rounded-md border ${
                  symbol === sbl
                    ? "bg-blue-600 text-white border-blue-600"
                    : "bg-transparent border-gray-500 hover:bg-gray-700"
                }`}
              >
                {sbl}
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export { HomeView };
