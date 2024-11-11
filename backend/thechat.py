import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_pinecone import PineconeVectorStore
from langchain import hub
from pinecone import Pinecone

# Configurar las API keys desde las variables de entorno
pinecone_api_key = os.environ.get('PINECONE_API_KEY')
openai_api_key = os.environ.get('OPENAI_API_KEY')
if not pinecone_api_key or not openai_api_key:
    raise ValueError("Las variables de entorno 'PINECONE_API_KEY' y 'OPENAI_API_KEY' deben estar configuradas.")

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

# Crear los embeddings con OpenAI
try:
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
except Exception as e:
    raise RuntimeError(f"Error al crear los embeddings con OpenAI: {e}")

# Crear un retriever utilizando PineconeVectorStore
try:
    retriever = PineconeVectorStore(
        index=index,
        embedding=embeddings,  # Pasamos los embeddings aquí
        namespace=namespace
    ).as_retriever()
except Exception as e:
    raise RuntimeError(f"Error al configurar el retriever: {e}")

# Obtener el prompt de Retrieval QA Chat desde el hub de langchain
try:
    retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
except Exception as e:
    raise RuntimeError(f"Error al obtener el prompt desde el hub de Langchain: {e}")

# Configurar el LLM de OpenAI (ChatGPT)
try:
    llm = ChatOpenAI(
        openai_api_key=openai_api_key,
        model_name='gpt-4',  # Puedes cambiar el modelo según tu preferencia
        temperature=0.0  # Controlar la creatividad del modelo (0.0 es más preciso)
    )
except Exception as e:
    raise RuntimeError(f"Error al configurar el LLM de OpenAI: {e}")

# Recuperar los documentos relevantes utilizando invoke()
try:
    docs = retriever.invoke("¿Qué es RASA AI?")
except Exception as e:
    raise RuntimeError(f"Error al recuperar documentos: {e}")

# Crear la cadena que combina los documentos recuperados con el LLM
try:
    combine_docs_chain = create_stuff_documents_chain(
        llm, retrieval_qa_chat_prompt
    )
except Exception as e:
    raise RuntimeError(f"Error al crear la cadena de combinación de documentos: {e}")

# Función para hacer preguntas y obtener respuestas
def hacer_pregunta(query):
    try:
        response = combine_docs_chain.invoke({
            "context": docs,
            "input": query  # Pasamos la consulta original como input
        })
        return response
    except Exception as e:
        raise RuntimeError(f"Error al obtener respuesta para la consulta '{query}': {e}")

# PREGUNTAS

# Primera pregunta
query1 = "¿Cuáles son las principales características de RASA AI?"
response1 = hacer_pregunta(query1)
print(f"Respuesta a la primera pregunta:\n{response1}\n")

# Segunda pregunta
query2 = "¿Qué componentes principales tiene RASA AI?"
response2 = hacer_pregunta(query2)
print(f"Respuesta a la segunda pregunta:\n{response2}\n")

# Tercera pregunta
query3 = "¿Cuáles son las dos principales partes que componen el framework de RASA AI?"
response3 = hacer_pregunta(query3)
print(f"Respuesta a la tercera pregunta:\n{response3}\n")

# Cuarta pregunta
query4 = "Mi asistente RASA no está comprendiendo las intenciones correctamente. ¿Qué debo revisar primero?"
response4 = hacer_pregunta(query4)
print(f"Respuesta a la cuarta pregunta:\n{response4}\n")
