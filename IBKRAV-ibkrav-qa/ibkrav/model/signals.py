
import pandas as pd
from ibkrav.view.graficos import graficar_segmento

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

    if graficar:
        nombre = f"caida_{tipo.lower().replace(' ', '_')}_AAPL_demo"
        graficar_segmento(df, titulo=f"{tipo} AAPL_demo", nombre=f"{nombre}.png", style=style, show=show)

    return tipo, df.index[-1]