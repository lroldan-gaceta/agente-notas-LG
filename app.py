import os
import streamlit as st
from dotenv import load_dotenv

# 1. Importación moderna
from google import genai

# 2. Carga de variables de entorno
load_dotenv()
client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))

# --- INTERFAZ WEB ---
st.set_page_config(page_title="Asistente Editorial IA", page_icon="📰", layout="centered")

st.title("📰 Evaluador de Notas")
st.subheader("Recibe consejos acerca de tus títulos y secciones")

st.write("Introduce los datos de tu propuesta para recibir el informe de potencial de éxito basado en nuestro histórico de 122k notas.")

# Cajas de entrada de datos para el usuario
titulo_propuesto = st.text_input("Título de la Nota:", placeholder="Ej. El impacto de las nuevas tarifas de luz...")

# Selector de categorías basado en tus secciones reales
seccion_propuesta = st.selectbox(
    "Sección / Categoría:",
    ["Economía", "Sociedad", "Opinión", "Seguridad", "Deportes", "Cultura", "Espectáculos", "LG Play", "Mundo", "Rural", "Servicios y empresas"]
)

# Botón para ejecutar el Agente
if st.button("Evaluar Propuesta"):
    if titulo_propuesto.strip() == "":
        st.warning("Por favor, escribe un título primero.")
    else:
        with st.spinner("Analizando correlaciones históricas e IQL..."):
            
            # --- LÓGICA DEL AGENTE (Tu función) ---
            contexto_datos = "Aquí va tu string resumido de datos del paso anterior..."
            
            prompt = f"""
            Eres un Agente de Inteligencia Artificial experto en Analítica de Medios y Estrategia Editorial.
            Evalúa: Título: "{titulo_propuesto}" | Categoría: "{seccion_propuesta}".
            Basándote en: {contexto_datos}
            Genera el informe analítico estructurado.
            """
            
            try:
                response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                )
                
                # Mostrar el resultado con formato Markdown estético
                st.success("¡Análisis completado!")
                st.markdown("---")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Hubo un error con la API de Gemini: {e}")
