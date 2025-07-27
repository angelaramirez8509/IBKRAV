# limit_price_gui.py (versión refinada)
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from ibkrav.model.limit_price import calcular_precio_limite
import csv
import os
from datetime import datetime

def calcular():
    try:
        contratos = int(entry_contratos.get())
        costo = float(entry_costo.get())
        usar_auto = var_auto.get() == 1
        comision_manual = float(entry_comision.get()) if not usar_auto else 0.0
        multiplicador = float(entry_mult.get())

        # ✅ Comisiones por defecto (si están vacías)
        comision_fija = float(entry_comision_fija.get()) if entry_comision_fija.get() else 7.0
        comision_por_contrato = float(entry_comision_por_contrato.get()) if entry_comision_por_contrato.get() else 1.25

        if contratos <= 0 or costo <= 0 or multiplicador <= 0:
            raise ValueError("Todos los valores deben ser mayores que cero.")

        resultado = calcular_precio_limite(
            contratos, costo, usar_auto,
            comision_manual, multiplicador,
            comision_fija, comision_por_contrato
        )

        output = "\n".join([f"{k.replace('_', ' ').capitalize()}: ${v}" for k, v in resultado.items()])
        messagebox.showinfo("✅ Resultado del Cálculo", output)

        os.makedirs("resultados", exist_ok=True)
        filename = f"resultados/limite_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(filename, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Concepto", "Valor"])
            for k, v in resultado.items():
                writer.writerow([k.replace('_', ' ').capitalize(), v])

        messagebox.showinfo("💾 Guardado", f"Resultado exportado a:\n{filename}")

    except Exception as e:
        messagebox.showerror("❌ Error", str(e))


def toggle_manual():
    entry_comision.config(state="normal" if var_auto.get() == 0 else "disabled")

# 🌙 App en modo oscuro elegante
app = ttk.Window(
    title="📈 Calculadora Precio Límite - Opciones CALL",
    themename="darkly",
    size=(440, 390),
    resizable=(False, False),
    position=(700, 300)
)

frame = ttk.Frame(app, padding=15)
frame.pack(pady=10)

def agregar_entrada(texto, fila):
    ttk.Label(frame, text=texto).grid(row=fila, column=0, sticky="w", padx=4, pady=4)
    entrada = ttk.Entry(frame, width=20)
    entrada.grid(row=fila, column=1)
    return entrada

entry_contratos = agregar_entrada("🧾 Contratos:", 0)
entry_costo = agregar_entrada("💰 Costo por contrato ($):", 1)

var_auto = ttk.IntVar(value=1)
ttk.Checkbutton(
    frame,
    text="🧮 Calcular comisión automáticamente",
    variable=var_auto,
    command=toggle_manual,
    bootstyle="info-round-toggle"
).grid(row=2, column=0, columnspan=2, sticky="w", padx=4)

ttk.Label(frame, text="✏️ Comisión manual ($):").grid(row=3, column=0, sticky="w", padx=4)
entry_comision = ttk.Entry(frame, width=20)
entry_comision.insert(0, "0.0")
entry_comision.grid(row=3, column=1)

ttk.Label(frame, text="⚙️ Comisión fija ($, opcional):").grid(row=5, column=0, sticky="w", padx=4)
entry_comision_fija = ttk.Entry(frame, width=20)
entry_comision_fija.insert(0, "7.0")
entry_comision_fija.grid(row=5, column=1)

ttk.Label(frame, text="⚙️ Comisión por contrato ($, opcional):").grid(row=6, column=0, sticky="w", padx=4)
entry_comision_por_contrato = ttk.Entry(frame, width=20)
entry_comision_por_contrato.insert(0, "1.25")
entry_comision_por_contrato.grid(row=6, column=1)

ttk.Label(frame, text="🎯 Multiplicador deseado:").grid(row=4, column=0, sticky="w", padx=4)
entry_mult = ttk.Entry(frame, width=20)
entry_mult.insert(0, "2.0")
entry_mult.grid(row=4, column=1)

toggle_manual()

ttk.Button(
    app,
    text="📊 Calcular Precio Límite",
    command=calcular,
    bootstyle="success-outline"
).pack(pady=20)

app.mainloop()
