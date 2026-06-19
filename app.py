import streamlit as st
import google.generativeai as genai
import os

# Configuración de la página web
st.set_page_config(page_title="Buscador de Personajes IA", page_icon="🔍", layout="centered")

GEMINI_API_KEY = 'AQ.Ab8RN6LRKlXmJZhz7P-zCjh2q5Nu8Greib1z4qquMNt9YiCRPw'

def preguntar_ia(pregunta, base_datos):
    instrucciones_sistema = (
        "Eres un sistema experto de filtrado de personajes para un videojuego.\n"
        "Procesa las consultas basándote estrictamente en la base de datos proporcionada.\n\n"
        "REGLAS:\n"
        "1. Si te dan personajes separados por comas, da su rareza y bases.\n"
        "2. Sé flexible con errores ortográficos usando aproximación fonética.\n"
        "3. Si piden una categoría completa, lístalos de forma ordenada y pon el conteo total al final.\n\n"
        f"--- BASE DE DATOS ---\n{base_datos}"
    )
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=instrucciones_sistema,
            generation_config={"temperature": 0.2}
        )
        return model.generate_content(pregunta).text
    except Exception as e:
        return f"Error de conexión con la IA: {e}"

# ===== INTERFAZ GRÁFICA DE LA WEB =====
st.title("🤖 Buscador Inteligente de Rarities")

# Verificar si el archivo de personajes existe en el repositorio
if not os.path.exists("personajes.txt"):
    st.error("❌ No se encontró el archivo 'personajes.txt' en GitHub. Por favor, créalo para cargar los datos.")
else:
    with open("personajes.txt", "r", encoding="utf-8") as f:
        MIS_PERSONAJES = f.read()

    st.write("Escribe tu consulta en lenguaje natural (ej: *'dame los miticos con base candy'*).")
    
    # Entrada de texto del usuario
    consulta = st.text_input("🔍 ¿Qué estás buscando hoy?", placeholder="Ej: Nobini, skibidi, miticos...")

    if consulta:
        with st.spinner("La IA está revisando los archivos... 🧭"):
            resultado = preguntar_ia(consulta, MIS_PERSONAJES)
            st.subheader("✨ Resultados:")
            st.info(resultado)
