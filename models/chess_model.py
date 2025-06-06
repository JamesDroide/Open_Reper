import chess
import chess.pgn
import io
import chardet
import numpy as np
import joblib
import seaborn as sns
from collections import Counter
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import confusion_matrix
from imblearn.over_sampling import ADASYN
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.regularizers import l2
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import random

class ChessStyleAnalyzer:
    def __init__(self):

        # Mapeos de estilos
        self.style_mapping = {
            'Steinitz, Wilhelm': 'positional',
            'Capablanca, José': 'positional',
            'Karpov, Anatoly': 'positional',
            'Kramnik, Vladimir': 'positional',
            'Alekhine, Alexander': 'combinative',
            'Fischer, Robert James': 'combinative',
            'Kasparov, Garry': 'combinative',
            'Tal, Mikhail': 'combinative',
            'Petrosian, Tigran': 'positional',
            'Lasker, Emanuel': 'universal',
            'Spassky, Boris': 'universal',
            'Anand, Viswanathan': 'universal',
            'Carlsen, Magnus': 'universal',
            'Botvinnik, Mikhail': 'positional',
            'Euwe, Max': 'positional'
        }

        # Calcular número de clases únicas
        self.unique_styles = list(set(self.style_mapping.values()))
        self.num_classes = len(self.unique_styles)

        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.label_encoder.fit(self.unique_styles)
        self.model = self._build_neural_network()

        self.opening_mapping = {
            'positional': [
                ('E00', 'Apertura Catalana'),
                ('A10', 'Apertura Inglesa'),
                ('D02', 'Sistema Londres')
            ],
            'combinative': [
                ('C39', 'Gambito de Rey'),
                ('C44', 'Apertura Escocesa'),
                ('C21', 'Gambito Danés')
            ],
            'universal': [
                ('C50', 'Apertura Italiana'),
                ('C60', 'Apertura Española'),
                ('D00', 'Gambito de Dama')
            ]
        }

        self.style_spanish_mapping = {
            'positional' : 'Posicional',
            'combinative' : 'Combinativo',
            'universal' : 'Universal'
        }

    def _build_neural_network(self):
        """
            - Quitar Dropouts y solo en la ultima capa
            - Aumentar el numero de neuronas a 1600-2000 aprox
            - Estandarizar los valores
            - El segundo y tercer regularizar es probable que este al reves
            - Bajar todos los regularizadores al mismo hiperparametro
        """
        model = Sequential([
            Dense(360, activation='relu', input_shape=(360,), kernel_regularizer=l2(0.001)),
            Dropout(0.2),
            Dense(1024, activation='relu', kernel_regularizer=l2(0.001)),
            Dropout(0.2),
            Dense(512, activation='relu', kernel_regularizer=l2(0.001)),
            Dropout(0.2),
            Dense(256, activation='relu', kernel_regularizer=l2(0.001)),
            Dropout(0.2),
            Dense(64, activation='relu'),
            Dense(self.num_classes, activation='softmax')
        ])

        """
        Matriz de confusion predicted vs expected

        Considerar usar Redes Neuronales Recurrentes

        Posible problema de desbalance de clases
        """

        model.compile(
            optimizer=Adam(learning_rate=0.0001), # Posiblemente memorizacion
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        return model

    def process_pgns(self):
        """Procesa archivos PGN subidos y extrae características"""
        uploaded = files.upload()
        features = []
        labels = []

        """Añadir filtro para que solo acepte partidas de minimo 30 movimientos"""
        for filename, content in uploaded.items():
            try:
                # Detección de codificación
                enc = chardet.detect(content)['encoding'] or 'latin-1'
                pgn_text = content.decode(enc, errors='replace')
                pgn = io.StringIO(pgn_text)

                while True:
                    game = chess.pgn.read_game(pgn)
                    if not game:
                        break

                    move_count = sum(1 for _ in game.mainline_moves())
                    if move_count < 60:
                        continue

                    # Obtener estilo del jugador
                    white = game.headers.get('White', '').strip()
                    black = game.headers.get('Black', '').strip()
                    style = self.style_mapping.get(white)
                    color = chess.WHITE

                    if not style:
                        style = self.style_mapping.get(black)
                        color = chess.BLACK

                    if style:
                        game_features = self._extract_game_features(game, color)
                        if game_features:
                            features.append(game_features)
                            labels.append(style)

            except Exception as e:
                print(f"Error procesando {filename}: {str(e)}")
                continue

        if not features:
            print("No hay datos válidos para entrenar")
            return False

        # Asegurar que el LabelEncoder se ajuste correctamente
        self.label_encoder.fit(list(set(self.style_mapping.values())))

        # Preprocesamiento
        self.y = self.label_encoder.fit_transform(labels)
        self.X = self.scaler.fit_transform(features)

        # Balancear datos
        adasyn = ADASYN(n_neighbors=2)
        self.X, self.y = adasyn.fit_resample(self.X, self.y)

        print(f"\nDatos procesados: {len(self.X)} partidas")
        print("Distribución de estilos:", dict(zip(
            self.label_encoder.inverse_transform(np.unique(self.y)),
            np.bincount(self.y)
        )))
        return True

    def _extract_game_features(self, game, color):
      """Extrae características avanzadas de una partida de ajedrez"""
      MOVES_TO_ANALYZE = 30
      FEATURES_PER_MOVE = 12
      TOTAL_FEATURES = MOVES_TO_ANALYZE * FEATURES_PER_MOVE

      board = game.board()
      features = []
      previous_material = 0
      moves_analyzed = 0

      try:
          for i, move in enumerate(game.mainline_moves()):
              board.push(move)
              if board.turn != color:
                  continue

              if moves_analyzed < MOVES_TO_ANALYZE:
                  move_features = [
                      # Características estratégicas
                      self._calculate_material_balance(board),
                      self._king_safety_score(board),
                      self._pawn_structure_analysis(board),
                      self._piece_activity_score(board),
                      self._control_of_key_squares(board),
                      self._openness_position(board),
                      #self._development_score(board),
                      self._sacrifice_detection(board, move, previous_material),
                      self._tactical_opportunities(board),
                      self._space_advantage(board),
                      self._piece_mobility(board),
                      #self._attack_defense_ratio(board),
                      self._passed_pawns_count(board),
                      self._bishop_pair_advantage(board)
                  ]
                  features.extend(move_features)
                  previous_material = self._calculate_total_material(board)
                  moves_analyzed += 1

              if len(features) >= TOTAL_FEATURES:
                  break

          return features[:TOTAL_FEATURES]

      except Exception as e:
          print(f"Error en extracción: {str(e)}")
          return None

    def _calculate_material_balance(self, board):
        """Balance material con valores de pieza ajustados"""
        piece_values = {
            chess.PAWN: 1.5,    # Valor ligeramente mayor por estructura
            chess.KNIGHT: 3.2,
            chess.BISHOP: 3.5,  # Par de alfiles bonus se maneja aparte
            chess.ROOK: 5.1,
            chess.QUEEN: 9.8,
            chess.KING: 0
        }
        white = sum(len(board.pieces(pt, chess.WHITE)) * val for pt, val in piece_values.items())
        black = sum(len(board.pieces(pt, chess.BLACK)) * val for pt, val in piece_values.items())
        return (white - black) / 10  # Sin la division por 10, la maxima diferencia es de +-45.4

    def _king_safety_score(self, board):
        """Evaluación detallada de la seguridad del rey"""
        king_square = board.king(board.turn)
        if not king_square:
            return 0

        # Escudo de peones
        pawn_shield = sum(1 for sq in board.attacks(king_square)
              if board.piece_type_at(sq) == chess.PAWN
              and board.color_at(sq) == board.turn)

        # Ataques potenciales
        attackers = len(board.attackers(not board.turn, king_square))

        # Posición del rey (centro vs esquina)
        file = chess.square_file(king_square)
        rank = chess.square_rank(king_square)
        center_distance = abs(3.5 - file) + abs(3.5 - rank)

        return (pawn_shield * 0.5) - (attackers * 0.3) - (center_distance * 0.2) # Entre -2 y +3

    def _piece_mobility(self, board):
        """Movilidad de las piezas (número de movimientos legales disponibles)"""
        mobility = 0
        for piece_type in [chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN]:
            for sq in board.pieces(piece_type, board.turn):
                mobility += len(board.attacks(sq))
        return mobility / 50

    def _attack_defense_ratio(self, board):
        """Relación entre ataques y defensas en el tablero"""
        attack_count = 0
        defense_count = 0
        for square in chess.SQUARES:
            if board.piece_at(square):
                attack_count += len(board.attackers(board.turn, square))
                defense_count += len(board.attackers(not board.turn, square))
        if defense_count == 0:
            return 1.0 if attack_count > 0 else 0.0
        return (attack_count - defense_count) / (attack_count + defense_count)

    def _is_passed_pawn(self, board, pawn_square):
        """Verifica si un peón es pasado"""
        color = board.color_at(pawn_square)
        if color is None:
            return False

        pawn_file = chess.square_file(pawn_square)
        pawn_rank = chess.square_rank(pawn_square)

        # Determinar dirección según color
        direction = 1 if color == chess.WHITE else -1
        start_rank = pawn_rank + direction

        # Verificar casillas hacia adelante en columnas adyacentes
        for rank in range(start_rank, 8) if color == chess.WHITE else range(start_rank, -1, -1):
            for file_offset in (-1, 0, 1):
                current_file = pawn_file + file_offset
                if 0 <= current_file <= 7:
                    square = chess.square(current_file, rank)
                    # Verificar peones enemigos
                    if board.piece_type_at(square) == chess.PAWN and board.color_at(square) != color:
                        return False
        return True

    def _passed_pawns_count(self, board):
        """Conteo de peones pasados"""
        passed = 0
        pawns = board.pieces(chess.PAWN, board.turn)
        enemy_pawns = board.pieces(chess.PAWN, not board.turn)
        for pawn in pawns:
            is_passed = True
            pawn_file = chess.square_file(pawn)
            pawn_rank = chess.square_rank(pawn)
            # Verificar columnas adyacentes y frente del peón
            for file in [pawn_file-1, pawn_file, pawn_file+1]:
                if 0 <= file <= 7:
                    for rank in range(pawn_rank+1, 8):
                        if chess.square(file, rank) in enemy_pawns:
                            is_passed = False
                            break
                    if not is_passed:
                        break
            if is_passed:
                passed += 1
        return passed / 8

    def _development_score(self, board):
        """Puntaje de desarrollo de piezas menores"""
        developed = 0
        # Para blancas: piezas en filas 0-1 son no desarrolladas
        # Para negras: piezas en filas 6-7 son no desarrolladas
        back_rank = 0 if board.turn == chess.WHITE else 7
        second_rank = 1 if board.turn == chess.WHITE else 6

        for piece_type in [chess.KNIGHT, chess.BISHOP]:
            for sq in board.pieces(piece_type, board.turn):
                if chess.square_rank(sq) not in [back_rank, second_rank]:
                    developed += 1
        # Máximo 4 piezas (2 caballos y 2 alfiles)
        return developed / 4

    def _pawn_structure_analysis(self, board):
        """Análisis completo de estructura de peones"""
        pawns = board.pieces(chess.PAWN, board.turn)
        score = 0

        # Peones doblados
        files = [chess.square_file(p) for p in pawns]
        score -= sum(v-1 for v in Counter(files).values())

        # Peones pasados
        score += sum(1 for p in pawns if self._is_passed_pawn(board, p))

        # Peones aislados
        adjacent_files = set()
        for f in files:
            adjacent_files.update([f-1, f+1])
        score -= sum(1 for f in files if f not in adjacent_files)

        return score

    def _piece_activity_score(self, board):
        """Movilidad y actividad de piezas mayores"""
        activity = 0
        for piece_type in [chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN]:
            for sq in board.pieces(piece_type, board.turn):
                activity += len(board.attacks(sq))
        return activity / 20

    def _control_of_key_squares(self, board):
        """Control de centros estratégicos y casillas clave"""
        key_squares = [
            chess.D4, chess.D5, chess.E4, chess.E5,  # Centro clásico
            chess.C3, chess.C6, chess.F3, chess.F6,  # Centro extendido
            chess.D3, chess.E3, chess.D6, chess.E6  # Acceso al centro
        ]
        return sum(1 for sq in key_squares if board.is_attacked_by(board.turn, sq))

    def _openness_position(self, board):
        """Evalúa si la posición es abierta o cerrada"""
        open_files = 0
        for file in range(8):
            # Verificar si hay peones en el archivo para ambos colores
            has_pawns = False
            for color in [chess.WHITE, chess.BLACK]:
                for sq in board.pieces(chess.PAWN, color):
                    if chess.square_file(sq) == file:
                        has_pawns = True
                        break
                if has_pawns:
                    break
            if not has_pawns:
                open_files += 1
        return open_files

    def _calculate_total_material(self, board):
        """Calcula el material total del jugador actual"""
        piece_values = {
            chess.PAWN: 1.5,
            chess.KNIGHT: 3.2,
            chess.BISHOP: 3.5,
            chess.ROOK: 5.1,
            chess.QUEEN: 9.8,
            chess.KING: 0
        }
        total = 0
        for piece_type, value in piece_values.items():
            total += len(board.pieces(piece_type, board.turn)) * value
        return total

    def _sacrifice_detection(self, board, move, previous_material):
        """Detección de sacrificios posicionales y materiales"""
        current_material = self._calculate_total_material(board)
        material_diff = previous_material - current_material

        # Sacrificio si pérdida material > 2 puntos y control del centro aumenta
        if material_diff > 2 and self._control_of_key_squares(board) > 4:
            return 1
        return 0

    def _tactical_opportunities(self, board):
        """Oportunidades tácticas potenciales"""
        hanging_pieces = 0
        for color in [chess.WHITE, chess.BLACK]:
            for sq in board.pieces(chess.PAWN, color):
                if not board.attackers(color, sq):
                    hanging_pieces += 1
        return -hanging_pieces if board.turn == chess.WHITE else hanging_pieces

    def _space_advantage(self, board):
        """Ventaja espacial en el tablero"""
        squares_controlled = 0
        for sq in chess.SQUARES:
            if board.is_attacked_by(board.turn, sq):
                squares_controlled += 1
        return squares_controlled / 64

    def _bishop_pair_advantage(self, board):
        """Ventaja de pareja de alfiles"""
        white_bishops = len(board.pieces(chess.BISHOP, chess.WHITE))
        black_bishops = len(board.pieces(chess.BISHOP, chess.BLACK))

        white_pair = 1 if white_bishops >= 2 else 0
        black_pair = 1 if black_bishops >= 2 else 0
        return white_pair - black_pair

    def train_model(self):
        # Preparar datos con one-hot encoding
        y_onehot = to_categorical(self.y, num_classes=self.num_classes)

        X_train, X_test, y_train, y_test = train_test_split(
            self.X,
            y_onehot,
            test_size=0.2,
            random_state=42
        )

        # Configurar early stopping
        early_stop = EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True,
            min_delta=0.0001
        )

        print("\n== Resumen del Modelo ==")
        self.model.summary()

        # Entrenamiento
        history = self.model.fit(
            X_train, y_train,
            epochs=150,
            batch_size=128,
            validation_data=(X_test, y_test),
            callbacks=[early_stop],
            verbose=1
        )

        # Evaluación final
        loss, accuracy = self.model.evaluate(X_test, y_test, verbose=0)

        y_pred = np.argmax(self.model.predict(X_test), axis=1)
        y_true = np.argmax(y_test, axis=1)
        conf_matrix = confusion_matrix(y_true, y_pred)

        print(f"\nPrecisión final en test: {accuracy*100:.2f}%")

        self._plot_training_history(history, conf_matrix)

    def recommend_opening(self, pgn_text):
        """Realiza una recomendación de apertura con validaciones mejoradas"""
        try:
            # --- Validación 1: Input vacío o texto no válido ---
            if not pgn_text or not isinstance(pgn_text, str) or pgn_text.isspace():
                return {
                    "status": "error",
                    "message": "No se ha enviado un PGN válido"
                }

            # --- Validación 2: Verificar formato PGN válido ---
            try:
                game = chess.pgn.read_game(io.StringIO(pgn_text))
                if not game or not game.mainline_moves():
                    raise ValueError("Formato PGN inválido")
            except:
                return {
                    "status": "error",
                    "message": "No se ha enviado un PGN válido"
                }

            # --- Validación 3: Mínimo de movimientos ---
            move_count = sum(1 for _ in game.mainline_moves())
            if move_count < 60:
                return {
                    "status": "error",
                    "message": "El PGN enviado debe contener un mínimo de 30 movimientos"
                }

            # --- Procesamiento normal si pasa validaciones ---
            features = self._extract_game_features(game, chess.WHITE)
            if features is None:
                return {
                    "status": "error",
                    "message": "No se pudo extraer características del PGN"
                }

            features_scaled = self.scaler.transform([features])
            pred = self.model.predict(features_scaled, verbose=0)
            style_code = np.argmax(pred)
            style = self.label_encoder.inverse_transform([style_code])[0]

            # Obtener recomendaciones
            eco, name = random.choice(self.opening_mapping[style])
            return {
                "status": "success",
                "style": self.style_spanish_mapping[style],
                "opening": {
                    "eco": eco,
                    "name": name
                }
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Error inesperado: {str(e)}"
            }

    def save_model(self, filename):
        """Guarda el modelo y metadatos de forma robusta"""
        model_data = {
            'scaler': self.scaler,
            'label_encoder': self.label_encoder,
            'style_mapping': self.style_mapping,
            'opening_mapping': self.opening_mapping,
            'style_spanish_mapping': self.style_spanish_mapping
        }

        # Guardar modelo en múltiples formatos
        self.model.save(f"{filename}.keras")
        self.model.save(f"{filename}.h5")

        # Guardar metadatos
        with open(f"{filename}_data.joblib", 'wb') as f:
            joblib.dump(model_data, f)

        print(f"Modelo guardado exitosamente: {filename}.keras + metadatos")

    @classmethod
    def load_model(cls, filename):
        """Carga el modelo y metadatos con verificación de integridad"""
        analyzer = cls()

        # Cargar metadatos
        with open(f"{filename}_data.joblib", 'rb') as f:
            model_data = joblib.load(f)

        # Asignar metadatos
        analyzer.scaler = model_data['scaler']
        analyzer.label_encoder = model_data['label_encoder']
        analyzer.style_mapping = model_data['style_mapping']
        analyzer.opening_mapping = model_data['opening_mapping']
        analyzer.style_spanish_mapping = model_data.get('style_spanish_mapping', {})

        try:
            analyzer.model = load_model(f"{filename}.keras")
        except:
            analyzer.model = load_model(f"{filename}.h5")

        print(f"Modelo cargado exitosamente desde {filename}")
        return analyzer

    def _plot_training_history(self, history, conf_matrix):
        """Genera gráficos de precisión, pérdida y matriz de confusión"""
        style_names = self.label_encoder.classes_

        fig = plt.figure(figsize=(20, 7))

        # Gráfico de precisión
        ax1 = plt.subplot(1, 3, 1)
        ax1.plot(history.history['accuracy'], label='Entrenamiento', linewidth=2)
        ax1.plot(history.history['val_accuracy'], label='Validación', linewidth=2)
        ax1.set_title('Evolución de la Precisión', pad=20, fontsize=16)
        ax1.set_ylabel('Precisión', fontsize=12)
        ax1.set_xlabel('Época', fontsize=12)
        ax1.legend(loc='lower right', frameon=True, fontsize=10)

        # Gráfico de pérdida
        ax2 = plt.subplot(1, 3, 2)
        ax2.plot(history.history['loss'], label='Entrenamiento', linewidth=2)
        ax2.plot(history.history['val_loss'], label='Validación', linewidth=2)
        ax2.set_title('Evolución de la Pérdida', pad=20, fontsize=16)
        ax2.set_ylabel('Pérdida', fontsize=12)
        ax2.set_xlabel('Época', fontsize=12)
        ax2.legend(loc='upper right', frameon=True, fontsize=10)

        # Matriz de confusión
        ax3 = plt.subplot(1, 3, 3)
        sns.heatmap(conf_matrix, annot=True, fmt='d', ax=ax3, cmap='Blues',
                    xticklabels=style_names, yticklabels=style_names)
        ax3.set_title('Matriz de Confusión', pad=20, fontsize=16)
        ax3.set_xlabel('Predicho', fontsize=12)
        ax3.set_ylabel('Verdadero', fontsize=12)

        plt.tight_layout()
        plt.show()