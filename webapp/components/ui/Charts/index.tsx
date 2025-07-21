import {
  createChart,
  type IChartApi,
  type ISeriesApi,
  type CandlestickData,
  type SeriesMarker,
} from 'lightweight-charts';
import { useQuery } from '@tanstack/react-query';
import { useEffect, useRef } from 'react';
import { requestGetChartAnalysis } from 'services/Chart/get-analysis';

type Props = {
  symbol: string;
  timeframe: string;
  timerange: number;
};

const Chart = ({ symbol, timeframe, timerange }: Props) => {
  const chartContainerRef = useRef<HTMLDivElement>(null);
  const chartRef = useRef<IChartApi | null>(null);
  const seriesRef = useRef<ISeriesApi<'Candlestick'> | null>(null);

  const { data } = useQuery({
    queryKey: ['candles', symbol, timeframe, timerange],
    refetchInterval: 5000,
    queryFn: async () => {
      const res = await requestGetChartAnalysis({ symbol, timeframe, timerange });
      return res.data;
    },
  });

  useEffect(() => {
    if (!data || !chartContainerRef.current) return;

    const chart = createChart(chartContainerRef.current, {
      width: chartContainerRef.current?.clientWidth,
      height: chartContainerRef.current?.clientHeight,
      layout: { background: { color: '#fff' }, textColor: '#000' },
      grid: {
        vertLines: { color: '#eee' },
        horzLines: { color: '#eee' },
      },
      timeScale: {
        timeVisible: true,
      },
    });

    chartRef.current = chart;

    const candlestickSeries = chart.addCandlestickSeries();
    seriesRef.current = candlestickSeries;

    candlestickSeries.setData(
      data.candles.map((candle) => ({
        time: Math.floor(candle.timestamp / 1000),
        open: candle.open,
        high: candle.high,
        low: candle.low,
        close: candle.close,
      })) as CandlestickData[]
    );

    return () => chart.remove();
  }, [data]);

  return <div id="chartAnalysis" ref={chartContainerRef} className='h-full w-full' />;
};

export { Chart };
