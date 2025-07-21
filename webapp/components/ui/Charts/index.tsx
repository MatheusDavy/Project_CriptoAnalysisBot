import {
  createChart,
  LineStyle,
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

  const generateSrShapes = (candlestickSeries: ISeriesApi<'Candlestick'>) => {
    const sr = data?.shapes.sr;
    sr?.forEach((price) => {
      candlestickSeries.createPriceLine({
        price,
        color: '#0000ff57',
        lineWidth: 1,
        axisLabelVisible: true,
        title: 'SR',
      });
    })
  }

  const generateBuySellMarkers = (candlestickSeries: ISeriesApi<'Candlestick'>) => {
    const buyMarkers = data?.buy.map((timestamp: number) => ({
      time: timestamp as Time,
      position: 'belowBar' as const,
      color: 'green',
      shape: 'arrowUp' as const,
      text: 'Buy',
    })) || []

    const sellMarkers = data?.sell.map((timestamp: number) => ({
      time: timestamp as Time,
      position: 'aboveBar' as const,
      color: 'red',
      shape: 'arrowDown' as const,
      text: 'Sell',
    })) || []

    const allMarkers = [...buyMarkers, ...sellMarkers].sort((a: any, b: any) => a.time - b.time);
    candlestickSeries.setMarkers(allMarkers);
  }

  const generatePatternsShapes = (chart: IChartApi) => {
    if (!data?.shapes?.flag) return;

    const shapes = [...data.shapes.flag]

    // 1. Filtrar e validar os dados
    const validFlags = shapes?.filter(flag => {
      return (
        flag.points &&
        flag.points.length === 4 &&
        !flag.points.some(isNaN) &&
        flag.points[0] > 0 &&
        flag.points[2] > 0
      );
    });

    // 2. Ordenar por timestamp
    validFlags.sort((a, b) => a.points[0] - b.points[0]);

    // 3. Adicionar as linhas
    validFlags.forEach(flag => {
      try {
        const [time1, price1, time2, price2] = flag.points;

        // Converter timestamp se necessário (millis → segundos)
        const convertTime = (t: number) => {
          return t > 1e12 ? Math.floor(t / 1000) : t;
        };

        const lineSeries = chart.addLineSeries({
          color: flag.type.includes('bull') ? 'rgba(0, 255, 0, 0.7)' : 'rgba(255, 0, 0, 0.7)',
          lineWidth: 2,
          lineStyle: LineStyle.Solid,
        });

        lineSeries.setData([
          { time: convertTime(time1) as Time, value: price1 },
          { time: convertTime(time2) as Time, value: price2 }
        ]);

      } catch (error) {
        console.error('Erro ao criar linha:', flag, error);
      }
    });
  };

  const generateHsShapes = (chart: IChartApi) => {
    if (!data?.shapes?.hs) return;

    data.shapes.hs.forEach(pattern => {
      try {
        // Adiciona linhas do padrão HS
        const patternLineSeries = chart.addLineSeries({
          color: pattern.type === 'head_shoulders' ? 'rgb(255, 152, 152)' : 'rgb(170, 255, 170)',
          lineWidth: 2,
          lineStyle: LineStyle.Solid,
        });

        // Converte os pontos para o formato do Lightweight Charts
        const patternPoints = pattern.points.map((point: any) => ({
          time: (point[0] > 1e12 ? Math.floor(point[0] / 1000) : point[0]) as Time,
          value: point[1]
        }));

        patternLineSeries.setData(patternPoints);

        // Adiciona linha do pescoço
        const necklineSeries = chart.addLineSeries({
          color: 'rgba(255, 255, 0, 0.7)',
          lineWidth: 1,
          lineStyle: LineStyle.Dashed,
        });

        const necklinePoints = pattern.neckline.map((point: any) => ({
          time: (point[0] > 1e12 ? Math.floor(point[0] / 1000) : point[0]) as Time,
          value: point[1]
        }));

        necklineSeries.setData(necklinePoints);

      } catch (error) {
        console.error('Error creating HS pattern lines:', error);
      }
    });
  };

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

    generateSrShapes(candlestickSeries);
    generateBuySellMarkers(candlestickSeries);
    generatePatternsShapes(chart);
    generateHsShapes(chart);

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
