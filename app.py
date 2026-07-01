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

# 3. Función optimizada con ruta absoluta dinámica
@st.cache_data
def cargar_matriz_conocimiento():
    # Encuentra la carpeta exacta donde reside este archivo app.py
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    
    # Construye la ruta uniendo de forma absoluta: carpeta_de_app_py -> data -> archivo.json
    ruta_matriz = os.path.join(directorio_actual, "data", "matriz_conocimiento_editorial.json")
    
    if os.path.exists(ruta_matriz):
        try:
            with open(ruta_matriz, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"Error al leer el archivo de la matriz: {e}")
            return {}
    else:
        # Esto te mostrará en la interfaz de Streamlit la ruta REAL exacta que está buscando el sistema
        st.error(f"No se encontró el archivo en la ruta física: '{ruta_matriz}'.")
        return {}

# Cargamos el diccionario dinámico de la base de conocimiento
matriz_secciones = cargar_matriz_conocimiento()

# --- INTERFAZ WEB MEJORADA ---
st.set_page_config(page_title="Asistente Editorial IA", page_icon="📰", layout="centered")

st.title("📰 Evaluador de Notas")
st.subheader("Optimiza tus títulos y valida la mejor sección para tus notas")

st.write(
    "Introduce los datos de tu propuesta. Nuestro Agente de IA analizará la semántica del título "
    "y la telemetría de la categoría para darte títulos alternativos y **sugerirte si es conveniente "
    "cambiar la nota de sección** para maximizar su impacto según nuestro histórico de 122k notas."
)
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
- Sección/Categoría Tentativa: "{seccion_propuesta}"

MÉTRICAS TANGIBLES AGREGADAS DE NUESTRO ENTORNO PARA LA SECCIÓN "{seccion_propuesta}":
{contexto_datos_json}

INSTRUCCIONES DE ANÁLISIS CRÍTICO Y REUBICACIÓN TAXONÓMICA:
1. **Auditoría de Sección/Categoría (Crucial)**: Analiza semánticamente si el Título Propuesto encaja perfectamente en "{seccion_propuesta}". Cruzando los datos históricos de scroll (`scroll_promedio_hist`), engagement (`iql_interaccion_promedio_actual`) y conversiones de esta categoría, dictamina de forma crítica si la nota debe mantenerse en "{seccion_propuesta}" o si, por el contrario, su temática suele performar con métricas significativamente más altas si se publicara en otra sección alternativa (por ejemplo: Economía vs. Servicios y empresas, o Sociedad vs. LG Play).
2. **Perspectiva de Rendimiento**: Utiliza los indicadores vigentes y de largo plazo para predecir el impacto en tráfico orgánico, fidelidad de lectores habituales (`usuarios_fieles_loyal`) y conversiones si se conserva la configuración propuesta.
3. **Optimización de Título**: Evalúa la urgencia, el clickbait negativo vs. el interés genuino, y la estructura SEO del título original.

FORMATO DE SALIDA EXIGIDO (Devuelve estrictamente esta estructura en Markdown. Sé directo, sumamente profesional, analítico y cuantitativo):

### 📊 1. Score de Potencial Predictivo (En Sección Tentativa)
- **Tráfico Estimado (Volumen de Entrada):** [Alto / Medio / Bajo] (Justificar contrastando contra la métrica `vistas_promedio_actual`).
- **Conversión a Suscripción:** [Alta / Media / Baja] (Estimar según la capacidad transaccional reflejada en `total_suscripciones_actual`).
- **Retención Estimada de Audiencia:** [Alta / Media / Baja] (Calificar según el rendimiento de interacciones bajo `iql_interaccion_promedio_actual`).

### 🗂️ 2. Dictamen de Sección y Taxonomía Recomendada
- **¿Es la sección correcta?:** [**MANTENER EN SECCIÓN** / **RECOMENDACIÓN DE CAMBIO DE SECCIÓN**]
- **Justificación Editorial:** [Explica científicamente si la temática rinde mejor aquí o si el perfil de usuario de otra sección del diario se ajusta más. Si recomiendas un cambio, especifica a qué sección exacta y por qué variables métricas, como mayor scroll medio previo o más conversiones en ese nicho].

### 💡 3. Paralelismo y Requerimientos de Formato
- **Análisis de Variables de Largo Plazo:** [Analiza si el scroll histórico de la sección justifica estructurar la nota con mayor longitud, apoyarse fuertemente en redes según el promedio de compartidos previos, o si es un requerimiento mandatorio la inclusión de elementos multimedia/video debido a los históricos de la categoría].

### 🎯 4. Optimización Gramatical y Títulos Alternativos
*Escribe una breve crítica analítica sobre el enfoque del título original escrito por el redactor.*
- **Opción A (Optimizada para Tráfico Orgánico y SEO):** [Propuesta alternativa de título manteniendo la esencia de la sección final recomendada]
- **Opción B (Optimizada para Engagement IQL, Redes y Conversión):** [Propuesta alternativa de título de alto impacto para suscriptores]
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
