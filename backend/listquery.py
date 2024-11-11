import os
import time
from pinecone import Pinecone

# Configurar las API keys desde las variables de entorno
pinecone_api_key = os.environ.get('PINECONE_API_KEY')
if not pinecone_api_key:
    raise ValueError("La variable de entorno 'PINECONE_API_KEY' no está configurada.")

# Crear una instancia de Pinecone
try:
    pc = Pinecone(api_key=pinecone_api_key)
except Exception as e:
    raise ConnectionError(f"No se pudo conectar a Pinecone: {e}")

# Definir el índice y el namespace que estás utilizando
index_name = "neonato"
namespace = "Rasa01"

# Conectar con el índice de Pinecone
try:
    index = pc.Index(index_name)
except Exception as e:
    raise RuntimeError(f"No se pudo conectar al índice '{index_name}': {e}")

# Ruta del archivo de resultados (relativa)
output_path = os.path.join(os.path.dirname(__file__), '..', 'resultados_consulta.txt')

# Abrir el archivo para guardar los resultados
try:
    with open(output_path, "w") as file:
        # Listar y consultar los registros en el namespace "Rasa01"
        ids_list = index.list(namespace=namespace)
        if not ids_list:
            print(f"No se encontraron registros en el namespace '{namespace}'.")
        else:
            for ids in ids_list:
                query = index.query(
                    id=ids[0],  # Obtener el primer ID del listado
                    namespace=namespace,
                    top_k=1,  # Obtener el vector más cercano (k=1)
                    include_values=True,
                    include_metadata=True
                )
                # Guardar el resultado en el archivo
                file.write(f"Resultado para ID {ids[0]}:\n")
                file.write(str(query))  # Convertir el resultado a string y escribir en el archivo
                file.write("\n\n")
                
        print(f"Consulta completada y resultados guardados en '{output_path}'.")
except Exception as e:
    raise IOError(f"No se pudo escribir en el archivo de salida: {e}")
