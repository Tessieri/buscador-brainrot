import streamlit as st
import google.generativeai as genai

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

# --- 3. INICIALIZACIÓN SEGURA DE LA IA ---
def conectar_gemini():
    if "GEMINI_API_KEY" in st.secrets:
        try:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            # Usamos directamente el prefijo completo de la API que es el estándar requerido en entornos Cloud
            return genai.GenerativeModel('models/gemini-1.5-flash')
        except Exception as e:
            st.error(f"Error al configurar la conexión de Gemini: {e}")
            return None
    else:
        st.warning("⚠️ La API Key no está configurada en los Secrets de Streamlit. Ve a Settings -> Secrets para agregarla.")
        return None

model = conectar_gemini()

# --- 4. INTERFAZ GRÁFICA Y LÓGICA DE BÚSQUEDA ---
consulta = st.text_input(
    "¿Qué personaje o variante quieres buscar?", 
    placeholder="Ej. ¿Cuántos personajes tienen la variante Candy?"
)

if st.button("Buscar"):
    if consulta:
        if model:
            with st.spinner("Escaneando la base de datos con IA..."):
                try:
                    # Forzamos temperatura 0.0 para máxima precisión (cero creatividad)
                    config = genai.GenerationConfig(temperature=0.0)
                    
                    # Combinamos el contexto de los personajes con la pregunta
                    prompt_final = f"{INFORMACION_CONTEXTO}\n\nPregunta del usuario: {consulta}"
                    
                    resultado = model.generate_content(prompt_final, generation_config=config)
                    
                    st.success("¡Búsqueda finalizada!")
                    st.write(resultado.text)
                except Exception as e:
                    st.error(f"Error al procesar la consulta con la IA: {e}")
        else:
            st.error("La IA no está disponible porque falta la API Key o hay un problema de configuración.")
    else:
        st.info("Por favor, escribe una pregunta primero.")
