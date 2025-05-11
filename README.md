# Open Reper

Open Reper es una aplicación web desarrollada con [Reflex](https://reflex.dev/) que analiza tu estilo de juego en ajedrez y te recomienda aperturas personalizadas. Utiliza una base de datos de más de 20,000 partidas profesionales para ofrecerte sugerencias adaptadas a tu nivel y preferencias.

## Autores

- James Huaman Zumaeta
- José María Luyo Campos

## Características

- Analiza partidas en formato PGN.
- Recomienda aperturas basadas en tu estilo de juego.
- Interfaz intuitiva y responsiva.
- Inspirado en jugadores profesionales y estrategias reales.

## Demo en línea

Puedes probar la aplicación desplegada aquí:  
[https://open-reper-cyan-grass.reflex.run/](https://open-reper-cyan-grass.reflex.run/)

## Instalación local

1. Clona este repositorio:
   ```sh
   git clone https://github.com/tu_usuario/open_reper.git
   cd open_reper
   ```

2. Instala las dependencias:
   ```sh
   pip install -r requirements.txt
   ```

3. Ejecuta la aplicación:
   ```sh
   reflex run
   ```

## Estructura del proyecto

- `open_reper/`: Código fuente principal de la app.
- `models/`: Modelos de IA y utilidades de análisis.
- `assets/`: Imágenes y recursos estáticos.
- `requirements.txt`: Dependencias de Python.
- `ajedrez.ipynb`: Notebook de Google Collab donde está el entrenamiento de nuestra red neuronal.

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

---