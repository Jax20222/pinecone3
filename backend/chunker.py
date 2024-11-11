import sys
import os
from langchain.text_splitter import MarkdownHeaderTextSplitter

# Verificar los argumentos
if len(sys.argv) < 3:
    raise ValueError("Uso: python chunker.py <ruta_del_archivo_txt> <ruta_de_salida>")

input_file_path = sys.argv[1]
output_file_path = sys.argv[2]

# Leer el contenido del archivo de texto
try:
    with open(input_file_path, 'r', encoding='utf-8') as archivo_texto:
        markdown_document = archivo_texto.read()
    print(f"Archivo '{input_file_path}' leído correctamente.")
except FileNotFoundError:
    raise FileNotFoundError(f"No se encontró el archivo en la ruta especificada: {input_file_path}")
except Exception as e:
    raise IOError(f"Error al leer el archivo '{input_file_path}': {e}")

# Definir los encabezados para dividir el documento basado en encabezados H2
headers_to_split_on = [
    ("##", "Header 2")
]

# Inicializar el MarkdownHeaderTextSplitter
markdown_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=headers_to_split_on, strip_headers=False
)

# Dividir el documento en fragmentos basados en los encabezados
try:
    md_header_splits = markdown_splitter.split_text(markdown_document)
    print("Documento dividido correctamente en fragmentos.")
except Exception as e:
    raise RuntimeError(f"Error al dividir el documento en fragmentos: {e}")

# Guardar los fragmentos en un archivo de salida
try:
    with open(output_file_path, 'w', encoding='utf-8') as archivo_fragmentos:
        for fragment in md_header_splits:
            archivo_fragmentos.write(str(fragment) + "\n\n")
    print(f"Los fragmentos han sido guardados en '{output_file_path}'.")
except Exception as e:
    raise IOError(f"Error al escribir los fragmentos en el archivo '{output_file_path}': {e}")
