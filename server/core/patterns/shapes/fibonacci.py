import pandas as pd
from typing import List, Dict, Any

FIB_LEVELS = [0.0, 0.236, 0.382, 0.5, 0.618, 0.786, 1.0]
ACTIVE_LEVELS = [0.382, 0.5]

def generate_fibonacci_signals(df: pd.DataFrame, lookback_period: int = 100) -> pd.DataFrame:
    """
    Marca sinais de compra/venda nos níveis de Fibonacci 0.5 e 0.618.

    Args:
        df (pd.DataFrame): DataFrame OHLC com índice datetime
        lookback_period (int): Número de candles usados para o cálculo do range Fibonacci

    Returns:
        pd.DataFrame: DataFrame com colunas 'fibonacci_buy' e 'fibonacci_sell'
    """
    df = df.copy()
    df['fibonacci_buy'] = False
    df['fibonacci_sell'] = False

    df['high_max'] = df['high'].rolling(window=lookback_period).max()
    df['low_min'] = df['low'].rolling(window=lookback_period).min()

    level_indices = [FIB_LEVELS.index(lvl) for lvl in ACTIVE_LEVELS]
    order_array = [False] * len(FIB_LEVELS)

    for i in range(lookback_period, len(df)):
        high = df['high_max'].iloc[i]
        low = df['low_min'].iloc[i]

        if pd.isna(high) or pd.isna(low):
            continue

        diff = high - low
        fib_prices = [low + level * diff for level in FIB_LEVELS]

        current_low = df['low'].iloc[i]
        current_high = df['high'].iloc[i]

        for j in level_indices:
            # Sinal de compra: preço atual tocando o nível ativo (suporte)
            if current_low <= fib_prices[j] and not order_array[j]:
                df.at[df.index[i], 'fibonacci_buy'] = True
                order_array[j] = True

            # Sinal de venda: preço atual tocando nível acima (resistência)
            if j < len(FIB_LEVELS) - 1:
                if current_high >= fib_prices[j + 1] and order_array[j]:
                    df.at[df.index[i], 'fibonacci_sell'] = True
                    order_array[j] = False

    return df

def calculate_fibonacci_lines(df: pd.DataFrame, lookback_period: int = 100) -> Dict[float, List[Dict[str, Any]]]:
    """
    Recebe um DataFrame com candles (com índice datetime ou timestamp em segundos)
    e retorna um dicionário onde a chave é o nível Fibonacci e o valor é a lista
    de pontos para plotar a linha horizontal no lightweight-charts via addLineSeries.

    Args:
        df (pd.DataFrame): DataFrame com colunas 'high', 'low' e índice datetime ou int timestamp
        lookback_period (int): número de candles para calcular o range
        fib_levels (List[float]): níveis Fibonacci desejados

    Returns:
        Dict[float, List[Dict]]: dicionário {nivel: [{time, value}, ...], ...}
    """

    df = df.copy()
    df['high_max'] = df['high'].rolling(window=lookback_period).max()
    df['low_min'] = df['low'].rolling(window=lookback_period).min()

    # Pega o último valor válido para high_max e low_min
    high = df['high_max'].dropna().iloc[-1]
    low = df['low_min'].dropna().iloc[-1]
    diff = high - low

    fib_prices = [low + level * diff for level in FIB_LEVELS]

    # Pega a lista de timestamps para o eixo x
    if isinstance(df.index[0], pd.Timestamp):
        # Converter para int timestamp em segundos para JS
        times = [int(ts.timestamp()) for ts in df.index]
    else:
        times = df.index.tolist()

    # Monta os pontos para cada linha (preço constante, tempo variável)
    lines_data = {}
    for level, price in zip(FIB_LEVELS, fib_prices):
        points = [{"time": t, "value": price} for t in times]
        lines_data[level] = points

    return lines_data
