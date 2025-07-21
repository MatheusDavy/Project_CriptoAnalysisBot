import os
import re

def calculate_limit(timeframe: str, timerange: int):
    """
    Calcula o limite de candles baseado no timeframe e timerange.
    
    Args:
        timeframe (str): timeframe no formato "<n><unit>", ex: "1h", "15m", "2d", "1w", "1M"
        timerange (int): quantidade do timeframe desejada, ex: 1, 2, 3...
        
    Returns:
        int: limite de candles para o período desejado considerando 1 mês (30 dias)
    """
    minutes_per_month = 30 * 24 * 60  # minutos em 1 mês
    
    match = re.match(r"(\d+)([mhdwM])", timeframe)

    if not match:
        raise ValueError(f"Formato inválido para timeframe: {timeframe}")
    
    num, unit = match.groups()
    num = int(num)
    
    if unit == 'm':
        timeframe_minutes = num
    elif unit == 'h':
        timeframe_minutes = num * 60
    elif unit == 'd':
        timeframe_minutes = num * 24 * 60
    elif unit == 'w':
        timeframe_minutes = num * 7 * 24 * 60
    elif unit == 'M':
        timeframe_minutes = num * 30 * 24 * 60
    else:
        raise ValueError(f"Unidade desconhecida no timeframe: {unit}")
    
    limit = int((minutes_per_month / timeframe_minutes) * timerange)
    return limit

