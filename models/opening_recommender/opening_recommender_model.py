import chess.pgn
import io
from sklearn.preprocessing import StandardScaler, LabelEncoder
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
import joblib

class OpeningRecommender:
    def __init__(self):

        self.opening_mapping = {
            'Catalana': {'style': 'posicional'},
            'Inglesa': {'style': 'posicional'},
            'Londres': {'style': 'posicional'},
            'Escocesa': {'style': 'combinativo'},
            'Gambito_de_Rey': {'style': 'combinativo'},
            'Gambito_Danes': {'style': 'combinativo'},
            'Italiana': {'style': 'universal'},
            'Española': {'style': 'universal'},
            'Gambito_de_Dama': {'style': 'universal'}
        }

        self.style_spanish_mapping = {
            'positional': 'posicional',
            'combinative': 'combinativo',
            'universal': 'universal'
        }

        self.scaler = StandardScaler()
        self.opening_encoder = LabelEncoder()
        self.style_encoder = LabelEncoder()

        opening_names = list(self.opening_mapping.keys())
        self.opening_encoder.fit(opening_names)

        styles = list({v['style'] for v in self.opening_mapping.values()})
        self.style_encoder.fit(styles)

        self.model = None

    def _build_recommendation_model(self, input_shape, num_openings):
        """Construye la red neuronal para recomendación de aperturas"""
        model = Sequential([
            Dense(256, activation='relu', input_shape=(input_shape,)),
            Dropout(0.4),
            Dense(128, activation='relu'),
            Dropout(0.3),
            Dense(64, activation='relu'),
            Dense(num_openings, activation='softmax')
        ])

        model.compile(
            optimizer=Adam(learning_rate=0.0008),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        return model

    def _extract_game_features(self, game, style):
        """Extrae características técnicas + estilo como input"""
        MOVES_TO_ANALYZE = 30
        FEATURES_PER_MOVE = 8
        STYLE_FEATURES = 3
        TOTAL_FEATURES = MOVES_TO_ANALYZE * FEATURES_PER_MOVE + STYLE_FEATURES

        board = game.board()
        features = []
        moves_analyzed = 0

        try:
            # One-hot encoding del estilo
            style_encoded = self.style_encoder.transform([style])[0]
            style_onehot = [0] * STYLE_FEATURES
            style_onehot[style_encoded] = 1

            for move in game.mainline_moves():
                board.push(move)
                if moves_analyzed >= MOVES_TO_ANALYZE:
                    break

                # 1. Control del centro
                center_control = sum(1 for sq in [chess.D4, chess.D5, chess.E4, chess.E5]
                                    if board.is_attacked_by(chess.WHITE, sq))

                # 2. Desarrollo de piezas
                knights = [sq for sq in board.pieces(chess.KNIGHT, chess.WHITE)
                          if sq not in [chess.B1, chess.G1]]
                bishops = [sq for sq in board.pieces(chess.BISHOP, chess.WHITE)
                          if sq not in [chess.C1, chess.F1]]
                piece_development = len(knights + bishops)

                # 3. Enroque
                castling = 1 if board.has_castling_rights(chess.WHITE) else 0

                # 4. Avance de peones
                pawn_advance = sum(chess.square_rank(sq) for sq in board.pieces(chess.PAWN, chess.WHITE))

                # 5. Actividad de la dama
                queen_squares = board.pieces(chess.QUEEN, chess.WHITE)
                queen_active = 1 if queen_squares and next(iter(queen_squares)) not in [chess.D1, chess.E1] else 0

                # 6. Balance material
                material_balance = (
                    len(board.pieces(chess.PAWN, chess.WHITE)) * 1 +
                    len(board.pieces(chess.KNIGHT, chess.WHITE)) * 3 +
                    len(board.pieces(chess.BISHOP, chess.WHITE)) * 3 +
                    len(board.pieces(chess.ROOK, chess.WHITE)) * 5 +
                    len(board.pieces(chess.QUEEN, chess.WHITE)) * 9
                )

                # 7. Columnas abiertas
                open_files = 0
                for file_index in range(8):
                    file_mask = chess.BB_FILES[file_index]
                    white_pawns = board.pieces(chess.PAWN, chess.WHITE) & file_mask
                    black_pawns = board.pieces(chess.PAWN, chess.BLACK) & file_mask
                    if not white_pawns and not black_pawns:
                        open_files += 1

                # 8. Complejidad posicional
                position_complexity = len(list(board.legal_moves))

                features.extend([
                    center_control,
                    piece_development,
                    castling,
                    pawn_advance,
                    queen_active,
                    material_balance,
                    open_files,
                    position_complexity
                ])
                moves_analyzed += 1

            # Asegurar longitud fija
            current_length = len(features)
            if current_length < TOTAL_FEATURES - STYLE_FEATURES:
                features += [0] * (TOTAL_FEATURES - STYLE_FEATURES - current_length)
            features = features[:TOTAL_FEATURES - STYLE_FEATURES]

            # Agregar características de estilo
            features += style_onehot
            return features
        except Exception as e:
            print(f"Error en extracción: {str(e)}")
            return None

    def recommend_for_pgn(self, pgn_text, player_style=None):
        """Recomienda aperturas basadas en un PGN de partida y estilo de jugador"""

        try:
            if player_style and player_style not in self.style_spanish_mapping.values():
                return f"Estilo '{player_style}' no válido. Opciones: {list(self.style_spanish_mapping.values())}"

            # Procesar PGN
            pgn = io.StringIO(pgn_text)
            game = chess.pgn.read_game(pgn)
            if not game:
                return "Error: No se pudo leer el PGN"

            features = self._extract_game_features(game, player_style)
            if not features:
                return "Error: No se pudieron extraer características"

            scaled_features = self.scaler.transform([features])

            # Predecir probabilidades
            prediction = self.model.predict(scaled_features, verbose=0)[0]

            opening_names = list(self.opening_mapping.keys())
            recommendations = []
            for idx, prob in enumerate(prediction):
                opening = opening_names[idx]
                if opening not in self.opening_mapping:
                    continue
                recommendations.append({
                    'apertura': opening,
                    'estilo': self.opening_mapping[opening]['style'],
                    'probabilidad': float(prob),
                    'ponderacion' : 0.00
                })

            recommendations.sort(key=lambda x: (-x['probabilidad'], x['apertura']))
            return recommendations[:3]

        except Exception as e:
            return f"Error: {str(e)}"

    @classmethod
    def load_model(cls, filename="opening_recommender"):
        """Carga el modelo y metadatos"""
        recommender = cls()

        # Cargar metadatos
        model_data = joblib.load(f"{filename}_metadata.joblib")
        recommender.scaler = model_data['scaler']
        recommender.opening_encoder = model_data['opening_encoder']
        recommender.style_encoder = model_data['style_encoder']
        recommender.opening_mapping = model_data['opening_mapping']
        recommender.style_spanish_mapping = model_data['style_spanish_mapping']

        # Cargar modelo
        recommender.model = load_model(f"{filename}.keras")
        print(f"Modelo cargado desde {filename}.keras")
        return recommender