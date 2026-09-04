from openai import OpenAI

client = OpenAI(api_key="")

respuesta = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "Eres un asistente redactor de correos."},
        {"role": "user", "content": "Escribe un correo breve disculpándome por llegar tarde a la reunión de hoy."}
    ]
)

print(f"Resultado IA Generativa:\n{respuesta.choices[0].message.content}")