import pandas as pd
import pytest
from ibkrav.model.signals import detectar_reversion_tras_caida

@pytest.mark.parametrize("archivo", [
    "data/AAPL.csv",
    "data/MSFT.csv"
])
def test_csv_real(archivo):
    df = pd.read_csv(archivo)
    assert all(col in df.columns for col in ["open", "high", "low", "close"])
    tipo, idx = detectar_reversion_tras_caida(df)
    print(f"🧪 {archivo} → {tipo} @ vela {idx}")
    assert tipo in ["reversion_fuerte", "reversion_normal", "sin_reversion"]
