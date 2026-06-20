import streamlit as st
import google.generativeai as genai

# 1. Configurar la clave de forma segura desde los Secrets
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error("Error al cargar la API Key. Verifica los Secrets en Streamlit.")

# 2. Función para preguntar a la IA (con temperatura 0 para evitar variaciones)
def preguntar_ia(consulta):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        config = genai.GenerationConfig(temperature=0.0)
        resultado = model.generate_content(consulta, generation_config=config)
        return resultado.text
    except Exception as e:
        return f"Error al procesar la consulta: {str(e)}"
