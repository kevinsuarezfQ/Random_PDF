import random
import fitz
import streamlit as st
import os
from io import BytesIO

# Título de la aplicación
st.title("Reductor de PDF")

# Subir archivo PDF
archivo_pdf = st.file_uploader("Sube un archivo PDF", type=["pdf"])

if archivo_pdf is not None:
    # Cargar el archivo PDF
    doc = fitz.open(stream=archivo_pdf.read(), filetype="pdf")
    
    # Calcular cuántas páginas dejar (20% del total)
    total_paginas = len(doc)
    paginas_a_dejar = max(1, int(total_paginas * 0.2))
    
    # Seleccionar aleatoriamente qué páginas conservar
    paginas_seleccionadas = sorted(random.sample(range(total_paginas), paginas_a_dejar))
    
    # Crear un nuevo PDF solo con esas páginas
    nuevo_doc = fitz.open()
    for i in paginas_seleccionadas:
        # Copiar la página al nuevo documento
        nuevo_doc.insert_pdf(doc, from_page=i, to_page=i)

    # Agregar marca de agua a todas las páginas del nuevo documento
    for pagina in nuevo_doc:
        rect = pagina.rect  # Dimensiones de la página
        texto = "Documento al 20%"  # Texto de la marca de agua
        tamaño_fuente = 40  # Tamaño de la fuente

        posicion = fitz.Point(rect.width / 4, rect.height / 2)  # Posición central aproximada

        # Dibujar el texto en la página
        pagina.insert_text(
            posicion,
            texto,
            fontsize=tamaño_fuente,
            fontname="times-roman",
            color=(0.85, 0.85, 0.85),  # Color gris
            rotate=0,  # Rotación del texto
            overlay=True
        )
    
    # Guardar el nuevo archivo en memoria
    pdf_bytes = BytesIO()
    nuevo_doc.save(pdf_bytes)
    nuevo_doc.close()
    pdf_bytes.seek(0)
    
    # Mostrar mensaje de éxito
    st.success("Archivo reducido generado con éxito.")
    
    # Botón para descargar el archivo
    nombre_archivo = os.path.splitext(archivo_pdf.name)[0]
    st.download_button(
        label="Descargar archivo reducido",
        data=pdf_bytes,
        file_name=f"{nombre_archivo}_20%.pdf",
        mime="application/pdf"
    )