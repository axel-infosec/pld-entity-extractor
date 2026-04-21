import spacy
import pandas as pd
from datetime import datetime
from pathlib import Path

# Cargamos el motor de IA una sola vez a nivel global para mayor eficiencia
print(f"[{datetime.now().strftime('%H:%M:%S')}] Cargando motor de IA...")
nlp = spacy.load("es_core_news_lg")

def extraer_nombres(archivo_entrada: str) -> list:
    """
    Lee un archivo de texto y utiliza el modelo NER de SpaCy para 
    extraer entidades etiquetadas como Personas (PER).
    """
    ruta = Path(archivo_entrada)
    if not ruta.is_file():
        raise FileNotFoundError(f"No se encontró el archivo: {archivo_entrada}")

    print(f"[{datetime.now().strftime('%H:%M:%S')}] Leyendo archivo: {ruta.name}...")
    with ruta.open("r", encoding="utf-8") as f:
        texto = f.read()
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Analizando texto y buscando personas...")
    doc = nlp(texto)
    
    # Extraemos solo entidades de tipo "PER" (Persona), eliminamos duplicados y ordenamos
    nombres = sorted(list(set([ent.text for ent in doc.ents if ent.label_ == "PER"])))
    
    return nombres

def guardar_resultados(lista_nombres: list, nombre_archivo: str = None) -> None:
    """
    Toma una lista de nombres y la exporta a un archivo Excel (.xlsx)
    incluyendo una marca de tiempo de la extracción.
    """
    if not lista_nombres:
        print("No se encontraron nombres en el texto analizado.")
        return

    # Creamos un DataFrame de Pandas
    df = pd.DataFrame(lista_nombres, columns=["Nombres Encontrados"])
    df["Fecha de Extracción"] = datetime.now().strftime("%d/%m/%Y")
    
    # Guardamos a Excel
    if nombre_archivo is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"reporte_{timestamp}.xlsx"
    df.to_excel(nombre_archivo, index=False)
    print(f"Se han guardado {len(lista_nombres)} nombres en '{nombre_archivo}'.")

if __name__ == "__main__":
    print("--- Analizador NER para PLD ---")
    archivo_txt = input("Ingresa la ruta del archivo de texto (ej. datos.txt): ")
    
    try:
        nombres_extraidos = extraer_nombres(archivo_txt)
        guardar_resultados(nombres_extraidos)
    except Exception as e:
        print(f"Error inesperado: {e}")