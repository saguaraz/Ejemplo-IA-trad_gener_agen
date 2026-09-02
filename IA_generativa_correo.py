import google.generativeai as genai

# Reemplaza el texto entre comillas con la clave obtenida en Google AI Studio (empieza con AIzaSy...)
API_KEY = "AQ.Ab8RN6K9Tx9qgL2HUI3rMcytxC4559JalPCwzLUPyEk_Z4O8BQ"

genai.configure(api_key=API_KEY)

# Configuración e invocación del modelo
model = genai.GenerativeModel("gemini-1.5-flash")

respuesta = model.generate_content(
    "Escribe un correo breve disculpándome por llegar tarde a la reunión de hoy."
)

print(f"Resultado IA Generativa:\n{respuesta.text}")