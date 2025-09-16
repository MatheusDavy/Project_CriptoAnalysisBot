export const indicators = [
  { label: "RSI", value: "rsi" },
  { label: "EMA", value: "ema" },
  { label: "Bollinger Bands", value: "bb" },
  { label: "MACD", value: "macd" },
  { label: "Stochastic", value: "stochastic" },
];

export const candlePatterns = [
  { label: "Flags", value: "flags" },
  { label: "Head & Shoulders", value: "hs" },
  { label: "Support/Resistance", value: "sr" },
  { label: "Fibonacci", value: "fibonacci" },
];

export const timeRanges = [
  { label: "1h", value: "1" },
  { label: "3h", value: "3" },
  { label: "6h", value: "6" },
  { label: "12h", value: "12" },
  { label: "24h", value: "24" },
  { label: "36h", value: "36" },
  { label: "48h", value: "48" },
];

export const timeFrames = [
  { label: "1m", value: "1m" },
  { label: "5m", value: "5m" },
  { label: "15m", value: "15m" },
  { label: "1h", value: "1h" },
  { label: "4h", value: "4h" },
  { label: "1d", value: "1d" },
  { label: "1w", value: "1w" },
];

export const currencies = [
  { label: "BTC/USDT", value: "BTCUSDT" },
  { label: "ETH/USDT", value: "ETHUSDT" },
  { label: "AXS/USDT", value: "AXSUSDT" },
  { label: "XRP/USDT", value: "XRPUSDT" },
  { label: "BCH/USDT", value: "BCHUSDT" },
  { label: "LINK/USDT", value: "LINKUSDT" },
  { label: "NEO/USDT", value: "NEOUSDT" },
  { label: "XLM/USDT", value: "XLMUSDT" },
  { label: "SAND/USDT", value: "SANDUSDT" },
  { label: "ATOM/USDT", value: "ATOMUSDT" },
  { label: "AAVE/USDT", value: "AAVEUSDT" },
  { label: "SUSHI/USDT", value: "SUSHIUSDT" },
  { label: "ADA/USDT", value: "ADAUSDT" },
  { label: "DOGE/USDT", value: "DOGEUSDT" },
  { label: "AVAX/USDT", value: "AVAXUSDT" },
  { label: "MANA/USDT", value: "MANAUSDT" },
  { label: "BNB/USDT", value: "BNBUSDT" },
  { label: "DOT/USDT", value: "DOTUSDT" },
  { label: "SOL/USDT", value: "SOLUSDT" },
];

export type GainTargetTypes = 'NEXT_CANDLE' | 'PERCENT'

export const gainTargets = [
  {
    label: 'Next Candles',
    value: 'NEXT_CANDLE',
  },
  {
    label: 'Percent',
    value: 'PERCENT',
  }
]

export type LossTargetTypes = 'NEXT_CANDLE' | 'PERCENT'

export const lossTargets = [
  {
    label: 'Next Candles',
    value: 'NEXT_CANDLE',
  },
  {
    label: 'Percent',
    value: 'PERCENT',
  }
]