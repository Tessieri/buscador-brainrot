import streamlit as st
from google import genai
from google.genai import types

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Buscador de Personajes - Brainrot", 
    page_icon="🔍", 
    layout="centered"
)

st.title("🔍 Buscador de Personajes - Brainrot")
st.write("Introduce tu consulta para buscar variantes y rarezas de forma exacta.")

# --- 2. BASE DE DATOS DE PERSONAJES (PROMPT ASISTENTE) ---
INFORMACION_CONTEXTO = """
Eres un buscador experto y estricto para el juego 'Steal a Brainrot' en Roblox.
Tu única fuente de verdad es la lista de personajes que tienes abajo. 
Si el usuario te pide contar o buscar variantes (como 'Candy'), busca de forma literal línea por línea de arriba a abajo.
No inventes personajes ni asumas variantes si no están en este texto de manera explícita.
Cuenta con precisión matemática, asegurándote de revisar toda la lista.

[AQUÍ PEGA TU LISTA COMPLETA DE LOS 62 PERSONAJES CON SUS RARIDADES]
"""

# --- 3. INICIALIZACIÓN SEGURA DEL CLIENTE ---
def conectar_gemini():
    if "GEMINI_API_KEY" in st.secrets:
        try:
            # Usamos el nuevo cliente oficial e independiente de la librería moderna
            return genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
        except Exception as e:
            st.error(f"Error al configurar la conexión de Gemini: {e}")
            return None
    else:
        st.warning("⚠️ La API Key no está configurada en los Secrets de Streamlit. Ve a Settings -> Secrets para agregarla.")
        return None

client = conectar_gemini()

# --- 4. INTERFAZ GRÁFICA Y LÓGICA DE BÚSQUEDA ---
consulta = st.text_input(
    "¿Qué personaje o variante quieres buscar?", 
    placeholder="Ej. ¿Cuántos personajes tienen la variante Candy?"
)

if st.button("Buscar"):
    if not consulta:
        st.info("Por favor, escribe una pregunta primero.")
    elif not client:
        st.error("La IA no está disponible porque falta la API Key o la configuración es incorrecta.")
    else:
        with st.spinner("Escaneando la base de datos con IA..."):
            try:
                # Configuramos los parámetros con el nuevo formato 'types'
                config = types.GenerateContentConfig(
                    temperature=0.0,
                    system_instruction=INFORMACION_CONTEXTO
                )
                
                # Llamada directa al modelo usando el cliente moderno
                resultado = client.models.generate_content(
                    model='gemini-1.5-flash',
                    contents=consulta,
                    config=config
                )
                
                st.success("¡Búsqueda finalizada!")
                st.write(resultado.text)
            except Exception as e:
                st.error(f"Error al procesar la consulta con la IA: {e}")
