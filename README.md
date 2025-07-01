# Open Reper

Open Reper es una aplicación web desarrollada con [Reflex](https://reflex.dev/) que analiza tu estilo de juego en ajedrez y te recomienda aperturas personalizadas basadas en inteligencia artificial. Utiliza redes neuronales entrenadas con más de 20,000 partidas profesionales para ofrecerte sugerencias adaptadas a tu nivel y preferencias.

## 🎯 Características principales

- **Análisis de estilo de juego**: Detecta tu estilo personal (posicional, agresivo, universal)
- **Recomendación de aperturas**: Sugiere aperturas específicas basadas en tu estilo
- **Recomendación de defensas**: Propone defensas óptimas contra diferentes aperturas
- **Análisis de partidas PGN**: Procesa partidas en formato estándar PGN
- **Interfaz intuitiva**: Diseño responsivo con visualización de tablero interactivo
- **IA avanzada**: Tres modelos especializados para diferentes aspectos del juego

## 🚀 Demo en línea

Puedes probar la aplicación desplegada aquí:  
**[https://open-reper-cyan-grass.reflex.run/](https://open-reper-cyan-grass.reflex.run/)**

## 👥 Autores

- **James Huaman Zumaeta** - [@JamesDroide](https://github.com/JamesDroide)
- **José María Luyo Campos** - [@jmlc643](https://github.com/jmlc643)

## 🛠️ Tecnologías utilizadas

- **Frontend/Backend**: [Reflex](https://reflex.dev/) (Python full-stack)
- **Deep Learning**: TensorFlow/Keras
- **Procesamiento de ajedrez**: python-chess
- **Análisis de datos**: scikit-learn, imbalanced-learn
- **Visualización**: matplotlib, seaborn

## 📦 Instalación local

### Prerrequisitos
- Python 3.8+
- pip

### Pasos de instalación

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/JamesDroide/Open_Reper.git
   cd Open_Reper
   ```

2. **Crea un entorno virtual (recomendado):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecuta la aplicación:**
   ```bash
   reflex run
   ```

5. **Abre tu navegador en:**
   ```
   http://localhost:3000
   ```

## 📁 Estructura del proyecto

```
Open_Reper/
├── open_reper/                    
# Código fuente principal
│   ├── BackEnd/                   
# Lógica del Backend
│   ├── FrontEnd/                  
# Lógica del Frontend
│   ├── components/                  
# Componentes de interfaz
│   │   └── views/                 
# Vistas de la aplicación
│   ├── open_reper.py             
# Aplicación principal
│   └── variables.py              
# Variables globales y configuración
├── models/                        
# Modelos de IA
│   ├── notebooks/                 
# Notebooks de entrenamiento
│   │   ├── ajedrez-*.ipynb       
# Detector de estilos
│   │   ├── detector_aperturas-*.ipynb 
# Recomendador de aperturas
│   │   └── recomendador_defensas-*.ipynb  
# Recomendador de defensas
│   ├── style_detector/           
# Modelo de detección de estilos
│   ├── opening_recommender/      
# Modelo de recomendación de aperturas
│   └── defense_recommender/      
# Modelo de recomendación de defensas
├── assets/                       
# Recursos estáticos
│   ├── game_pieces/             
# Imágenes de piezas de ajedrez
│   ├── logo_open_reper.png      
# Logo de la aplicación
│   └── pieces.png               
# Conjunto de piezas
├── requirements.txt             
# Dependencias de Python
└── README.md                   
# Información acerca del Proyecto
```

## 🤖 Modelos de IA

### 1. Detector de Estilos (`ChessStyleAnalyzer`)
- **Propósito**: Analiza una partida y determina el estilo de juego predominante
- **Estilos detectados**: Posicional, Agresivo, Universal
- **Características**: Extrae más de 300 características por partida

### 2. Recomendador de Aperturas (`OpeningRecommender`)
- **Propósito**: Sugiere aperturas basadas en el estilo detectado
- **Aperturas incluidas**: Catalana, Inglesa, Italiana, Española, Gambitos, etc.
- **Precisión**: >90% en tests de validación

### 3. Recomendador de Defensas (`DefenseRecommender`)
- **Propósito**: Recomienda defensas contra aperturas específicas
- **Defensas incluidas**: Siciliana, Francesa, Caro-Kann, India de Rey, etc.
- **Funcionalidad**: Top 3 defensas por apertura con probabilidades

## 🎮 Cómo usar la aplicación

1. **Sube tu partida**: Carga un archivo PGN o pega el texto de una partida
2. **Análisis automático**: La IA analiza tu estilo de juego
3. **Recibe recomendaciones**: Obtén sugerencias personalizadas de:
   - Aperturas que se adapten a tu estilo
   - Defensas efectivas contra diferentes aperturas
   - Estrategias de jugadores profesionales

## 📊 Entrenamiento de modelos

Los modelos fueron entrenados usando:
- **Dataset**: +20,000 partidas profesionales
- **Técnicas**: Redes neuronales profundas, balanceo de datos (ADASYN)
- **Validación**: Cross-validation y early stopping
- **Métricas**: Precisión y matriz de confusión

Para entrenar los modelos desde cero, consulta los notebooks en [`models/notebooks/`](models/notebooks/).

## 🚀 Despliegue

La aplicación está desplegada usando Reflex Cloud. Para desplegar tu propia instancia:

1. Configura tu cuenta en [Reflex Cloud](https://reflex.dev/)
2. Ejecuta: `reflex deploy`
3. Sigue las instrucciones del CLI

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

## 🙏 Agradecimientos

- Comunidad de [Reflex](https://reflex.dev/) por el excelente framework
- [Lichess](https://lichess.org/) por proporcionar datos de partidas
- Comunidad de ajedrez por inspirar este proyecto

---

**¿Listo para mejorar tu juego de ajedrez con IA? 🚀**

[🌐 Probar la app](https://open-reper-cyan-grass.reflex.run/) | [📖 Documentación](https://deepwiki.com/JamesDroide/Open_Reper) | [🐛 Reportar bug](https://github.com/JamesDroide/Open_Reper/issues)