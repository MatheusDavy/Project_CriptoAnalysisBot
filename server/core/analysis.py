import pandas as pd
import pandas_ta as ta
import logging

def apply_technical_analysis(df):
    if df.empty:
        return df

    for col in ['open', 'high', 'low', 'close', 'volume']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df.dropna(subset=['open', 'high', 'low', 'close', 'volume'], inplace=True)

    df.ta.sma(length=20, append=True)
    df.ta.ema(length=50, append=True)
    df.ta.rsi(length=14, append=True)
    df.ta.macd(append=True)
    df.ta.bbands(append=True)

    logging.info("Applied technical analysis indicators.")
    return df