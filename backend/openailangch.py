import os
from pinecone import Pinecone, ServerlessSpec
from langchain_openai import OpenAIEmbeddings  # Import actualizado para OpenAIEmbeddings
from langchain_community.vectorstores import Pinecone as VectorStorePinecone

# Configurar las API keys desde las variables de entorno
pinecone_api_key = os.environ.get('PINECONE_API_KEY')
openai_api_key = os.environ.get('OPENAI_API_KEY')

# Verificar que las API keys se han cargado correctamente
if not pinecone_api_key:
    raise ValueError("La variable de entorno 'PINECONE_API_KEY' no está configurada.")
if not openai_api_key:
    raise ValueError("La variable de entorno 'OPENAI_API_KEY' no está configurada.")

# Crear una instancia de Pinecone
try:
    pc = Pinecone(api_key=pinecone_api_key)
except Exception as e:
    raise ConnectionError(f"No se pudo conectar a Pinecone: {e}")

# Verificar si el índice ya existe, si no, crearlo
index_name = "neonato"
try:
    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=1536,  # Dimensión para OpenAI embeddings
            metric='cosine',  # Cambia la métrica si es necesario
            spec=ServerlessSpec(
                cloud='aws',
                region='us-west-1'  # Cambia la región si es necesario
            )
        )
        print(f"Índice '{index_name}' creado en Pinecone.")
    else:
        print(f"Índice '{index_name}' ya existe en Pinecone.")
except Exception as e:
    raise RuntimeError(f"Error al crear o verificar el índice '{index_name}': {e}")

# Crear los embeddings con OpenAI
try:
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
except Exception as e:
    raise RuntimeError(f"No se pudo conectar a OpenAI para crear embeddings: {e}")

# Leer el contenido de 'salida_mejorada.txt'
file_path = os.path.join(os.path.dirname(__file__), '..', 'salida_mejorada.txt')
try:
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    print(f"Contenido de '{file_path}' leído correctamente.")
except FileNotFoundError:
    raise FileNotFoundError(f"No se encontró el archivo en la ruta especificada: {file_path}")
except Exception as e:
    raise IOError(f"Error al leer el archivo '{file_path}': {e}")

# Dividir el texto en fragmentos si es necesario
text_fragments = text.split("\n\n")  # Aquí se divide por párrafos o como prefieras

# Conectar con el vector store Pinecone e insertar el texto leído del archivo
try:
    vector_store = VectorStorePinecone.from_texts(
        text_fragments,  # Usamos los fragmentos del texto leídos del archivo
        embeddings,
        index_name=index_name
    )
    print(f"Texto desde '{file_path}' ha sido almacenado en Pinecone exitosamente.")
except Exception as e:
    raise RuntimeError(f"Error al almacenar el texto en Pinecone: {e}")

# Mostrar el estado del índice después de la inserción
try:
    print(pc.Index(index_name).describe_index_stats())
    print("\n")
except Exception as e:
    raise RuntimeError(f"No se pudo obtener el estado del índice '{index_name}': {e}")
