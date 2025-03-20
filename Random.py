import random
import fitz
import streamlit as st
import os

# Función para obtener la carpeta de descargas del usuario
def obtener_carpeta_descargas():
    return os.path.join(os.path.expanduser("~"), "Downloads")

# Título de la aplicación
st.title("Reductor de PDF")

# Subir archivo PDF
archivo_pdf = st.file_uploader("Sube un archivo PDF", type=["pdf"])

if archivo_pdf is not None:
    # Cargar el archivo PDF
    doc = fitz.open(stream=archivo_pdf.read(), filetype="pdf")
    
    # Calcular cuántas páginas dejar (20% del total)
    total_paginas = len(doc)
    paginas_a_dejar = max(1, int(total_paginas * 0.2))  # Asegurar que sea al menos 1 página
    
    # Seleccionar aleatoriamente qué páginas conservar
    paginas_seleccionadas = sorted(random.sample(range(total_paginas), paginas_a_dejar))
    
    # Crear un nuevo PDF solo con esas páginas
    nuevo_doc = fitz.open()
    for i in paginas_seleccionadas:
        nuevo_doc.insert_pdf(doc, from_page=i, to_page=i)
    
    # Guardar el nuevo archivo en la carpeta de descargas
    carpeta_descargas = obtener_carpeta_descargas()
    nombre_archivo = os.path.splitext(archivo_pdf.name)[0]
    ruta_guardado = os.path.join(carpeta_descargas, f"{nombre_archivo}_20%.pdf")
    nuevo_doc.save(ruta_guardado)
    nuevo_doc.close()
    
    # Mostrar mensaje de éxito y enlace de descarga
    st.success(f"Archivo reducido guardado en: {ruta_guardado}")
    st.write(f"[Descargar archivo reducido](file://{ruta_guardado})")
