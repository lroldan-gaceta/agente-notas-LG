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
                Eres un Agente de IA experto en Ciencia de Datos Aplicada a Medios Digitales y Estrategia Editorial de Alto Rendimiento.

                VALORACIÓN DE PROPUESTA ACTUAL:
                - Título Propuesto: "{titulo_propuesto}"
                - Sección/Categoría: "{seccion_propuesta}"

                CONTEXTO HISTÓRICO COMPLETO (Dataset consolidado de 122k registros + métricas BQ):
                {contexto_datos}

                INSTRUCCIONES DE ANÁLISIS CRÍTICO:
                1. Analiza semánticamente el Título Propuesto y compáralo con los patrones de títulos históricos más exitosos en la sección "{seccion_propuesta}".
                2. Utiliza las métricas de Search Console (Clics, Impresiones, CTR) y Landing Pages del contexto para predecir si este título tiene el potencial de superar el CTR medio del sitio (2.27%) o si necesita optimización SEO.
                3. Evalúa la retención potencial del lector basándote en el histórico de Tiempo de Interacción Medio por Sesión para temas similares.

                FORMATO DE SALIDA EXIGIDO (Devuelve estrictamente esta estructura en Markdown, sé directo, profesional y crítico):

                ### 📊 1. Score de Potencial Predictivo
                - **Tráfico Estimado (Volumen):** [Alto / Medio / Bajo] (Justificar según impresiones históricas de la sección).
                - **CTR Esperado (Atractivo del Título):** [Superior al 2.27% / Inferior al 2.27%] (Analizar si genera urgencia o curiosidad).
                - **Engagement Estimado (Retención):** [Duración esperada alta o baja según tiempo de interacción histórico].

                ### 💡 2. Recomendaciones Editoriales Estratégicas
                - [Recomendación sobre la longitud, el ángulo periodístico o la inclusión de elementos multimedia para mejorar el Tiempo de Interacción según los datos históricos].
                - [Indicar si el tema rinde mejor en formato estándar o requiere optimización para formato móvil/AMP].
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
