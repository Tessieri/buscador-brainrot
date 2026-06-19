import streamlit as st
import google.generativeai as genai
import os
import json

# Configuración de la página web
st.set_page_config(page_title="Buscador de Personajes IA", page_icon="🔍", layout="centered")

GEMINI_API_KEY = 'AQ.Ab8RN6LRKlXmJZhz7P-zCjh2q5Nu8Greib1z4qquMNt9YiCRPw'

def preguntar_ia(pregunta, base_datos_json):
    instrucciones_sistema = (
        "Eres un sistema experto y riguroso de filtrado de personajes para un videojuego.\n"
        "Se te proporcionará la base de datos exacta en formato JSON. Cada personaje tiene su 'rareza' y una lista de 'bases' que pinta.\n\n"
        "REGLAS CRÍTICAS:\n"
        "1. Si el usuario pide personajes sueltos (ej: Nobini, Skibidi), busca en el JSON y responde con su rareza exacta y TODAS las bases asociadas a él. No omitas ninguna.\n"
        "2. Si piden un filtro (ej: 'que pinten lava' o 'quienes son miticos'), revisa minuciosamente TODO el JSON, genera una lista ordenada de los que cumplan la condición y muestra el total exacto al final.\n"
        "3. Sé extremadamente flexible con la ortografía del usuario usando aproximación fonética para encontrar el personaje correcto.\n\n"
        f"--- BASE DE DATOS (JSON) ---\n{base_datos_json}"
    )
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=instrucciones_sistema,
            generation_config={"temperature": 0.1} # Bajamos la temperatura a 0.1 para que sea más exacto y no invente nada
        )
        return model.generate_content(pregunta).text
    except Exception as e:
        return f"Error de conexión con la IA: {e}"

# ===== INTERFAZ GRÁFICA DE LA WEB =====
st.title("🤖 Buscador Inteligente de Rarities")

# Verificar si el archivo JSON existe
if not os.path.exists("personajes.json"):
    st.error("❌ No se encontró el archivo 'personajes.json' en GitHub. Por favor, créalo para cargar los datos.")
else:
    with open("personajes.json", "r", encoding="utf-8") as f:
        MIS_PERSONAJES = f.read()

    st.write("Escribe tu consulta en lenguaje natural (ej: *'que personajes tienen base cyber'*).")
    
    # Entrada de texto del usuario
    consulta = st.text_input("🔍 ¿Qué estás buscando hoy?", placeholder="Ej: Nobini, miticos, base lava...")

    if consulta:
        with st.spinner("La IA está analizando minuciosamente la base de datos... 🧭"):
            resultado = preguntar_ia(consulta, MIS_PERSONAJES)
            st.subheader("✨ Resultados:")
            st.info(resultado)
        resultado = preguntar_ia(consulta)
        st.subheader("✨ Resultados:")
        st.info(resultado)
