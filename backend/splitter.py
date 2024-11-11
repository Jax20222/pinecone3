import os
from langchain.text_splitter import MarkdownHeaderTextSplitter

# Ruta relativa del archivo de texto de entrada (se espera que este archivo ya exista)
def chunk_text(input_txt_path, output_fragments_path):
    try:
        # Leer el archivo de texto plano generado previamente
        with open(input_txt_path, 'r', encoding='utf-8') as archivo_texto:
            markdown_document = archivo_texto.read()
        print(f"Archivo '{input_txt_path}' leído correctamente.")
    except FileNotFoundError:
        raise FileNotFoundError(f"No se encontró el archivo en la ruta especificada: {input_txt_path}")
    except Exception as e:
        raise IOError(f"Error al leer el archivo '{input_txt_path}': {e}")

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

    # Guardar los fragmentos en un archivo de salida en la carpeta 'fragmentos'
    try:
        with open(output_fragments_path, 'w', encoding='utf-8') as archivo_fragmentos:
            for fragment in md_header_splits:
                archivo_fragmentos.write(str(fragment) + "\n\n")
        print(f"Los fragmentos han sido guardados en '{output_fragments_path}'.")
    except Exception as e:
        raise IOError(f"Error al escribir los fragmentos en el archivo '{output_fragments_path}': {e}")

    return output_fragments_path
