import time
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage
from ddgs import DDGS

# 1. Cargar las credenciales desde .env
load_dotenv()

# --- Definición de Herramientas ---
@tool
def calcular_matematica(expresion: str) -> str:
    """Útil para realizar cálculos matemáticos numéricos. Ejemplo de entrada: '345 * 12 / 2'"""
    try:
        return str(eval(expresion))
    except Exception as e:
        return f"Error al calcular: {e}"

@tool
def buscar_en_web(consulta: str) -> str:
    """Útil para buscar información actualizada en internet sobre cualquier tema."""
    try:
        results = list(DDGS().text(keywords=consulta, max_results=3))
        if not results:
            return "No se encontraron resultados en la búsqueda web."
        
        respuesta = ""
        for item in results:
            respuesta += f"Título: {item.get('title')}\nResumen: {item.get('body')}\n\n"
        return respuesta
    except Exception as e:
        return f"Error en la búsqueda: {e}"

tools = [calcular_matematica, buscar_en_web]
tools_by_name = {tool.name: tool for tool in tools}

# 2. Inicialización de Gemini 3.6 Flash
llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    max_retries=3
)
llm_with_tools = llm.bind_tools(tools)

# 3. Función de ejecución agéntica con manejo de cuota
def ejecutar_agente(pregunta_usuario: str, max_iteraciones: int = 3):
    print(f"Pregunta: {pregunta_usuario}\n")
    messages = [HumanMessage(content=pregunta_usuario)]
    
    for i in range(max_iteraciones):
        time.sleep(3)  # Control del ritmo de peticiones
        
        exito = False
        intentos = 0
        ai_msg = None
        
        # Bucle de reintento si salta un error de tasa/cuota temporal
        while not exito and intentos < 3:
            try:
                ai_msg = llm_with_tools.invoke(messages)
                exito = True
            except Exception as e:
                intentos += 1
                if "RESOURCE_EXHAUSTED" in str(e):
                    print(f"\n[Aviso]: Cuota o frecuencia excedida. Esperando 20 segundos para reintentar (Intento {intentos}/3)...")
                    time.sleep(20)
                else:
                    print(f"\n[Error no recuperable]: {e}")
                    return

        if not ai_msg:
            print("\nNo se pudo obtener respuesta del modelo tras varios reintentos.")
            return

        messages.append(ai_msg)
        
        # Si el modelo responde directamente sin llamar herramientas
        if not ai_msg.tool_calls:
            print("\n--- Respuesta Final ---")
            print(ai_msg.content)
            return
            
        # Ejecutar herramientas llamadas por el modelo
        for tool_call in ai_msg.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            tool_id = tool_call["id"]
            
            print(f"-> Invocando herramienta: {tool_name}")
            print(f"   Parámetros: {tool_args}")
            
            selected_tool = tools_by_name[tool_name]
            tool_output = selected_tool.invoke(tool_args)
            
            messages.append(ToolMessage(content=str(tool_output), tool_call_id=tool_id))

    print("\n--- Proceso finalizado ---")

if __name__ == "__main__":
    print("Iniciando Agente Multi-Herramienta (gemini-3.6-flash)...\n")
    ejecutar_agente("¿Cuáles son algunas noticias recientes en la astronomía?")