"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""
import pandas as pd
import re

def limpiar_titulo(titulo: str) -> str:
    """Convierte los títulos en minúsculas y reemplaza espacios por guiones bajos."""
    return titulo.lower().replace(" ", "_")

def procesar_palabras_clave(palabras_clave_columna):
    """Procesa la columna de palabras clave para unir y limpiar los textos."""
    claves, texto = [], ""
    for p in palabras_clave_columna:
        if isinstance(p, str):
            p = re.sub(r'\s+', ' ', p).strip().rstrip(".")
            texto += p + " "
        elif texto:
            claves.append(", ".join(re.split(r'\s*,\s*', texto.strip())))
            texto = ""
    if texto:
        claves.append(", ".join(re.split(r'\s*,\s*', texto.strip())))
    return claves

def pregunta_01():
    """
    Construye y retorna un DataFrame de Pandas a partir del archivo
    'input/clusters_report.txt' cumpliendo los siguientes requisitos:
    
    - Mantiene la misma estructura que el archivo original.
    - Los nombres de las columnas están en minúsculas con espacios reemplazados por guiones bajos.
    - Las palabras clave se separan por comas y con un solo espacio entre ellas.
    """
    # Leer archivo ignorando líneas en blanco iniciales
    with open("files/input/clusters_report.txt", "r", encoding="utf-8") as file:
        lineas = file.readlines()
    
    # Extraer y limpiar los títulos de las columnas
    t1 = re.sub(r"\s{2,}", "-", lineas[0]).strip().split("-")
    t2 = re.sub(r"\s{2,}", "-", lineas[1]).strip().split("-")
    t1.pop()
    t2.pop(0)
    
    cabeceras = [
        t1[0],  
        f"{t1[1]} {t2[0]}",  
        f"{t1[2]} {t2[1]}",
        t1[3], 
    ]    
    cabeceras = [limpiar_titulo(t) for t in cabeceras]
    
    # Leer el archivo 
    df = pd.read_fwf(
        "files/input/clusters_report.txt", widths=[9, 16, 16, 80], 
        header=None, names=cabeceras, skip_blank_lines=False,
        converters={cabeceras[2]: lambda x: x.rstrip(" %").replace(",", ".")},
    ).iloc[4:] 
    
    # Extraer y procesar palabras clave
    palabras_clave = df[cabeceras[3]]
    df = df[df[cabeceras[0]].notna()].drop(columns=[cabeceras[3]])
    df = df.astype({
        cabeceras[0]: int,
        cabeceras[1]: int,
        cabeceras[2]: float,
    })
    
    df[cabeceras[3]] = procesar_palabras_clave(palabras_clave)
    
    print(df)
    return df  

pregunta_01()