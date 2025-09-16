import pandas as pd

def bollinger_bands(df, window=20, num_std=2):
    """
    Calcula as Bandas de Bollinger e detecta sinais de compra e venda
    baseados na interação do preço com as bandas.

    Parâmetros:
        df (pd.DataFrame): DataFrame com colunas 'close', 'open', 'high', 'low'.
        window (int): Período para o cálculo da Média Móvel Simples (SMA).
        num_std (int): Número de desvios padrão para as bandas superior e inferior.

    Retorna:
        pd.DataFrame: O DataFrame original com as colunas
                      'BB_Middle', 'BB_Upper', 'BB_Lower',
                      'bb_buy', e 'bb_sell'.
    """
    # 1. Cálculo das Bandas de Bollinger
    df['BB_Middle'] = df['close'].rolling(window=window, min_periods=1).mean()
    df['BB_Std'] = df['close'].rolling(window=window, min_periods=1).std()
    df['BB_Upper'] = df['BB_Middle'] + num_std * df['BB_Std']
    df['BB_Lower'] = df['BB_Middle'] - num_std * df['BB_Std']

    # 2. Inicialização das colunas de sinal
    df['bb_buy'] = 0
    df['bb_sell'] = 0

    # 3. Detecção dos Sinais de Bollinger Bands
    # Iteramos a partir do segundo elemento para ter acesso ao candle anterior
    for i in range(1, len(df)):
        current_row = df.iloc[i]
        prev_row = df.iloc[i-1]

        # Garantir que os valores das bandas não são NaN (podem ser no início do DataFrame)
        if pd.isna(current_row['BB_Upper']) or pd.isna(current_row['BB_Lower']):
            continue

        # --- Sinais de COMPRA (bb_buy) ---
        # Priorizamos o preenchimento com 1 e não sobrescrevemos se já for 1

        # 1. Preço toca ou cruza a banda inferior (Oversold)
        # Se o fechamento atual está na ou abaixo da banda inferior
        if current_row['close'] <= current_row['BB_Lower']:
            df.at[df.index[i], 'bb_buy'] = 1

        # 2. Reversão da Banda Inferior (Bollinger Bounce de COMPRA)
        # Se o candle anterior estava fechando na ou abaixo da banda inferior,
        # e o candle atual fecha acima dela, indicando uma possível reversão de alta.
        elif prev_row['close'] <= prev_row['BB_Lower'] and current_row['close'] > current_row['BB_Lower']:
            df.at[df.index[i], 'bb_buy'] = 1
        
        # 3. Fechamento acima da banda média (confirmação de força de alta)
        # Se o preço veio de baixo da banda média e a cruza para cima
        elif prev_row['close'] < prev_row['BB_Middle'] and current_row['close'] > current_row['BB_Middle']:
            df.at[df.index[i], 'bb_buy'] = 1
        
        # --- Sinais de VENDA (bb_sell) ---
        # Priorizamos o preenchimento com 1 e não sobrescrevemos se já for 1

        # 1. Preço toca ou cruza a banda superior (Overbought)
        # Se o fechamento atual está na ou acima da banda superior
        if current_row['close'] >= current_row['BB_Upper']:
            df.at[df.index[i], 'bb_sell'] = 1

        # 2. Reversão da Banda Superior (Bollinger Bounce de VENDA)
        # Se o candle anterior estava fechando na ou acima da banda superior,
        # e o candle atual fecha abaixo dela, indicando uma possível reversão de baixa.
        elif prev_row['close'] >= prev_row['BB_Upper'] and current_row['close'] < current_row['BB_Upper']:
            df.at[df.index[i], 'bb_sell'] = 1

        # 3. Fechamento abaixo da banda média (confirmação de força de baixa)
        # Se o preço veio de cima da banda média e a cruza para baixo
        elif prev_row['close'] > prev_row['BB_Middle'] and current_row['close'] < current_row['BB_Middle']:
            df.at[df.index[i], 'bb_sell'] = 1

    return df

def ema_crossover(df, short=9, long=21):
    df['ema_short'] = df['close'].ewm(span=short).mean()
    df['ema_long'] = df['close'].ewm(span=long).mean()
    df['ema_buy'] = (df['ema_short'] > df['ema_long']) & (df['ema_short'].shift(1) <= df['ema_long'].shift(1))
    df['ema_sell'] = (df['ema_short'] < df['ema_long']) & (df['ema_short'].shift(1) >= df['ema_long'].shift(1))
    return df

def rsi_signal(df, period=14):
    delta = df['close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    rs = avg_gain / (avg_loss + 1e-9)
    df['rsi'] = 100 - (100 / (1 + rs))
    df['rsi_buy'] = df['rsi'] < 30
    df['rsi_sell'] = df['rsi'] > 70
    return df

def macd(df, fast=12, slow=26, signal=9):
    df = df.copy()
    ema_fast = df['close'].ewm(span=fast, adjust=False).mean()
    ema_slow = df['close'].ewm(span=slow, adjust=False).mean()
    df['macd'] = ema_fast - ema_slow
    df['macd_signal'] = df['macd'].ewm(span=signal, adjust=False).mean()
    df['macd_buy'] = (df['macd'] > df['macd_signal']) & (df['macd'].shift(1) <= df['macd_signal'].shift(1))
    df['macd_sell'] = (df['macd'] < df['macd_signal']) & (df['macd'].shift(1) >= df['macd_signal'].shift(1))
    return df

def stochastic(df, k_period=14, d_period=3):
    df = df.copy()
    low_min = df['low'].rolling(k_period).min()
    high_max = df['high'].rolling(k_period).max()
    df['stoch_k'] = 100 * ((df['close'] - low_min) / (high_max - low_min + 1e-9))
    df['stoch_d'] = df['stoch_k'].rolling(d_period).mean()
    df['stoch_buy'] = (df['stoch_k'] < 20) & (df['stoch_k'] > df['stoch_d'])
    df['stoch_sell'] = (df['stoch_k'] > 80) & (df['stoch_k'] < df['stoch_d'])
    return df