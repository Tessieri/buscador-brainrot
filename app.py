import streamlit as st
import google.generativeai as genai

# 1. Streamlit busca la clave de forma ultra secreta en sus servidores
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Falta configurar la API Key en los Secrets de Streamlit.")

# 2. Creas la función para consultar al modelo
def preguntar_ia(consulta):
    model = genai.GenerativeModel('gemini-1.5-flash')
    # Configuración para que sea exacto con tus datos (Temperatura 0)
    config = genai.GenerationConfig(temperature=0.0)
    respuesta = model.generate_content(consulta, generation_config=config)
    return respuesta.text
