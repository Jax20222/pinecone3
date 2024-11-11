from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import os

app = Flask(__name__)
CORS(app)

@app.route('/convert_pdf', methods=['POST'])
def convert_pdf():
    file = request.files['pdf']
    uploads_dir = os.path.join(os.path.dirname(__file__), 'uploads')
    os.makedirs(uploads_dir, exist_ok=True)
    pdf_path = os.path.join(uploads_dir, file.filename)

    try:
        file.save(pdf_path)
        print(f"Archivo PDF guardado en: {pdf_path}")
    except Exception as e:
        return jsonify({'error': f"Error al guardar el archivo: {e}"}), 500

    python_executable = r'C:\Users\jaime\OneDrive\Escritorio\Pinecone\env\Scripts\python.exe'
    textos_dir = os.path.join(os.path.dirname(__file__), 'textos')
    os.makedirs(textos_dir, exist_ok=True)
    output_txt_path = os.path.join(textos_dir, file.filename.replace('.pdf', '.txt'))

    result = subprocess.run([python_executable, 'lumber.py', pdf_path, output_txt_path], cwd=os.path.dirname(__file__), capture_output=True, text=True)

    if result.returncode != 0:
        return jsonify({'error': f"Error en lumber.py: {result.stderr}"}), 500

    try:
        with open(output_txt_path, 'r', encoding='utf-8') as f:
            text = f.read()
        return jsonify({'message': f'Archivo convertido exitosamente y guardado en {output_txt_path}', 'text': text}), 200
    except FileNotFoundError:
        return jsonify({'error': f"Archivo de salida no encontrado en {output_txt_path}"}), 500

# Nuevo endpoint para chunking
@app.route('/chunk_text', methods=['POST'])
def chunk_text():
    try:
        # Obtener el nombre del archivo de texto generado en el primer paso
        texto_nombre = request.json.get('file_name', 'output.txt').replace('.pdf', '.txt')
        input_txt_path = os.path.join(os.path.dirname(__file__), 'textos', texto_nombre)

        # Verificar si el archivo de texto existe
        if not os.path.exists(input_txt_path):
            return jsonify({'error': f"El archivo de texto '{texto_nombre}' no se encontró."}), 404

        # Definir la ruta de salida para los fragmentos
        output_fragments_path = os.path.join(os.path.dirname(__file__), 'fragmentos', texto_nombre.replace('.txt', '_fragmentos.txt'))

        # Ejecutar el chunking con el archivo de texto
        python_executable = r'C:\Users\jaime\OneDrive\Escritorio\Pinecone\env\Scripts\python.exe'
        result = subprocess.run([python_executable, 'chunker.py', input_txt_path, output_fragments_path], cwd=os.path.dirname(__file__), capture_output=True, text=True)

        # Verificar si hubo algún error en la ejecución de chunker.py
        if result.returncode != 0:
            print(f"Error en la ejecución de chunker.py: {result.stderr}")
            return jsonify({'error': f"Error en chunker.py: {result.stderr}"}), 500

        print(f"Fragmentos guardados en: {output_fragments_path}")
        return jsonify({'message': f'Texto fragmentado exitosamente y guardado en {output_fragments_path}'}), 200
    except Exception as e:
        print(f"Error al fragmentar el texto: {e}")
        return jsonify({'error': f"Hubo un error al fragmentar el texto: {e}"}), 500


if __name__ == '__main__':
    app.run(debug=True)