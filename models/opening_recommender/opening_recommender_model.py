import chess.pgn
import io
from sklearn.preprocessing import StandardScaler, LabelEncoder
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
import joblib
from collections import  Counter

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
        
    def _extract_game_features(self, game, style, color=chess.WHITE):
        """Extrae características avanzadas de una partida de ajedrez con estilo"""
        MOVES_TO_ANALYZE = 30
        FEATURES_PER_MOVE = 13
        STYLE_FEATURES = len(self.style_encoder.classes_)
        TOTAL_FEATURES = MOVES_TO_ANALYZE * FEATURES_PER_MOVE + STYLE_FEATURES

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
                        self._calculate_material_balance(board),
                        self._king_safety_score(board),
                        self._pawn_structure_analysis(board),
                        self._piece_activity_score(board),
                        self._control_of_key_squares(board),
                        self._openness_position(board),
                        self._sacrifice_detection(board, move, previous_material),
                        self._tactical_opportunities(board),
                        self._space_advantage(board),
                        self._piece_mobility(board),
                        self._passed_pawns_count(board),
                        self._bishop_pair_advantage(board),
                        self._pieces_in_enemy_territory(board)
                    ]
                    features.extend(move_features)
                    previous_material = self._calculate_total_material(board)
                    moves_analyzed += 1

                if len(features) >= MOVES_TO_ANALYZE * FEATURES_PER_MOVE:
                    break

            style_encoded = self.style_encoder.transform([style])[0]
            style_onehot = [0] * STYLE_FEATURES
            style_onehot[style_encoded] = 1
            features += style_onehot

            current_length = len(features)
            if current_length < TOTAL_FEATURES:
                features += [0] * (TOTAL_FEATURES - current_length)
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

    def _pieces_in_enemy_territory(self, board):
        """Calcula cuántas piezas están en campo enemigo"""
        enemy_territory = range(24, 64) if board.turn == chess.WHITE else range(0, 40)
        count = 0
        for square in chess.SQUARES:
            if square in enemy_territory and board.piece_at(square) and board.color_at(square) == board.turn:
                # Dar mayor peso a piezas de ataque
                piece_type = board.piece_type_at(square)
                if piece_type in [chess.QUEEN, chess.ROOK, chess.BISHOP]:
                    count += 1.5
                else:
                    count += 1
        return count / 10

    def recommend_for_pgn(self, pgn_text, color, player_style=None):
        """Recomienda aperturas basadas en un PGN de partida y estilo de jugador"""

        try:
            if player_style and player_style not in self.style_spanish_mapping.values():
                return f"Estilo '{player_style}' no válido. Opciones: {list(self.style_spanish_mapping.values())}"

            # Procesar PGN
            if not pgn_text or not isinstance(pgn_text, str) or pgn_text.isspace():
                return {
                    "status": "error",
                    "message": "No se ha enviado un PGN válido"
                }
                
            try:
                game = chess.pgn.read_game(io.StringIO(pgn_text))
                if not game or not game.mainline_moves():
                    raise ValueError("Formato PGN inválido")
            except:
                return {
                    "status": "error",
                    "message": "No se ha enviado un PGN válido"
                }
                
            move_count = sum(1 for _ in game.mainline_moves())
            if move_count < 60:
                return {
                    "status": "error",
                    "message": "El PGN enviado debe contener un mínimo de 30 movimientos"
                }

            chess_color = chess.WHITE if color.lower() == 'white' else chess.BLACK

            features = self._extract_game_features(game, player_style, chess_color)
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
                    'probabilidad': round(float(prob), 2)
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