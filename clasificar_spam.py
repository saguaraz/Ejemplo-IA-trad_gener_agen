from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Datos de entrenamiento
textos = ["Ganaste un premio dinero gratis", "Hola como estas", "Oferta exclusiva gratis", "Nos vemos mañana en la reunión"]
etiquetas = ["spam", "no_spam", "spam", "no_spam"]

# Procesamiento y entrenamiento
vectorizador = CountVectorizer()
X = vectorizador.fit_transform(textos)
modelo = MultinomialNB()
modelo.fit(X, etiquetas)

# Predicción
# Pide al usuario que ingrese la frase desde la consola
entrada_usuario = input("Ingresa una frase para analizar: ")
nuevo_texto = [entrada_usuario]
X_nuevo = vectorizador.transform(nuevo_texto)
prediccion = modelo.predict(X_nuevo)

print(f"Resultado IA Tradicional: {prediccion[0]}")