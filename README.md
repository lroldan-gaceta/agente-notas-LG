# 📰 Consultor de Notas - Evaluador Predictivo y Optimizador Editorial

Este proyecto es un Agente de Inteligencia Artificial de alto rendimiento desarrollado para optimizar la estrategia editorial de medios digitales y redacciones modernas. Su objetivo principal es auditar propuestas de títulos y taxonomías de secciones antes de su publicación para maximizar el tráfico, el engagement y las conversiones.

A diferencia de un corrector común, este agente realiza un **análisis predictivo cruzado** comparando la propuesta con un histórico de 122,000 registros y matrices de telemetría web avanzada extraídas de Google BigQuery (Google Analytics 4 y Google Search Console).

## 🚀 Características Principales
* **Optimización Semántica de Títulos:** Evalúa la estructura gramatical, longitud y el enfoque SEO/viral del título propuesto.
* **Auditoría Temática de Secciones:** Analiza si la temática del artículo realmente pertenece a la sección sugerida por el periodista o si rinde matemáticamente mejor en otra categoría del medio (por ejemplo, mover una nota de *Economía* a *Sociedad* basado en métricas históricas de retención y scroll).
* **Predicción de Telemetría (Doble Era):** Cruza datos de rendimiento actual inmediato con patrones históricos de comportamiento de largo plazo (2024-2025).

## 🛠️ Funcionamiento del Código

La aplicación está construida en Python utilizando **Streamlit** para la interfaz dinámica y el SDK unificado de **Google GenAI** (`gemini-2.5-flash`) como motor cognitivo.

1. **Carga y Consolidación Express:** Si la matriz de conocimiento no existe en el servidor, el script analiza los datasets `.jsonl` en segundos y genera un nodo analítico estructurado por sección.
2. **Interfaz de Entrada:** El redactor ingresa su propuesta de título y una categoría inicial tentativa.
3. **Inyección Quirúrgica de Contexto:** El sistema extrae en tiempo real las métricas agregadas de esa categoría (vistas, scroll medio, conversiones, presencia de video, engagement index IQL y sentimiento).
4. **Análisis Crítico:** Un prompt optimizado bajo técnicas avanzadas de ingeniería de instrucciones audita la propuesta y devuelve recomendaciones editoriales críticas y predictivas en formato Markdown.

## 📦 Despliegue (Deploy)

El proyecto está optimizado para su ejecución continua en **Streamlit Community Cloud**.

### Requisitos en el Repositorio
* **`.gitignore`**: Configurado correctamente para excluir credenciales locales y archivos pesados innecesarios.
* **`requirements.txt`**: Dependencias de producción fijadas (`streamlit`, `google-genai`, `python-dotenv`, `pandas`).

### Pasos para Desplegar
1. Conecta tu cuenta de Streamlit Cloud al repositorio de GitHub.
2. Selecciona la rama principal (`main`) y define `app.py` como el archivo ejecutable.
3. En **Advanced Settings > Secrets**, declara tu clave de acceso:
   ```toml
   GEMINI_API_KEY = "tu_api_key_aqui"
