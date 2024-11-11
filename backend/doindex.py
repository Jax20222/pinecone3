import os
import time
from pinecone import Pinecone, ServerlessSpec

# Obtener las API keys desde las variables de entorno
pinecone_api_key = os.environ.get("PINECONE_API_KEY")
if not pinecone_api_key:
    raise ValueError("La variable de entorno 'PINECONE_API_KEY' no está configurada.")

# Crear una instancia de Pinecone
try:
    pc = Pinecone(api_key=pinecone_api_key)
except Exception as e:
    raise ConnectionError(f"No se pudo conectar a Pinecone: {e}")

# Configurar la nube y la región para Pinecone desde variables de entorno (o usar valores predeterminados)
cloud = os.environ.get('PINECONE_CLOUD', 'aws')
region = os.environ.get('PINECONE_REGION', 'us-west-1')  # Usando región por defecto si no está configurada
spec = ServerlessSpec(cloud=cloud, region=region)

# Definir el nombre del índice
index_name = "neonato"  # El índice que estás usando

# Dimensión de los embeddings (asumiendo OpenAI embeddings con 1536 dimensiones)
dimension = 1536

# Crear el índice si no existe
try:
    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=dimension,
            metric="cosine",  # Puedes cambiar a 'dotproduct' o 'euclidean' si es necesario
            spec=spec
        )
        # Esperar hasta que el índice esté listo
        while not pc.describe_index(index_name).status['ready']:
            time.sleep(1)
        print(f"Índice '{index_name}' creado exitosamente.")
    else:
        print(f"Índice '{index_name}' ya existe.")
except Exception as e:
    raise RuntimeError(f"Error al crear el índice: {e}")

# Ver el estado del índice antes de realizar el "upsert"
try:
    print("Estado del índice antes del upsert:")
    print(pc.Index(index_name).describe_index_stats())
    print("\n")
except Exception as e:
    raise RuntimeError(f"No se pudo obtener el estado del índice: {e}")
