import openai
from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Cargar la clave de la API
openai.api_key = os.getenv("OPENAI_API_KEY")

def chatbot(messages):
    response = openai.chat.completions.create(model="gpt-4o-mini",  # O usa "gpt-3.5-turbo" si prefieres
    messages=messages)
    return response.choices[0].message.content

# Inicializar la conversación con el bot
messages = [
    {"role": "system", "content": "Eres un asistente útil y amable."}
]

while True:
    user_input = input("Tú: ")
    if user_input.lower() == 'salir':
        break
    messages.append({"role": "user", "content": user_input})
    bot_response = chatbot(messages)
    print(f"Bot: {bot_response}")
    messages.append({"role": "assistant", "content": bot_response})
