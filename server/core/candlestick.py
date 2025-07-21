import pandas as pd

def engulfing(df):
    df['engulfing'] = 0
    for i in range(1, len(df)):
        prev = df.iloc[i-1]
        curr = df.iloc[i]
        
        # Bullish engulfing
        if (prev['close'] < prev['open'] and 
            curr['open'] < curr['close'] and 
            curr['open'] < prev['close'] and 
            curr['close'] > prev['open']):
            df.at[df.index[i], 'engulfing'] = 1
            
        # Bearish engulfing
        elif (prev['close'] > prev['open'] and 
              curr['open'] > curr['close'] and 
              curr['open'] > prev['close'] and 
              curr['close'] < prev['open']):
            df.at[df.index[i], 'engulfing'] = -1
    return df

def hammer(df):
    df['hammer'] = 0
    for i in range(len(df)):
        curr = df.iloc[i]
        body = abs(curr['close'] - curr['open'])
        lower_wick = curr['open'] - curr['low'] if curr['close'] > curr['open'] else curr['close'] - curr['low']
        
        if lower_wick > 2 * body and (curr['high'] - curr['close']) < body:
            df.at[df.index[i], 'hammer'] = 1
    return df

def doji(df):
    df['doji'] = 0
    for i in range(len(df)):
        curr = df.iloc[i]
        body = abs(curr['close'] - curr['open'])
        total_range = curr['high'] - curr['low']
        
        if body < 0.1 * total_range:
            df.at[df.index[i], 'doji'] = 1
    return df

def detect_candle_patterns(df):
    """
    Função principal que detecta todos os padrões de candlestick
    e retorna o DataFrame com colunas de sinais de compra/venda
    
    Parâmetros:
    df -- DataFrame com colunas: 'open', 'high', 'low', 'close'
    
    Retorna:
    DataFrame com colunas adicionais de padrões e sinais
    """
    # Aplica todos os padrões
    df = engulfing(df)
    df = hammer(df)
    df = doji(df)
    
    # Inicializa colunas de decisão
    df['pattern_buy'] = False
    df['pattern_sell'] = False
    
    # Define regras de compra/venda baseadas nos padrões
    df['pattern_buy'] |= (df['engulfing'] == 1) | (df['hammer'] == 1)
    df['pattern_sell'] |= (df['engulfing'] == -1)
    
    # Doji pode ser usado como confirmação (opcional)
    # df['pattern_confirm'] = df['doji'] == 1
    
    return df