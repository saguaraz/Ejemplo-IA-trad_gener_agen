import os
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

@tool
def leer_archivo_local(ruta_archivo: str) -> str:
    """Útil para leer el contenido de un archivo de texto o datos local (.txt, .csv, .json, .md).
    Entrada: la ruta relativa o absoluta del archivo."""
    try:
        if not os.path.exists(ruta_archivo):
            return f"Error: El archivo en '{ruta_archivo}' no existe."
        
        # Límite de seguridad: 100 KB para evitar lecturas masivas que colapsen el contexto
        tamanio = os.path.getsize(ruta_archivo)
        if tamanio > 100 * 1024:
            return f"Error: El archivo es demasiado grande ({tamanio / 1024:.2f} KB). El límite es 100 KB."
            
        with open(ruta_archivo, "r", encoding="utf-8", errors="ignore") as f:
            contenido = f.read()
            
        return contenido if contenido.strip() else "El archivo está vacío."
    except Exception as e:
        return f"Error al leer el archivo: {e}"

tools = [calcular_matematica, buscar_en_web, leer_archivo_local]
tools_by_name = {tool.name: tool for tool in tools}

# 2. Inicialización de Gemini 3.6 Flash
llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    max_retries=3
)
llm_with_tools = llm.bind_tools(tools)

# 3. Función de ejecución agéntica
def ejecutar_agente(pregunta_usuario: str, max_iteraciones: int = 4):
    print(f"Pregunta: {pregunta_usuario}\n")
    messages = [HumanMessage(content=pregunta_usuario)]
    
    for i in range(max_iteraciones):
        time.sleep(3)
        
        exito = False
        intentos = 0
        ai_msg = None
        
        while not exito and intentos < 3:
            try:
                ai_msg = llm_with_tools.invoke(messages)
                exito = True
            except Exception as e:
                intentos += 1
                if "RESOURCE_EXHAUSTED" in str(e):
                    print(f"\n[Aviso]: Límite alcanzado. Esperando 20s...")
                    time.sleep(20)
                else:
                    print(f"\n[Error no recuperable]: {e}")
                    return

        if not ai_msg:
            return

        messages.append(ai_msg)
        
        if not ai_msg.tool_calls:
            print("\n--- Respuesta Final ---")
            print(ai_msg.content)
            return
            
        for tool_call in ai_msg.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            tool_id = tool_call["id"]
            
            print(f"-> Invocando herramienta: {tool_name}")
            print(f"   Parámetros: {tool_args}")
            
            selected_tool = tools_by_name[tool_name]
            tool_output = selected_tool.invoke(tool_args)
            
            messages.append(ToolMessage(content=str(tool_output), tool_call_id=tool_id))

if __name__ == "__main__":
    print("Iniciando Agente Multi-Herramienta con acceso a archivos...\n")
    
    # Prueba: Leer el propio archivo requirements.txt y contar cuántas librerías hay
    ejecutar_agente("Lee el archivo local 'requirements.txt', dime qué librerías contiene y cuántas son en total.")