import pandas as pd
from ibkrav.model.signals import detectar_reversion_tras_caida
from ibkrav.model.graficos import graficar_segmento
from pathlib import Path
import matplotlib
matplotlib.use("Agg")  # Evita problemas de entorno

# Crear DataFrame de prueba con caída fuerte
fechas = pd.date_range(end=pd.Timestamp.today(), periods=250)
precios = [180] * 248 + [174, 168]  # Caída fuerte al final
df = pd.DataFrame({
    "date": fechas,
    "open": precios,
    "high": [p + 1 for p in precios],
    "low": [p - 1 for p in precios],
    "close": precios,
    "volume": [1_000_000] * 250
}).set_index("date")

# Crear carpeta resultados/
Path("resultados").mkdir(exist_ok=True)

# Ejecutar
try:
    tipo, vela = detectar_reversion_tras_caida(
        df,
        graficar=True,
        show=False,
        style=None
    )
    print(f"[OK] Tipo detectado: {tipo} en {vela}")
except Exception as e:
    print(f"[ERROR] {e}")
