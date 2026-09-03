from openai import OpenAI

client = OpenAI(api_key="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")

respuesta = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "Eres un asistente redactor de correos."},
        {"role": "user", "content": "Escribe un correo breve disculpándome por llegar tarde a la reunión de hoy."}
    ]
)

print(f"Resultado IA Generativa:\n{respuesta.choices[0].message.content}")