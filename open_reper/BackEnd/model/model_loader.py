import os
import warnings
import numpy as np
import joblib

# Suprimir warnings de deprecación de TFLite
warnings.filterwarnings('ignore', category=UserWarning, module='tensorflow.lite.python.interpreter')

import tensorflow as tf
from models.style_detector.chess_model import ChessStyleAnalyzer
from models.opening_recommender.opening_recommender_model import OpeningRecommender
from models.defense_recommender.defense_recommender_model import DefenseRecommender


class TFLiteModel:
    """Modelo TFLite puro sin dependencia de archivos Keras"""
    
    def __init__(self, tflite_path, metadata_path, model_class_instance):
        self.tflite_path = tflite_path
        self.metadata_path = metadata_path
        self.model_class = model_class_instance
        
        # Cargar modelo TFLite
        if not os.path.exists(tflite_path):
            raise FileNotFoundError(f"Archivo TFLite no encontrado: {tflite_path}")
        
        self.interpreter = tf.lite.Interpreter(model_path=tflite_path)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        
        # Cargar metadatos (scaler, encoder, etc.)
        if os.path.exists(metadata_path):
            self.metadata = joblib.load(metadata_path)
        else:
            raise FileNotFoundError(f"Archivo de metadatos no encontrado: {metadata_path}")
        
        print(f"Modelo TFLite cargado: {os.path.basename(tflite_path)}")
    
    def predict(self, X, verbose=0, **kwargs):
        """Predicción usando TFLite"""
        # Convertir input a float32
        input_data = np.array(X, dtype=np.float32)
        
        # Si es un array 1D, expandir dimensiones
        if len(input_data.shape) == 1:
            input_data = np.expand_dims(input_data, axis=0)
        
        # Establecer el tensor de entrada
        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
        
        # Ejecutar inferencia
        self.interpreter.invoke()
        
        # Obtener resultado
        output_data = self.interpreter.get_tensor(self.output_details[0]['index'])
        
        return output_data
    
    def __getattr__(self, name):
        """Delegar atributos a los metadatos o clase del modelo"""
        if 'metadata' in self.__dict__ and name in self.metadata:
            return self.metadata[name]
        if 'model_class' in self.__dict__:
            return getattr(self.model_class, name)
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")


def load_tflite_model(model_class_instance, tflite_path, metadata_path):
    """Carga un modelo TFLite puro (sin archivos Keras)"""
    tflite_model = TFLiteModel(tflite_path, metadata_path, model_class_instance)
    
    # Inyectar el método predict en la instancia del modelo
    model_class_instance.model = tflite_model
    model_class_instance.scaler = tflite_model.metadata.get('scaler')
    model_class_instance.label_encoder = tflite_model.metadata.get('label_encoder')
    
    return model_class_instance


# Cargar modelos TFLite optimizados (sin archivos Keras)
print("Cargando modelos TFLite optimizados...")

analyzer = load_tflite_model(
    ChessStyleAnalyzer(),
    "models/style_detector/chess_model.tflite",
    "models/style_detector/chess_model_data.joblib"
)

recommender = load_tflite_model(
    OpeningRecommender(),
    "models/opening_recommender/opening_recommender_model.tflite",
    "models/opening_recommender/opening_recommender_model_metadata.joblib"
)

defense_recommender = load_tflite_model(
    DefenseRecommender(),
    "models/defense_recommender/defense_recommender_model.tflite",
    "models/defense_recommender/defense_recommender_model_metadata.joblib"
)

print("Todos los modelos TFLite cargados correctamente")