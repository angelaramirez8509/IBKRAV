# strategies.py

# Aquí se implementarán las estrategias como check_moving_averages y check_gap_breakdown

# strategies.py

import pandas as pd
from datetime import datetime
from ib_insync import Stock
from telegram_alerts import send_telegram
import asyncio

# src/strategies.py

def check_moving_averages(ib, symbol):
    contract = Stock(symbol, 'SMART', 'USD')
    bars = ib.reqHistoricalData(
        contract,
        endDateTime='',
        durationStr='1 Y', #1 año
        barSizeSetting='1 day',#barras cada dia
        whatToShow='TRADES',
        useRTH=True,
        formatDate=1
    )

    if not bars:
        print(f"⚠️ No data para {symbol}")
        return

    closes = [bar.close for bar in bars]
    if len(closes) < 200:
        print(f"⚠️ No hay suficientes datos para {symbol}")
        return

    # Cálculo de medias móviles
    ma20 = sum(closes[-20:]) / 20
    ma40 = sum(closes[-40:]) / 40
    ma100 = sum(closes[-100:]) / 100
    ma200 = sum(closes[-200:]) / 200

    # Ejemplo de alerta si MA20 cruza MA40
    if ma20 > ma40:
        msg = f"🚀 {symbol}: MA20 ({ma20:.2f}) > MA40 ({ma40:.2f})"
        print(msg)
        send_telegram(msg)


def check_gap_breakdown(ib, symbol):
    contract = Stock(symbol, 'SMART', 'USD')
    
    bars = ib.reqHistoricalData(
        contract,
        endDateTime='',
        durationStr='2 D',
        barSizeSetting='1 day',
        whatToShow='TRADES',
        useRTH=True
    )
    
    if len(bars) < 2:
        return
    
    prev_low = bars[-2].low
    today_open = bars[-1].open
    
    if today_open < prev_low:
        msg = f"⚠️ {symbol} Apertura ROMPE piso GAP: Open={today_open}, Prev Low={prev_low}"
        asyncio.run(send_telegram(msg))
        log_alert(symbol, 'Ruptura Piso GAP', {'open': today_open, 'prev_low': prev_low})

def log_alert(symbol, strategy, data):
    now = datetime.now().isoformat()
    log_entry = pd.DataFrame([{
        'datetime': now,
        'symbol': symbol,
        'strategy': strategy,
        'data': data
    }])
    log_entry.to_csv('logs/alerts_log.csv', mode='a', index=False, header=not pd.io.common.file_exists('logs/alerts_log.csv'))


# strategies.py

def check_gap_and_alert(ib, symbol, threshold=1.0):
    contract = Stock(symbol, 'SMART', 'USD')
    bars = ib.reqHistoricalData(
        contract,
        endDateTime='',
        durationStr='2 D',
        barSizeSetting='1 day',
        whatToShow='TRADES',
        useRTH=True
    )

    if len(bars) < 2:
        print(f"Not enough data for {symbol}")
        return

    prev_close = bars[-2].close
    today_open = bars[-1].open
    gap_pct = ((today_open - prev_close) / prev_close) * 100

    if abs(gap_pct) >= threshold:
        msg = f"🔔 GAP Alert {symbol}: {gap_pct:.2f}% (Prev Close: {prev_close}, Open: {today_open})"
        asyncio.run(send_telegram(msg))
        log_alert(symbol, 'GAP', gap_pct)

def check_first_candle_color(ib, symbol, timeframe='5 mins'):
    contract = Stock(symbol, 'SMART', 'USD')
    bars = ib.reqHistoricalData(
        contract,
        endDateTime='',
        durationStr='30 mins',
        barSizeSetting=timeframe,
        whatToShow='TRADES',
        useRTH=True
    )

    if len(bars) == 0:
        return

    first_bar = bars[0]
    color = 'green' if first_bar.close > first_bar.open else 'red'
    msg = f"🕒 First Candle Alert {symbol}: {color.upper()} candle ({first_bar.open}->{first_bar.close})"
    asyncio.run(send_telegram(msg))
    log_alert(symbol, 'First Candle', color)

def log_alert(symbol, strategy, data):
    now = datetime.now().isoformat()
    log_entry = pd.DataFrame([{
        'datetime': now,
        'symbol': symbol,
        'strategy': strategy,
        'data': data
    }])
    log_entry.to_csv('logs/alerts_log.csv', mode='a', index=False, header=not pd.io.common.file_exists('logs/alerts_log.csv'))
