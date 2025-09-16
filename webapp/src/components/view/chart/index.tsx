// import { Analysis } from "components/ui/Analysis";
// import { Chart } from "components/material/Charts";
import { Checkbox } from "components/ui/checkbox";
import { Input } from "components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "components/ui/select";

// import { useChartContext } from "context/ChartContext";
// import { allSymbols } from "utils/symbols";

const ChartView = () => {
  // const {
  //   tabs,
  //   onSetTabs,
  //   timeframe,
  //   onSetTimeframe,
  //   timerange,
  //   onSetTimerange,
  //   indicators,
  //   onToggleIndicator,
  //   shapes,
  //   onToggleShape,
  //   individuals,
  //   onToggleIndividual,
  //   confluence,
  //   onSetConfluence,
  // } = useChartContext();

  const timeframes = ["1m", "5m", "15m", "1h", "4h", "1d", "1w"];
  const timeranges = [1, 3, 6, 12, 24, 36, 48];
  const allIndicators = ["rsi", "ema", "bb", "macd", "stochastic"];
  const allShapes = ["flags", "hs", "sr", "fibonacci"];

  return (
    <div className="grid grid-cols-[1fr_25%] items-start h-screen overflow-hidden">
      {/* Chart */}
      {/* <div className="w-full max-w-full h-full bg-black">
        <div className="w-full h-full relative">
          {tabs?.opens?.map((symbol) => (
            <Chart symbol={symbol} />
          ))}
        </div>
      </div> */}

      {/* Sidebar */}
      {/* <div className="border-l-2 border-gray-700 w-full grid grid-rows-[auto_auto_1fr] bg-[#0f0f0f] max-h-screen h-full gap-4 text-white text-sm overflow-auto">
        <div className="flex flex-col gap-2">
          <p className="font-semibold px-6 py-2">Timeframe</p>
          <div className="w-full px-4">
            <Select value={timeframe} onValueChange={onSetTimeframe}>
              <SelectTrigger className="w-full ">
                <SelectValue placeholder="Selecione o timeframe" />
              </SelectTrigger>
              <SelectContent>
                {timeframes.map((tf) => (
                  <SelectItem key={tf} value={tf}>
                    {tf}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </div>

        <hr className="w-full border-[#2e2e2e]" />

        <div className="flex flex-col gap-2">
          <p className="font-semibold px-6 py-2">Timerange (meses)</p>
          <div className="w-full px-4">
            <Select
              value={String(timerange)}
              onValueChange={(v) => onSetTimerange(Number(v))}
            >
              <SelectTrigger className="w-full">
                <SelectValue placeholder="Selecione o timerange" />
              </SelectTrigger>
              <SelectContent>
                {timeranges.map((range) => (
                  <SelectItem key={range} value={String(range)}>
                    {range}m
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </div>

        <hr className="w-full border-[#2e2e2e]" />

        <div className="flex flex-col gap-2">
          <p className="font-semibold px-6 py-2">Indicadores</p>
          <div className="flex flex-wrap gap-4 px-4">
            {allIndicators.map((idc) => (
              <div key={idc} className="flex items-center gap-2">
                <Checkbox
                  id={`indicator-${idc}`}
                  checked={indicators.includes(idc)}
                  onCheckedChange={() => onToggleIndicator(idc)}
                />
                <label htmlFor={`indicator-${idc}`}>{idc}</label>
              </div>
            ))}
          </div>
        </div>

        <div className="flex flex-col gap-2">
          <p className="font-semibold px-6 py-2">Figuras Gráficas</p>
          <div className="flex flex-wrap gap-4 px-4">
            {allShapes.map((shape) => (
              <div key={shape} className="flex items-center gap-2">
                <Checkbox
                  id={`shape-${shape}`}
                  checked={shapes.includes(shape)}
                  onCheckedChange={() => onToggleShape(shape)}
                />
                <label htmlFor={`shape-${shape}`}>{shape}</label>
              </div>
            ))}
          </div>
        </div>

        <div className="flex flex-col gap-2">
          <p className="font-semibold px-6 py-2">Individuais</p>
          <div className="flex flex-wrap gap-4">
            {Object.keys(individuals).map((key) => (
              <div key={key} className="flex items-center gap-2 px-4">
                <Checkbox
                  id={`individual-${key}`}
                  checked={individuals[key]}
                  onCheckedChange={() => onToggleIndividual(key as any)}
                />
                <label htmlFor={`individual-${key}`}>{key}</label>
              </div>
            ))}
          </div>
        </div>

        <hr className="w-full border-[#2e2e2e]" />

        <div className="flex flex-col">
          <p className="font-semibold px-6 py-2">Confluências</p>
          <div className="flex flex-col gap-4 px-4">
            {Object.entries(confluence).map(([key, value]) => (
              <div key={key} className="flex flex-col gap-2">
                <label>{key}</label>
                <Input
                  type="number"
                  value={value}
                  onChange={(e) =>
                    onSetConfluence(key as any, Number(e.target.value))
                  }
                  className={`px-2 py-1 border ${
                    key === "sell" ? "border-red-500" : "border-green-500"
                  }`}
                />
              </div>
            ))}
          </div>
        </div>

        <hr className="w-full border-[#2e2e2e]" />

      <div className="flex flex-col mt-6 h-full">
          <p className="font-semibold px-6 py-2 border-b-[1px] border-[#2e2e2e]">
            Símbolos
          </p>
          <div className="flex flex-col">
            {allSymbols.map((sbl) => (
              <button
                key={sbl}
                onClick={() => {
                  onSetTabs({
                    active: sbl,
                    opens: tabs?.opens!,
                  });
                }}
                className={`
                  px-4 py-2 text-left cursor-pointer border-b-[1px] border-[#2e2e2e]
                  ${tabs?.active === sbl ? "bg-gray-700" : "bg-transparent "}
                `}
              >
                {sbl}
              </button>
            ))}
          </div>
        </div>
      </div> */}
    </div>
  );
};

export { ChartView };
