"""Funciones sencillas que se reutilizan en los notebooks."""
import pandas as pd

# Diccionario para pasar los meses en español a número
MESES = {
    "enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6,
    "julio": 7, "agosto": 8, "septiembre": 9, "octubre": 10,
    "noviembre": 11, "diciembre": 12,
}


def coma_a_numero(columna):
    """Convierte una columna con coma decimal ('93,994') a número (93.994)."""
    return pd.to_numeric(columna.str.replace(",", "."))


def fecha_espanola(columna):
    """Convierte '2-agosto-2019' en fecha. Los nulos se quedan como NaT."""
    partes = columna.str.split("-", expand=True)  # dia | mes | año
    mes = partes[1].map(MESES)
    texto = partes[2] + "-" + mes.astype("Int64").astype(str) + "-" + partes[0]
    return pd.to_datetime(texto, format="%Y-%m-%d", errors="coerce")


def tasa_conversion(df, columna):
    """Devuelve nº de clientes y % de suscripción (y=1) por cada valor de 'columna'."""
    tabla = df.groupby(columna, observed=True)["y"].agg(["count", "sum", "mean"])
    tabla.columns = ["clientes", "suscritos", "tasa_%"]
    tabla["tasa_%"] = (tabla["tasa_%"] * 100).round(2)
    return tabla.sort_values("tasa_%", ascending=False)
