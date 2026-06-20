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
            # Configura la clave que guardaste en Secrets
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            
            # Forzamos la inicialización explícita del modelo funcional
            return genai.GenerativeModel(model_name='gemini-1.5-flash')
            
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
    if not consulta:
        st.info("Por favor, escribe una pregunta primero.")
    elif not model:
        st.error("La IA no está disponible porque falta la API Key o la API de Google Cloud está desactivada.")
    else:
        with st.spinner("Escaneando la base de datos con IA..."):
            try:
                # Fijamos temperatura 0.0 para que cuente y busque con precisión total
                config = genai.GenerationConfig(temperature=0.0)
                
                # Unimos tu lista de personajes con lo que escribe el usuario
                prompt_final = f"{INFORMACION_CONTEXTO}\n\nPregunta del usuario: {consulta}"
                
                resultado = model.generate_content(prompt_final, generation_config=config)
                
                st.success("¡Búsqueda finalizada!")
                st.write(resultado.text)
            except Exception as e:
                st.error(f"Error al procesar la consulta con la IA: {e}")
