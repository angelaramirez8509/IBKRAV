import pandas as pd

def generar_signal(datos):
    if not datos:
        return "NO DATA"
    if datos[-1].close > datos[0].close:
        return "BUY"
    return "SELL"


def detectar_tendencia_alcista(df: pd.DataFrame, min_ratio=0.6) -> bool:
    df = df.copy()
    df["MA20"] = df["close"].rolling(window=20).mean()
    df["MA40"] = df["close"].rolling(window=40).mean()
    df["MA100"] = df["close"].rolling(window=100).mean()
    df["MA200"] = df["close"].rolling(window=200).mean()

    valid_rows = df.dropna()
    if valid_rows.empty:
        return False

    velas_alcistas = (valid_rows["close"] > valid_rows["MA20"]).sum()
    total = len(valid_rows)
    if velas_alcistas / total < min_ratio:
        return False

    ultima = valid_rows.iloc[-1]
    return ultima["MA20"] > ultima["MA40"] > ultima["MA100"] > ultima["MA200"]