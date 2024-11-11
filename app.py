from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import os

app = Flask(__name__)
CORS(app)

@app.route('/convert_pdf', methods=['POST'])
def convert_pdf():
    # Recibe el archivo PDF subido desde el frontend
    file = request.files['pdf']

    # Definir la ruta para guardar el PDF en la carpeta "uploads"
    uploads_dir = os.path.join(os.path.dirname(__file__), 'uploads')
    os.makedirs(uploads_dir, exist_ok=True)  # Asegurarse de que la carpeta exista
    pdf_path = os.path.join(uploads_dir, file.filename)

    try:
        # Guardar el archivo PDF en la carpeta uploads
        file.save(pdf_path)
        print(f"Archivo PDF guardado en: {pdf_path}")
    except Exception as e:
        print(f"Error al guardar el archivo: {e}")
        return jsonify({'error': f"Error al guardar el archivo: {e}"}), 500

    # Ruta al intérprete de Python en el entorno virtual
    python_executable = r'C:\Users\jaime\OneDrive\Escritorio\Pinecone\env\Scripts\python.exe'

    # Definir la ruta para guardar el archivo de texto en la carpeta "textos"
    textos_dir = os.path.join(os.path.dirname(__file__), 'textos')
    os.makedirs(textos_dir, exist_ok=True)  # Asegurarse de que la carpeta exista
    output_txt_path = os.path.join(textos_dir, file.filename.replace('.pdf', '.txt'))

    # Ejecuta lumber.py pasándole la ruta del archivo PDF subido y la ruta de salida
    result = subprocess.run([python_executable, 'lumber.py', pdf_path, output_txt_path], cwd=os.path.dirname(__file__), capture_output=True, text=True)

    # Verifica si hubo algún error en la ejecución de lumber.py
    if result.returncode != 0:
        print(f"Error en la ejecución de lumber.py: {result.stderr}")
        return jsonify({'error': f"Error en lumber.py: {result.stderr}"}), 500

    # Verifica si el archivo de salida fue generado correctamente
    try:
        with open(output_txt_path, 'r', encoding='utf-8') as f:
            text = f.read()
        print(f"Archivo de salida leído correctamente desde: {output_txt_path}")
        # Asegúrate de que esto devuelva un código 200 al frontend
        return jsonify({'message': f'Archivo convertido exitosamente y guardado en {output_txt_path}', 'text': text}), 200
    except FileNotFoundError:
        print(f"El archivo {output_txt_path} no se encontró.")
        return jsonify({'error': f"Archivo de salida no encontrado en {output_txt_path}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
