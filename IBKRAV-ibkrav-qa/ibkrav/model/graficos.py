import mplfinance as mpf
from pathlib import Path
from datetime import datetime
import pandas as pd

def graficar_segmento(df: pd.DataFrame, nombre="grafico", style=None, show=False, filename=None) -> str:
    if style is None:
        style = mpf.make_mpf_style(
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

    Path("resultados").mkdir(parents=True, exist_ok=True)

    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"resultados/{nombre}_{timestamp}.png"

    mpf.plot(
        df,
        type='candle',
        mav=(20, 40, 100, 200),
        style=style,
        volume=True,
        title=nombre,
        tight_layout=True,
        show_nontrading=True,
        savefig=filename,
        show=show
    )

    # Registrar en log
    with open("resultados/graficos.log", "a") as log:
        log.write(f"{pd.Timestamp.now()} -> {filename}\n")

    return filename
