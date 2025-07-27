import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt
import mplfinance as mpf
from .graficos import graficar_segmento

#Graficar = True cuando el .log no exista
def detectar_reversion_tras_caida(df: pd.DataFrame, graficar=True, show=False, style=None):
    df = df.copy()
    df["MA20"] = df["close"].rolling(window=20).mean()
    df["MA40"] = df["close"].rolling(window=40).mean()
    df["MA100"] = df["close"].rolling(window=100).mean()
    df["MA200"] = df["close"].rolling(window=200).mean()

    df = df.dropna().copy()

    if df.empty:
        raise ValueError("No hay suficientes datos después de calcular los promedios móviles.")


    ultima = df.iloc[-1]
    penultima = df.iloc[-2]

    cambio_dolares = ultima['close'] - penultima['close']
    cambio_pct = (cambio_dolares / penultima['close']) * 100

    if cambio_dolares <= -6 and cambio_pct <= -1.5:
        tipo = "Caída fuerte"
    elif -5 <= cambio_dolares <= -3 and cambio_pct > -1.5:
        tipo = "Caída normal"
    else:
        tipo = "Sin caída significativa"

    timestamp = df.index[-1].strftime("%Y%m%d_%H%M")
    nombre = f"{tipo.replace(' ', '_')}_AAPL_demo_{timestamp}"
    filename = f"resultados/{nombre}.png"

    if graficar:
        mpf.plot(
            df,
            type='candle',
            style=style or 'charles',
            mav=(20, 40, 100, 200),
            volume=True,
            title=f"{tipo} - {idx}",
            savefig=filename,
            show_nontrading=True,
            tight_layout=True
        )
        Path("resultados/graficos.log").parent.mkdir(parents=True, exist_ok=True)
        with open("resultados/graficos.log", "a") as log:
            log.write(f"{datetime.now()} -> {filename}\n")

        if show:
            from PIL import Image
            img = Image.open(filename)
            img.show()

    return tipo, df.index[-1]
