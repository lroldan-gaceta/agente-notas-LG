# Consultor de notas - Evaluador Predictivo de Notas

Este proyecto es un Agente de Inteligencia Artificial desarrollado para optimizar la estrategia editorial de medios digitales. Evalúa propuestas de títulos y categorías antes de su publicación, comparándolas con un histórico de 122,000 registros y métricas avanzadas de rendimiento web extraídas de Google BigQuery (GA4 y Google Search Console).

## Funcionamiento del Código

La aplicación está construida en Python utilizando **Streamlit** para la interfaz de usuario y el SDK unificado de **Google GenAI** (`gemini-2.5-flash`) para el motor de análisis.

1. **Carga de Configuración:** El script inicializa el entorno mediante `python-dotenv` para cargar la clave de API de Gemini de forma segura sin exponerla en el código fuente.
2. **Interfaz de Usuario:** El usuario ingresa un título propuesto y selecciona la categoría o sección correspondiente de la nota.
3. **Procesamiento y Contexto:** El sistema extrae una matriz estadística de rendimiento histórico (que incluye sesiones, usuarios activos, tiempo de interacción medio, impresiones de búsqueda orgánica y CTR medio del sitio como benchmark del 2.27%).
4. **Análisis Predictivo:** Un prompt optimizado bajo técnicas de ingeniería de instrucciones envía el contexto al modelo de lenguaje, el cual devuelve un informe analítico estructurado con scores predictivos, optimización SEO de títulos y recomendaciones estratégicas.

## Despliegue (Deploy)

El proyecto está configurado para ser desplegado de manera ágil y segura en **Streamlit Community Cloud**.

### Requisitos Previos en el Repositorio
* **`.gitignore`**: Configurado correctamente para excluir el archivo local `.env` y las carpetas de caché, evitando la filtración de credenciales.
* **`requirements.txt`**: Contiene las dependencias necesarias para el entorno de producción (`streamlit`, `google-genai`, `python-dotenv`, `pandas`).

### Pasos para el Despliegue
1. Conectar la cuenta de Streamlit Cloud con el repositorio de GitHub correspondiente.
2. Configurar una nueva aplicación apuntando a la rama principal (`main`) y al archivo ejecutable (`app.py`).
3. En la sección **Advanced Settings > Secrets**, declarar la variable de entorno para la API Key de Google:
