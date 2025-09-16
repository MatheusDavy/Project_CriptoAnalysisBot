import pandas as pd

def evaluate_signals(df, signals, direction='buy', future_candles=10):
    hits = 0
    misses = 0
    total = len(signals)

    for ts in signals:
        entry_time = pd.to_datetime(ts, unit='s')
        idx = df.index.get_indexer([entry_time], method='nearest')[0]

        if idx + future_candles >= len(df):
            # Evita erro de index
            total -= 1
            continue

        entry_open = df.iloc[idx]['open']
        exit_close = df.iloc[idx + future_candles]['close']

        if direction == 'buy':
            success = exit_close > entry_open
        elif direction == 'sell':
            success = exit_close < entry_open
        else:
            raise ValueError("Direction must be 'buy' or 'sell'")

        if success:
            hits += 1
        else:
            misses += 1

    assertiveness = (hits / total * 100) if total > 0 else 0

    return {
        'total': total,
        'hits': hits,
        'misses': misses,
        'assertiveness': round(assertiveness, 2)
    }
