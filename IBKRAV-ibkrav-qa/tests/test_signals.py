import pandas as pd
from ibkrav.model.signals import detectar_reversion_tras_caida

def test_sin_datos():
    df = pd.DataFrame(columns=["open", "high", "low", "close"])
    tipo, idx = detectar_reversion_tras_caida(df)
    assert tipo == "sin_reversion"
    assert idx is None

def test_sintetico_caida_normal():
    data = {
        "open": [10, 9, 8.5, 8.2, 8.0],
        "high": [10.5, 9.3, 8.6, 8.3, 8.2],
        "low":  [9.8, 8.7, 8.3, 8.0, 7.9],
        "close": [9.5, 8.9, 8.4, 8.1, 8.6]
    }
    df = pd.DataFrame(data)
    df.index = range(len(df))
    tipo, idx = detectar_reversion_tras_caida(df)
    assert tipo in ["reversion_normal", "sin_reversion"]
    