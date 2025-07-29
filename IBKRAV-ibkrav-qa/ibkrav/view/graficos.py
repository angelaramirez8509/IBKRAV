
import mplfinance as mpf
from pathlib import Path
from datetime import datetime
from PIL import Image

def graficar_segmento(df, titulo="Gráfico", nombre=None, style=None, show=False):
    if df.empty:
        raise ValueError("El DataFrame está vacío, no se puede graficar.")

    style = style or mpf.make_mpf_style(
        base_mpf_style='charles',
        rc={'axes.facecolor': 'black', 'figure.facecolor': 'black'},
        marketcolors=mpf.make_marketcolors(
            up='green', down='red',
            edge='inherit', wick='inherit', volume='in'
        ),
        mavcolors=['purple', 'red', 'green', 'yellow']
    )

    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    nombre_archivo = nombre or f"grafico_{timestamp}.png"
    path_resultado = Path("resultados") / nombre_archivo
    path_resultado.parent.mkdir(parents=True, exist_ok=True)

    mpf.plot(
        df,
        type='candle',
        style=style,
        mav=(20, 40, 100, 200),
        volume=True,
        title=titulo,
        savefig=str(path_resultado),
        tight_layout=True,
        show_nontrading=True
    )

    with open("resultados/graficos.log", "a") as log:
        log.write(f"{datetime.now()} -> {path_resultado}\n")

    if show:
        img = Image.open(path_resultado)
        img.show()

    return path_resultado