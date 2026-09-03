from google import genai
from google.genai import types

API_KEY = "AQ.Ab8RN6LnSjyXnHrjBjGXOb01sePIWtS3sOVVpU9Bxx3SirvHTw"

client = genai.Client(api_key=API_KEY)

# Desactiva la advertencia de Automatic Function Calling (AFC)
config = types.GenerateContentConfig(
    automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True)
)

print("Enviando petición a Gemini...")

respuesta = client.models.generate_content(
    model="gemini-3.6-flash",
    contents="Escribe un correo breve disculpándome por llegar tarde a la reunión de hoy.",
    config=config
)

print("\n--- Respuesta de la IA ---")
print(respuesta.text)