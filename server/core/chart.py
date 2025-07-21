import os
import pandas as pd
import mplfinance as mpf
import logging
import sys

def generate_chart(df, buy_signals, sell_signals, filename):
    if df.empty:
        logging.warning("DataFrame vazio. Gráfico não será gerado.")
        return

    # Garante que o índice do DataFrame seja datetime
    # Use astype(str) first to handle potential mixed types before to_datetime
    df.index = pd.to_datetime(df.index.astype(str))
    # Ordenar o índice é crucial para mplfinance
    df = df.sort_index()

    # Converte sinais para datetime também
    # Garante que buy_signals e sell_signals sejam Series ou listas, e depois convertidos
    buy_signals = pd.to_datetime(buy_signals) if buy_signals is not None else pd.Series(dtype='datetime64[ns]')
    sell_signals = pd.to_datetime(sell_signals) if sell_signals is not None else pd.Series(dtype='datetime64[ns]')


    # Garante que o diretório onde o gráfico será salvo exista
    dir_path = os.path.dirname(filename)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    apds = []

    # ========== BUY SIGNALS ==========
    # Solução inspirada no Stack Overflow: criar uma série com o mesmo índice do df
    if not buy_signals.empty and 'low' in df.columns:
        buy_y = pd.Series(df['low'] * 0.99, index=df.index)
        # Usar .isin() para criar uma máscara booleana para os pontos de sinal
        buy_mask = buy_y.index.isin(buy_signals)
        # Aplicar a máscara para manter apenas os valores nos pontos de sinal, outros são NaN
        buy_y = buy_y.mask(~buy_mask) # '~' inverte a máscara

        if not buy_y.dropna().empty: # Verifica se há pontos de sinal reais
            apds.append(mpf.make_addplot(
                buy_y, type='scatter', marker='^',
                markersize=100, color='green'))
        else:
            logging.info("Nenhum sinal de compra válido encontrado no DataFrame para plotar.")
    elif 'low' not in df.columns:
        logging.warning("Coluna 'low' não encontrada no DataFrame para sinais de compra.")
    else:
        logging.info("Nenhum sinal de compra fornecido ou vazio.")


    # ========== SELL SIGNALS ==========
    # Solução inspirada no Stack Overflow: criar uma série com o mesmo índice do df
    if not sell_signals.empty and 'high' in df.columns:
        sell_y = pd.Series(df['high'] * 1.01, index=df.index)
        # Usar .isin() para criar uma máscara booleana para os pontos de sinal
        sell_mask = sell_y.index.isin(sell_signals)
        # Aplicar a máscara para manter apenas os valores nos pontos de sinal, outros são NaN
        sell_y = sell_y.mask(~sell_mask)

        if not sell_y.dropna().empty: # Verifica se há pontos de sinal reais
            apds.append(mpf.make_addplot(
                sell_y, type='scatter', marker='v',
                markersize=100, color='red'))
        else:
            logging.info("Nenhum sinal de venda válido encontrado no DataFrame para plotar.")
    elif 'high' not in df.columns:
        logging.warning("Coluna 'high' não encontrada no DataFrame para sinais de venda.")
    else:
        logging.info("Nenhum sinal de venda fornecido ou vazio.")


    # ========== INDICADORES ==========
    # É uma boa prática verificar se as colunas existem antes de tentar plotá-las
    # E também lidar com possíveis valores NaN nos indicadores, embora o mplfinance
    # geralmente os trate graciosamente ao não plotar os pontos ausentes.
    if 'SMA_20' in df.columns and 'EMA_50' in df.columns:
        # Verifica se ambas as colunas têm dados para plotar
        if not df[['SMA_20', 'EMA_50']].dropna().empty:
            apds.append(mpf.make_addplot(df[['SMA_20', 'EMA_50']]))
        else:
            logging.info("SMA_20 ou EMA_50 estão vazios após remover NaNs.")

    if 'RSI_14' in df.columns:
        if not df['RSI_14'].dropna().empty:
            apds.append(mpf.make_addplot(df['RSI_14'], panel=1))
        else:
            logging.info("RSI_14 está vazio após remover NaNs.")

    if 'MACD_12_26_9' in df.columns and 'MACDs_12_26_9' in df.columns:
        if not df[['MACD_12_26_9', 'MACDs_12_26_9']].dropna().empty:
            apds.append(mpf.make_addplot(df[['MACD_12_26_9', 'MACDs_12_26_9']], panel=2))
        else:
            logging.info("MACD_12_26_9 ou MACDs_12_26_9 estão vazios após remover NaNs.")

    if 'MACDh_12_26_9' in df.columns:
        if not df['MACDh_12_26_9'].dropna().empty:
            apds.append(mpf.make_addplot(df['MACDh_12_26_9'], type='bar', panel=2))
        else:
            logging.info("MACDh_12_26_9 está vazio após remover NaNs.")

    try:
        if not df.empty: # Verificação final para garantir que df não esteja vazio antes de plotar
            mpf.plot(df, type='candle', style='yahoo',
                     ylabel='Price', ylabel_lower='Volume',
                     volume=True, addplot=apds, figscale=1.5,
                     savefig=filename)
            logging.info(f"Gráfico salvo em {filename}")
        else:
            logging.warning("DataFrame vazio, gráfico não pode ser gerado.")

    except Exception as e:
        logging.error(f"Erro ao gerar gráfico: {e}")
        sys.exit(1)