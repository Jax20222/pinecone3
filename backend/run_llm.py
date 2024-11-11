import os
from langchain_openai import ChatOpenAI

# Obtener la clave de API de OpenAI desde las variables de entorno
openai_api_key = os.environ.get('OPENAI_API_KEY')
if not openai_api_key:
    raise ValueError("La variable de entorno 'OPENAI_API_KEY' no está configurada.")

# Crear la instancia de ChatOpenAI
try:
    llm = ChatOpenAI(api_key=openai_api_key)
except Exception as e:
    raise RuntimeError(f"Error al crear la instancia de ChatOpenAI: {e}")

# Invocar al modelo con un mensaje de prueba
try:
    response = llm.invoke("Hello, world!")
    # Imprimir la respuesta del modelo
    print(response)
except Exception as e:
    raise RuntimeError(f"Error al invocar el modelo de OpenAI: {e}")
