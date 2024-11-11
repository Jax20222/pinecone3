import pdfplumber
import sys
import os

# Recibir la ruta del PDF como argumento
pdf_path = sys.argv[1]  # El primer argumento es la ruta al archivo PDF
output_path = sys.argv[2]  # El segundo argumento es la ruta al archivo de salida

# Función para convertir PDF a texto usando pdfplumber
def pdf_a_texto(pdf_path):
    texto_completo = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            num_paginas = len(pdf.pages)
            print(f"PDF abierto correctamente. Número de páginas: {num_paginas}")
            for i, pagina in enumerate(pdf.pages):
                texto_pagina = pagina.extract_text()
                if texto_pagina:
                    texto_completo += texto_pagina + "\n"
                print(f"Texto extraído de la página {i+1}: {len(texto_pagina)} caracteres")
    except Exception as e:
        print(f"Error al procesar el PDF: {e}")
        raise
    return texto_completo

# Convertir el PDF a texto
texto = pdf_a_texto(pdf_path)

# Guardar el texto en un archivo de salida
try:
    with open(output_path, 'w', encoding='utf-8') as archivo_texto:
        archivo_texto.write(texto)
    print(f"El archivo de texto ha sido guardado correctamente en: {output_path}")
except Exception as e:
    print(f"Error al guardar el archivo de salida: {e}")
    raise
