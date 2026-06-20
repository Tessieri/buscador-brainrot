import streamlit as st
import google.generativeai as genai

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Buscador Brainrot", page_icon="🔍", layout="centered")

st.title("🔍 Buscador de Personajes - Brainrot")
st.write("Introduce tu consulta para buscar variantes y rarezas.")

# --- INICIALIZACIÓN SEGURA DE LA IA ---
def conectar_gemini():
    # Buscamos si la clave existe en Secrets sin romper la app
    if "GEMINI_API_KEY" in st.secrets:
        try:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            return genai.GenerativeModel('gemini-1.5-flash')
        except Exception as e:
            st.error(f"Error al configurar Gemini: {e}")
            return None
    else:
        st.warning("⚠️ La API Key no está configurada en los Secrets de Streamlit.")
        return None

model = conectar_gemini()

# --- INTERFAZ GRÁFICA (Aparecerá pase lo que pase) ---
consulta = st.text_input("¿Qué personaje o variante quieres buscar?", placeholder="Ej. Cuantos candys hay?")

if st.button("Buscar"):
    if consulta:
        if model:
            with st.spinner("Buscando en la base de datos con IA..."):
                try:
                    config = genai.GenerationConfig(temperature=0.0)
                    # Aquí puedes concatenar tu lista de personajes al prompt si la tienes guardada
                    resultado = model.generate_content(consulta, generation_config=config)
                    st.success("¡Resultados encontrados!")
                    st.write(resultado.text)
                except Exception as e:
                    st.error(f"Error al procesar la consulta con la IA: {e}")
        else:
            st.error("No se puede realizar la búsqueda porque la IA no está conectada.")
    else:
        st.info("Por favor, escribe una pregunta primero.")
