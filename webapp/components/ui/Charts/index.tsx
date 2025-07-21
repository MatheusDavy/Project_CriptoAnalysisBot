import {
  createChart,
  type IChartApi,
  type ISeriesApi,
  type CandlestickData,
  type Time,
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
  const intervalRef = useRef<NodeJS.Timeout | null>(null);

  const { data } = useQuery({
    queryKey: ['candles', symbol, timeframe, timerange],
    queryFn: async () => {
      const res = await requestGetChartAnalysis({ symbol, timeframe, timerange });
      return res.data;
    },
  });

  useEffect(() => {
    if (!data || !chartContainerRef.current) return;

    const chart = createChart(chartContainerRef.current, {
      width: chartContainerRef.current.clientWidth,
      height: chartContainerRef.current.clientHeight,
      layout: { background: { color: '#000000' }, textColor: 'white' },
      grid: { vertLines: { color: '#242424' }, horzLines: { color: '#242424' } },
      timeScale: { timeVisible: true },
    });

    chartRef.current = chart;
    const candlestickSeries = chart.addCandlestickSeries();
    seriesRef.current = candlestickSeries;

    const formattedData = data.candles.map((candle: any) => ({
      time: Math.floor(candle.timestamp / 1000) as Time,
      open: candle.open,
      high: candle.high,
      low: candle.low,
      close: candle.close,
    }));

    candlestickSeries.setData(formattedData);

    intervalRef.current = setInterval(async () => {
      try {
        const res = await requestGetChartAnalysis({ symbol, timeframe, timerange: 1 });
        const last = res.data.candles.at(-1);
        if (!last) return;

        const newCandle: CandlestickData = {
          time: Math.floor(last.timestamp / 1000) as Time,
          open: last.open,
          high: last.high,
          low: last.low,
          close: last.close,
        };

        candlestickSeries.update(newCandle);
      } catch (e) {
        console.error('Erro ao atualizar candle:', e);
      }
    }, 5000);

    return () => {
      chart.remove();
      if (intervalRef.current) clearInterval(intervalRef.current);
    };
  }, [data]);

  return <div ref={chartContainerRef} className='w-full h-full' />;
};

export { Chart };
