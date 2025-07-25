from ibkrav.model import signals
from ibkrav.ibapi.client import IBKRClient
from ibkrav.view.terminal import mostrar_resultado
from ibkrav.view.telegram import enviar_mensaje_telegram
from ibkrav.model.signals import detectar_tendencia_alcista
import pandas as pd
import os

def ejecutar():
    client = IBKRClient()
    client.conectar()
    symbol = "AAPL"
    datos = client.obtener_datos_historicos(symbol)

    # ✅ Convertir a DataFrame para análisis
    df = pd.DataFrame(datos)

    # 🚨 Validar que el DataFrame contiene columna 'close'
    if df.empty or 'close' not in df.columns:
        print("⚠️ Datos insuficientes o sin columna 'close'")
        return

    # 💾 Guardar CSV para revisión
    os.makedirs("resultados", exist_ok=True)
    df.to_csv(f"resultados/{symbol}_historico.csv", index=False)

    signal = signals.generar_signal(datos)
    mostrar_resultado(symbol, signal)
    enviar_mensaje_telegram(symbol, signal)

    if detectar_tendencia_alcista(df):
        print("🚀 Tendencia alcista fuerte. Revisar que el MA20 y MA40 se vean paralelas. Si el PM40 se aleja por encima estamos en zona cara")
        