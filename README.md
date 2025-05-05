# Interactive Web for Soccer Match Analysis

## Descripción general del proyecto

Este proyecto es una aplicación web interactiva diseñada para el análisis y visualización de datos de partidos de fútbol. La plataforma está enfocada en proporcionar estadísticas detalladas y comparaciones entre equipos y jugadores. Utiliza **Streamlit** para generar paneles visuales dinámicos que permiten explorar métricas clave, como goles, asistencias, estadísticas de defensa, y mucho más. Los analistas y scouts pueden usar esta herramienta para evaluar el rendimiento de jugadores de manera objetiva, basándose en datos cuantificables.

## Requisitos para ejecutarse

Para ejecutar la aplicación localmente, asegúrate de tener instalado:

- **Python 3.9** o superior
- **pip** (gestor de paquetes de Python)

Además, se recomienda utilizar un entorno virtual (por ejemplo, usando **venv** o **conda**) para mantener las dependencias del proyecto organizadas y evitar conflictos con otras aplicaciones Python que puedas tener instaladas.

## Instalación


Sigue estos pasos para instalar y ejecutar la aplicación en tu entorno local:

1. **Clonar el repositorio**:
   Clona el repositorio en tu máquina local:
   ```bash
   git clone git@github.com:3zavalam/Ing-Software.git
   cd Ing-Software
   ```

2. **Crear un entorno virtual e instalar las dependencias**:
   Crea un entorno virtual para gestionar las dependencias del proyecto. Esto asegura que las bibliotecas necesarias no entren en conflicto con otros proyectos de Python que puedas tener instalados.
   ```bash
   python -m venv env
   source env/bin/activate  
   pip install -r requirements.txt
   ```

3. **Ejecutar la aplicación**:
   Una vez que las dependencias estén instaladas, puedes ejecutar la aplicación de la siguiente manera:
   ```bash
   streamlit run app.py
   ```
   Esto abrirá la aplicación en tu navegador predeterminado.