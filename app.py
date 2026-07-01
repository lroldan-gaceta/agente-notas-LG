import os
import json
import streamlit as st
from dotenv import load_dotenv

# 1. Importación moderna de la SDK de Google GenAI
from google import genai

# 2. Carga de variables de entorno
load_dotenv()

# Asegura compatibilidad leyendo tanto la variable estándar de la nueva SDK como la anterior
api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

# 3. Función optimizada para cargar la matriz combinada generada en el entorno
@st.cache_data
def cargar_matriz_conocimiento():
    ruta_matriz = "data/matriz_conocimiento_editorial.json"
    if os.path.exists(ruta_matriz):
        try:
            with open(ruta_matriz, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"Error al leer el archivo de la matriz: {e}")
            return {}
    else:
        st.error(f"No se encontró el archivo '{ruta_matriz}'. Asegúrate de ejecutar primero el script que consolida la matriz combinada.")
        return {}

# Cargamos el diccionario dinámico de la base de conocimiento
matriz_secciones = cargar_matriz_conocimiento()

# --- INTERFAZ WEB ---
st.set_page_config(page_title="Asistente Editorial IA", page_icon="📰", layout="centered")

st.title("📰 Evaluador de Notas Predictivo")
st.subheader("Recibe consejos editoriales basados en telemetría actual e histórica")

st.write("Introduce los datos de tu propuesta para recibir un informe profundo de potencial de éxito contrastado con métricas actuales de BigQuery e históricos consolidados (2024-2025).")

# Cajas de entrada de datos para el usuario
titulo_propuesto = st.text_input("Título de la Nota:", placeholder="Ej. El impacto de las nuevas tarifas de luz...")

# Mapeamos los selectores basados en las secciones reales disponibles en tus datos
secciones_disponibles = list(matriz_secciones.keys()) if matriz_secciones else [
    "Economía", "Sociedad", "Opinión", "Seguridad", "Deportes", 
    "Cultura", "Espectáculos", "LG Play", "Mundo", "Rural", "Servicios y empresas"
]

seccion_propuesta = st.selectbox("Sección / Categoría:", secciones_disponibles)

# Botón para ejecutar el Agente
if st.button("Evaluar Propuesta"):
    if titulo_propuesto.strip() == "":
        st.warning("Por favor, escribe un título primero.")
    elif not matriz_secciones:
        st.error("La matriz de conocimiento no se encuentra cargada o está vacía.")
    else:
        with st.spinner("Realizando análisis cruzado de eras de datos y telemetría de UX..."):
            
            # --- INYECCIÓN TANGIBLE DEL CONTEXTO DE DOBLE ERA ---
            # Extraemos el fragmento exacto de la matriz que le corresponde a la categoría seleccionada
            datos_contexto_seccion = matriz_secciones.get(seccion_propuesta, {})
            
            # Lo convertimos a una cadena JSON limpia y formateada para el prompt
            contexto_datos_json = json.dumps(datos_contexto_seccion, ensure_ascii=False, indent=2)
            
            # --- PROMPT ADECUADO PARA ANÁLISIS DE DOS PERSPECTIVAS ---
            prompt = f"""
Eres un Agente de IA experto en Ciencia de Datos Aplicada a Medios Digitales y Estrategia Editorial de Alto Rendimiento.

VALORACIÓN DE PROPUESTA ACTUAL DEL REDACTOR:
- Título Propuesto: "{titulo_propuesto}"
- Sección/Categoría: "{seccion_propuesta}"

MÉTRICAS TANGIBLES AGREGADAS DE NUESTRO ENTORNO PARA LA SECCIÓN "{seccion_propuesta}":
{contexto_datos_json}

INSTRUCCIONES DE ANÁLISIS CRÍTICO Y COMPARATIVO:
1. **Perspectiva de Rendimiento Actual**: Utiliza los indicadores vigentes (`vistas_promedio_actual`, `iql_interaccion_promedio_actual` y `total_suscripciones_actual`) para determinar el potencial inmediato de tracción que tiene este título frente al estándar actual de producción de la categoría.
2. **Perspectiva de Contexto Histórico General (2024-2025)**: Evalúa el comportamiento de largo plazo utilizando todas las variables históricas adjuntas. Analiza si enfoques semánticos similares requerían históricamente mayor longitud de texto (`longitud_caracteres_promedio_hist`), si el impacto de incluir videos en esa sección era crucial (`porcentaje_notas_con_video_hist`), el scroll medio alcanzado o si la polarización del sentimiento (`sentimiento_promedio_hist`) afectaba la conversión. 
3. **Paralelismo Temporal**: Establece un análisis predictivo indicando si este tema replica un patrón cíclico exitoso del pasado o si la tendencia de consumo actual en 2026 demuestra un enfriamiento/cambio de comportamiento de los usuarios en comparación al periodo previo.

FORMATO DE SALIDA EXIGIDO (Devuelve estrictamente esta estructura en Markdown. Sé directo, profesional, crítico y matemático):

### 📊 1. Score de Potencial Predictivo (Estado Actual)
- **Tráfico Estimado (Volumen de Entrada):** [Alto / Medio / Bajo] (Justificar y contrastar de manera directa contra la métrica `vistas_promedio_actual`).
- **Conversión a Suscripción:** [Alta / Media / Baja] (Estimar según la capacidad transaccional actual reflejada en `total_suscripciones_actual`).
- **Retención Estimada de Audiencia:** [Alta / Media / Baja] (Calificar según el rendimiento de interacciones bajo `iql_interaccion_promedio_actual`).

### ⏳ 2. Paralelismo y Contexto de Tendencia Histórica (2024-2025)
- **Análisis de Variables de Largo Plazo:** [Realiza una comparación directa. Por ejemplo, analiza si el scroll histórico de la sección `scroll_promedio_hist` o el enganche por tiempo justifican estructurar la nota con mayor longitud, apoyarse fuertemente en redes según el promedio de compartidos previos, o si es un requerimiento mandatorio la inclusión de elementos multimedia/video].
- **Evolución del Consumo:** [Explica de manera analítica si el rendimiento óptimo del pasado se ha enfriado en la actualidad o si la temática propuesta sigue manteniendo vigencia temporal].

### 🎯 3. Optimización y Alternativas Editoriales
*Escribe una breve crítica analítica sobre el enfoque gramatical del título original.*
- **Opción A (Maximizando Descubrimiento SEO y Tráfico Orgánico):** [Propuesta alternativa de título]
- **Opción B (Maximizando Viralidad, Interacción IQL y Conversión):** [Propuesta alternativa de título]
"""
            
            try:
                # Ejecución de la consulta utilizando el cliente moderno
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                )
                
                # Renderizado estético del informe en la aplicación web
                st.success("¡Análisis de datos combinado completado con éxito!")
                st.markdown("---")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Hubo un error al procesar la solicitud con la API de Gemini: {e}")