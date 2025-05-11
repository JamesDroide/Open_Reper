import chess
import chess.pgn
import numpy as np
from collections import Counter
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, BatchNormalization
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.utils import to_categorical
from keras.models import load_model
import matplotlib.pyplot as plt
from joblib import dump, load
import io
import chardet
import random

class ChessStyleAnalyzer:
    def __init__(self):

        # Mapeos de estilos
        self.style_mapping = {
            'Steinitz, Wilhelm': 'positional_classic',
            'Capablanca, José': 'positional_classic',
            'Karpov, Anatoly': 'positional_classic',
            'Kramnik, Vladimir': 'positional_classic',
            'Alekhine, Alexander': 'aggressive_dynamical',
            'Fischer, Robert James': 'aggressive_dynamical',
            'Kasparov, Garry': 'aggressive_dynamical',
            'Tal, Mikhail': 'aggressive_dynamical',
            'Petrosian, Tigran': 'defensive_prophylactic',
            'Lasker, Emanuel': 'defensive_prophylactic',
            'Spassky, Boris': 'universal_practical',
            'Anand, Viswanathan': 'universal_practical',
            'Carlsen, Magnus': 'universal_practical',
            'Botvinnik, Mikhail': 'scientific_technical',
            'Euwe, Max': 'scientific_technical'
        }

        # Calcular número de clases únicas
        self.unique_styles = list(set(self.style_mapping.values()))  # Obtener estilos únicos
        self.num_classes = len(self.unique_styles)  # Debería ser 5

        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.label_encoder.fit(self.unique_styles)
        self.model = self._build_neural_network()

        self.champion_mapping = {
            'positional_classic': [
                ('Karpov, Anatoly', 'Maestro del juego posicional'),
                ('Capablanca, José', 'Genio del juego simple y claro'),
                ('Kramnik, Vladimir', 'Especialista en transposiciones')
            ],
            'aggressive_dynamical': [
                ('Kasparov, Garry', 'Ataques dinámicos y preparación de aperturas'),
                ('Fischer, Robert James', 'Juego agudo y preciso'),
                ('Alekhine, Alexander', 'Ataques imaginativos'),
                ('Tal, Mikhail', 'Maestro de los sacrificios')
            ],
            'universal_practical': [
                ('Carlsen, Magnus', 'Adaptabilidad moderna'),
                ('Spassky, Boris', 'Estilo completo y versátil'),
                ('Anand, Viswanathan', 'Universalidad práctica')
            ],
            'scientific_technical': [
                ('Botvinnik, Mikhail', 'Padre del ajedrez científico'),
                ('Euwe, Max', 'Precisión técnica'),
                ('Petrosian, Tigran', 'Estrategia profiláctica')
            ],
            'defensive_prophylactic': [
                ('Petrosian, Tigran', 'Maestro de la defensa'),
                ('Lasker, Emanuel', 'Defensa práctica y psicológica')
            ]
        }

        self.opening_mapping = {
            'positional_classic': [
                ('E00', 'Apertura Catalana'),
                ('D37', 'Gambito de Dama Declinado'),
                ('A04', 'Apertura Reti'),
                ('D05', 'Sistema Colle')
            ],
            'aggressive_dynamical': [
                ('C30', 'Gambito de Rey'),
                ('A45', 'Apertura Trompowsky'),
                ('E60', 'India de Rey')
            ],
            'universal_practical': [
                ('A00', 'Apertura Inglesa'),
                ('D02', 'Sistema Londres'),
            ],
            'scientific_technical': [
                ('E12', 'India de Rey'),
                ('C65', 'Apertura Española'),
                ('D10', 'Gambito de Dama Aceptado')
            ],
            'defensive_prophylactic': [
                ('A46', 'Apertura de Torre'),
                ('D02', 'Sistema Londres')
            ]
        }

    def _build_neural_network(self):
        model = Sequential([
            Dense(256, activation='relu', input_shape=(420,)),
            # No usar ambos regularizadores al mismo tiempo
            # Probar primero una red neuronal sin regularizadores con 10 o 15 epocas
            # Probablemente mejor BatchNormalization
            BatchNormalization(),
            Dense(128, activation='relu'),
            BatchNormalization(),
            Dense(64, activation='relu'), # Capaz considerar Dropout(0.2)
            #Dropout(0.2),
            Dense(self.num_classes, activation='softmax')  # Usar self.num_classes
        ])

        model.compile(
            optimizer=Adam(learning_rate=0.001),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        return model

    def process_pgns(self):
        """Procesa archivos PGN subidos y extrae características"""
        uploaded = files.upload()
        features = []
        labels = []

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

                    # Obtener estilo del jugador
                    white = game.headers.get('White', '').strip()
                    black = game.headers.get('Black', '').strip()
                    style = self.style_mapping.get(white) or self.style_mapping.get(black)

                    if style:
                        game_features = self._extract_game_features(game)
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
        self.label_encoder.fit(list(set(self.style_mapping.values())))  # Forzar todas las clases

        # Preprocesamiento
        self.y = self.label_encoder.fit_transform(labels)
        self.X = self.scaler.fit_transform(features)

        # Podria aplicarse submuestreo y ya no seria necesario aplicar SMOTE

        # Balancear datos
        smote = SMOTE(k_neighbors=3)
        self.X, self.y = smote.fit_resample(self.X, self.y)

        print(f"\nDatos procesados: {len(self.X)} partidas")
        print("Distribución de estilos:", dict(zip(
            self.label_encoder.inverse_transform(np.unique(self.y)),
            np.bincount(self.y)
        )))
        return True

    def _extract_game_features(self, game):
      """Extrae características avanzadas de una partida de ajedrez"""
      MOVES_TO_ANALYZE = 30
      FEATURES_PER_MOVE = 14
      TOTAL_FEATURES = MOVES_TO_ANALYZE * FEATURES_PER_MOVE

      board = game.board()
      features = []
      previous_material = 0

      try:
          for move in list(game.mainline_moves())[:MOVES_TO_ANALYZE]:
              board.push(move)
              move_features = [
                  # Características estratégicas
                  self._calculate_material_balance(board),
                  self._king_safety_score(board),
                  self._pawn_structure_analysis(board),
                  self._piece_activity_score(board),
                  self._control_of_key_squares(board),
                  self._openness_position(board),
                  self._development_score(board),
                  self._sacrifice_detection(board, move, previous_material),
                  self._tactical_opportunities(board),
                  self._space_advantage(board),
                  self._piece_mobility(board),
                  self._attack_defense_ratio(board),
                  self._passed_pawns_count(board),
                  self._endgame_indicator(board)
              ]
              features.extend(move_features)
              previous_material = self._calculate_total_material(board)

          # Rellenar con ceros si la partida es más corta
          features += [0] * (TOTAL_FEATURES - len(features))
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
        return (white - black) / 10  # Normalizado

    def _king_safety_score(self, board):
        """Evaluación detallada de la seguridad del rey"""
        king_square = board.king(board.turn)
        if not king_square:
            return 0

        safety_score = 0
        # Escudo de peones
        pawn_shield = sum(1 for sq in board.attacks(king_square) if board.piece_type_at(sq) == chess.PAWN)

        # Ataques potenciales
        attackers = len(board.attackers(not board.turn, king_square))

        # Posición del rey (centro vs esquina)
        file = chess.square_file(king_square)
        rank = chess.square_rank(king_square)
        center_distance = abs(3.5 - file) + abs(3.5 - rank)

        return (pawn_shield * 0.5) - (attackers * 0.3) - (center_distance * 0.2)

    def _piece_mobility(self, board):
        """Movilidad de las piezas (número de movimientos legales disponibles)"""
        mobility = 0
        for piece_type in [chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN]:
            for sq in board.pieces(piece_type, board.turn):
                mobility += len(board.attacks(sq))
        return mobility / 50  # Normalizado según movilidad máxima típica

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
        return passed / 8  # Normalizado

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
        return activity / 20  # Normalizado

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

    def _endgame_indicator(self, board):
        """Indicador de fase de juego (0=apertura, 1=final)"""
        queens = len(board.pieces(chess.QUEEN, chess.WHITE)) + len(board.pieces(chess.QUEEN, chess.BLACK))
        minors = len(board.pieces(chess.BISHOP, chess.WHITE)) + len(board.pieces(chess.KNIGHT, chess.WHITE)) + \
                len(board.pieces(chess.BISHOP, chess.BLACK)) + len(board.pieces(chess.KNIGHT, chess.BLACK))

        if queens == 0 or (queens <= 1 and minors <= 2):
            return 1  # Final
        return 0  # Apertura/medio juego

    def train_model(self):
        # Preparar datos con one-hot encoding
        y_onehot = to_categorical(self.y, num_classes=self.num_classes)

        X_train, X_test, y_train, y_test = train_test_split(
            self.X,
            y_onehot,  # Usar el one-hot encoding correcto
            test_size=0.2,
            random_state=42
        )

        # Configurar early stopping
        early_stop = EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True
        )

        # Entrenamiento
        history = self.model.fit(
            X_train, y_train,
            epochs=30,
            batch_size=64,
            validation_data=(X_test, y_test),
            callbacks=[early_stop],
            verbose=1
        )

        # Evaluación final
        loss, accuracy = self.model.evaluate(X_test, y_test, verbose=0)
        print(f"\nPrecisión final en test: {accuracy*100:.2f}%")

        self._plot_training_history(history)

    def recommend_opening(self, pgn_text):
        """Realiza una recomendación de apertura"""
        try:
            game = chess.pgn.read_game(io.StringIO(pgn_text))
            features = self._extract_game_features(game)

            if features is None:
                return "Error", "No se pudo extraer características", "N/A"

            # Preprocesamiento y predicción
            features_scaled = self.scaler.transform([features])
            pred = self.model.predict(features_scaled, verbose=0)
            style_code = np.argmax(pred)
            style = self.label_encoder.inverse_transform([style_code])[0]

            # Obtener recomendaciones
            champion, desc = random.choice(self.champion_mapping[style])
            eco, name = random.choice(self.opening_mapping[style])
            return champion, desc, (eco, name)

        except Exception as e:
            return "Error", str(e), "N/A"

    def save_model(self, filename):
        """Guarda el modelo en formato .h5 y .keras"""
        model_data = {
            'scaler': self.scaler,
            'label_encoder': self.label_encoder,
            'style_mapping': self.style_mapping,
            'opening_mapping': self.opening_mapping,
            'champion_mapping': self.champion_mapping
        }
        # Guardar en ambos formatos
        self.model.save(filename + '.h5')  # Formato HDF5
        self.model.save(filename + '.keras')  # Formato Keras
        dump(model_data, filename + '_data.joblib')
        print(f"Modelo guardado en {filename}.h5, {filename}.keras y {filename}_data.joblib")

    @classmethod
    def load_model(cls, filename):
        """Carga el modelo desde cualquier formato"""
        analyzer = cls()
        model_data = load(filename + '_data.joblib')

        analyzer.scaler = model_data['scaler']
        analyzer.label_encoder = model_data['label_encoder']
        analyzer.style_mapping = model_data['style_mapping']
        analyzer.opening_mapping = model_data['opening_mapping']
        analyzer.champion_mapping = model_data['champion_mapping']

        try:
            analyzer.model = load_model(filename + '.h5')
        except:
            analyzer.model = load_model(filename + '.keras')

        print(f"Modelo cargado desde {filename}")
        return analyzer

    def _plot_training_history(self, history):
        """Genera gráficos de precisión y pérdida"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7))

        # Gráfico de precisión
        ax1.plot(history.history['accuracy'], label='Entrenamiento', linewidth=2)
        ax1.plot(history.history['val_accuracy'], label='Validación', linewidth=2)
        ax1.set_title('Evolución de la Precisión', pad=20, fontsize=16)
        ax1.set_ylabel('Precisión', fontsize=12)
        ax1.set_xlabel('Época', fontsize=12)
        ax1.legend(loc='lower right', frameon=True, fontsize=10)

        # Gráfico de pérdida
        ax2.plot(history.history['loss'], label='Entrenamiento', linewidth=2)
        ax2.plot(history.history['val_loss'], label='Validación', linewidth=2)
        ax2.set_title('Evolución de la Pérdida', pad=20, fontsize=16)
        ax2.set_ylabel('Pérdida', fontsize=12)
        ax2.set_xlabel('Época', fontsize=12)
        ax2.legend(loc='upper right', frameon=True, fontsize=10)

        plt.tight_layout()
        plt.show()
