import tkinter as tk
from tkinter import messagebox, scrolledtext
import subprocess
import os
from pathlib import Path
import webbrowser
import pandas as pd
from ibkrav.model.signals import detectar_reversion_tras_caida, graficar_segmento
import mplfinance as mpf

# Estilo personalizado oscuro para gráficos
estilo_personalizado = mpf.make_mpf_style(
    base_mpf_style='charles',
    rc={
        'axes.facecolor': 'black',
        'figure.facecolor': 'black',
        'savefig.facecolor': 'black'
    },
    marketcolors=mpf.make_marketcolors(
        up='green', down='red', edge='inherit', wick='inherit', volume='in'),
    mavcolors=['purple', 'red', 'green', 'yellow']  # MA20, MA40, MA100, MA200
)

mpf_style = estilo_personalizado

def abrir_log():
    log_path = Path("resultados/graficos.log")
    if not log_path.exists():
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with open(log_path, "w") as f:
            f.write("# Registro de gráficos generados\n")

    with open(log_path, "r") as f:
        contenido = f.read()

    ventana_log = tk.Toplevel(root, bg="black")
    ventana_log.title("Registro de Gráficos Generados")
    txt = scrolledtext.ScrolledText(ventana_log, width=80, height=20, font=("Courier", 10), bg="black", fg="white", insertbackground="white")
    txt.pack(padx=10, pady=10)
    txt.insert(tk.END, contenido)
    txt.config(state="disabled")

def abrir_ultimo_grafico():
    log_path = Path("resultados/graficos.log")
    if not log_path.exists():
        messagebox.showinfo("Log no encontrado", "No se encontró el archivo de log.")
        return

    with open(log_path, "r") as f:
        lineas = [line for line in f.readlines() if "->" in line]
    if not lineas:
        messagebox.showinfo("Sin registros", "El log está vacío.")
        return

    ultima_linea = lineas[-1]
    try:
        ruta = ultima_linea.strip().split(" -> ")[-1]
        ruta_abs = os.path.abspath(ruta)
        if os.path.exists(ruta_abs):
            webbrowser.open(f"file://{ruta_abs}")
        else:
            raise FileNotFoundError("El archivo gráfico no existe en la ruta esperada.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir el gráfico: {e}")

def cargar_analizar_desde_data():
    try:
        ruta_csv = "data/AAPL_demo.csv"
        if not os.path.exists(ruta_csv):
            raise FileNotFoundError("No se encontró el archivo de datos en 'data/AAPL_demo.csv'")

        df = pd.read_csv(ruta_csv, parse_dates=["date"], index_col="date")

        if df.empty:
            raise ValueError("El DataFrame cargado está vacío.")

        tipo, vela = detectar_reversion_tras_caida(
            df,
            graficar=True,
            show=True,
            style=mpf_style
        )

        nombre_grafico = f"{tipo} AAPL_demo - {vela.strftime('%Y%m%d_%H%M')}.png"
        messagebox.showinfo(
            "Resultado",
            f"Resultado: {tipo} en vela {vela}\nGráfico generado: {nombre_grafico}"
        )

    except Exception as e:
        messagebox.showerror("Error al cargar desde data", str(e))

# GUI principal
root = tk.Tk()
root.title("Revisión de Reversiones")
root.geometry("400x300")
root.configure(bg="black")

boton_ver_log = tk.Button(root, text="📂 Ver registro de gráficos", command=abrir_log, bg="#444", fg="white", padx=10, pady=5)
boton_ver_log.pack(pady=10)

boton_abrir_ultimo = tk.Button(root, text="🖼 Abrir último gráfico generado", command=abrir_ultimo_grafico, bg="#222", fg="white", padx=10, pady=5)
boton_abrir_ultimo.pack(pady=10)

boton_data = tk.Button(root, text="📊 Analizar demo en data/", command=cargar_analizar_desde_data, bg="#004", fg="white", padx=10, pady=5)
boton_data.pack(pady=10)

root.mainloop()
