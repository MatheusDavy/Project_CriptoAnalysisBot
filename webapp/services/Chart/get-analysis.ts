import type { AxiosResponse } from "axios";
import { api } from "services/api";

type Props = {
  symbol: string;
  timeframe: string;
  timerange: number;
};

type CandlesTypes = {
  timestamp: number
  open: number;
  high: number;
  low: number;
  close: number;
};

type ShapesTypes = {
  sr: number[],
  flag: {
    points: number[]
    type: string
  }[]
  hs: {
    neckline: number[]
    points: number[]
    type: string
  }[]
}

type Response = {
  candles: CandlesTypes[];
  buy: number[]
  sell: number[]
  shapes: ShapesTypes
};

const requestGetChartAnalysis = async (props: Props) : Promise<AxiosResponse<Response>> => {
  return api.get("/analysis", {
    params: props,
  });
};

export { requestGetChartAnalysis };
