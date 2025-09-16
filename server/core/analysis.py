from core.exchange import fetch_ohlcv
from core.signals import generate_signals
from core.shapes import generate_shapes

def generate_analysis (candles, analysis):
  shapes = generate_shapes(candles, analysis['shapes'])
  buy, sell, buy_eval, sell_eval = generate_signals(candles, analysis)

  return shapes, buy, sell, buy_eval, sell_eval
