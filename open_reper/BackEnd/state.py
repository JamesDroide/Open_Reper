#backend/state.py
import urllib
import chess
import reflex as rx
import asyncio
import io

from typing import List, Tuple, Dict
from .types import RecommendedOpening

from open_reper.BackEnd.model.model_loader import analyzer, recommender
from open_reper.BackEnd.constants import style_descriptions, openings, opening_mapping
from open_reper.BackEnd.openings_utils import _get_opening_description, _get_plans, _get_opening_moves, _get_model_games

class State(rx.State):
    pgn_text: str = ""
    recommendation: dict = {} # type: ignore
    recommended_opening: RecommendedOpening = {
        "eco": "",
        "name": "",
        "style": "",
        "description": "",
        "plans": []
    }
    is_loading: bool = False
    error: str = ""
    current_move: int = 0
    board_svg: str = ""
    game_moves: List[str] = []
    rating: int = 0
    variant_selected: str = ""
    description: str = ""
    plans: List[str] = []

    white_player: str = "Blancas"
    black_player: str = "Negras"
    game_metadata: dict = {} # type: ignore
    selected_color: str = "white"

    # Variables para el tablero interactivo
    fen: str = chess.Board().fen()
    position: Dict[str, str] = {}
    selected_square: str = ""
    move_from: str = ""
    move_to: str = ""
    legal_moves: List[str] = []
    turn: str = "white"
    move_history: List[str] = []
    interactive_current_move: int = 0

    def on_load(self):
        """Carga el estado al iniciar la página"""
        self.reset_board()

    @rx.event
    async def get_recommendation(self):
        self.is_loading = True
        self.error = ""
        color = self.selected_color
        try:
            # Análisis de estilo
            result = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: analyzer.detect_style(self.pgn_text, color)
            )

            if result['status'] != 'success':
                self.error = result['message']
                return

            style = result['style']
            self.recommendation = {
                "style": style,
                "description": style_descriptions.get(style, ""),
            }

            # Obtención de recomendación de apertura
            result_opening = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: recommender.recommend_for_pgn(self.pgn_text, color, style.lower())
            )

            # Validación de respuesta del recomendador
            if not isinstance(result_opening, list) or len(result_opening) == 0:
                self.error = "No se encontraron recomendaciones válidas"
                return

            # Extracción de datos de la apertura
            recommended_opening = result_opening[0]['apertura']
            eco_code = openings.get(recommended_opening)

            if not eco_code:
                self.error = f"No se encontró código ECO para {recommended_opening}"
                return

            # Actualización de estado
            self.recommendation['opening'] = f"Apertura {recommended_opening.replace('_', ' ')}"
            self.set_recommended_opening(recommended_opening, style)
            self.game_moves = _get_model_games(eco_code)
            self.current_move = 0

            if self.game_moves:
                self.board_svg = self._render_board(self.game_moves[:self.current_move + 1])

        except Exception as e:
            self.error = f"Error procesando PGN: {str(e)}"
        finally:
            self.is_loading = False

    def update_position(self):
        """Actualiza la posición de las piezas desde el FEN."""
        board = chess.Board(self.fen)
        self.position = {}
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                square_name = chess.square_name(square)
                self.position[square_name] = piece.symbol()
        self.turn = "white" if board.turn == chess.WHITE else "black"

    def select_square(self, square: str):
        if not self.move_from:
            self.move_from = square
            self.selected_square = square
            board = chess.Board(self.fen)
            self.legal_moves = [
                chess.square_name(move.to_square)
                for move in board.legal_moves
                if chess.square_name(move.from_square) == square
            ]
        else:
            self.move_to = square
            self.make_move()

    def make_move(self):
        if self.move_from and self.move_to:
            move_str = f"{self.move_from}{self.move_to}"
            try:
                board = chess.Board(self.fen)
                move = chess.Move.from_uci(move_str)
                if move in board.legal_moves:
                    board.push(move)
                    self.fen = board.fen()
                    self.move_history.append(move_str)
                    self.update_position()
                    self.generate_pgn_from_board()
            except Exception as e:
                print(f"Error making move: {e}")
            finally:
                self.reset_selection()

    def reset_selection(self):
        self.move_from = ""
        self.move_to = ""
        self.selected_square = ""
        self.legal_moves = []

    def reset_board(self):
        """Reinicia el tablero a la posición inicial."""
        self.fen = chess.Board().fen()
        self.move_history = []
        self.update_position()
        self.reset_selection()
        self.pgn_text = ""
        self.recommendation = {}

    def generate_pgn_from_board(self):
        """Genera el PGN acumulativo a partir del historial de movimientos."""
        try:
            game = chess.pgn.Game()
            board = chess.Board()
            node = game

            for move_uci in self.move_history:
                move = chess.Move.from_uci(move_uci)
                board.push(move)
                node = node.add_variation(move)

            exporter = chess.pgn.StringExporter(headers=False, variations=False, comments=False)
            pgn_str = game.accept(exporter).strip()

            self.pgn_text = pgn_str
        except Exception as e:
            print(f"Error generating PGN: {e}")

    def load_pgn_to_board(self):
        """Carga el PGN desde el área de texto al tablero interactivo."""
        try:
            game = chess.pgn.read_game(io.StringIO(self.pgn_text))
            if game:
                board = game.board()
                self.move_history = []
                for move in game.mainline_moves():
                    board.push(move)
                    self.move_history.append(move.uci())
                self.fen = board.fen()
                self.update_position()
                self.reset_selection()
        except Exception as e:
            print(f"Error loading PGN: {e}")

    def set_recommended_opening(self, opening: str, style: str):
        self.recommended_opening = {
            "eco": openings[opening],
            "name": f"Apertura {opening.replace('_', ' ')}",
            "style": style,
            "description": _get_opening_description(openings[opening]),
            "plans": _get_plans(openings[opening])
        }

    def _get_opening_name(self, eco_code: str) -> str:
        """Obtiene el nombre de la apertura por código ECO"""
        for style in opening_mapping.values():
            for code, name in style:
                if code == eco_code:
                    return name
        return "Desconocida"

    def _render_board(self, moves: List[str]) -> str:
        """Genera SVG del tablero como Data URI con mejor calidad"""
        board = chess.Board()
        try:
            for move in moves:
                board.push_san(move)

            # Configuración mejorada del SVG
            svg_content = chess.svg.board(
                board=board,
                size=400,
                coordinates=True,
                flipped=False,  # Mostrar desde perspectiva de blancas
                lastmove=board.peek() if board.move_stack else None,  # Resaltar último movimiento
                check=board.king(board.turn) if board.is_check() else None  # Resaltar jaque
            )
            encoded_svg = urllib.parse.quote(svg_content)
            return f"data:image/svg+xml;utf8,{encoded_svg}"
        except Exception as e:
            print(f"Error rendering board: {e}")
            return ""

    def next_move(self):
        if self.current_move < len(self.game_moves) - 1:
            self.current_move += 1
            self.board_svg = self._render_board(self.game_moves[:self.current_move + 1])

    def prev_move(self):
        if self.current_move > 0:
            self.current_move -= 1
            self.board_svg = self._render_board(self.game_moves[:self.current_move + 1])

    def reset_game(self):
        self.current_move = 0
        self.board_svg = self._render_board([self.game_moves[0]])

    @rx.var
    def move_pairs(self) -> List[int]:
        return list(range((len(self.game_moves) + 1) // 2))

    def next_move_second_board(self):
        """Avanza al siguiente movimiento en la reproducción"""
        if self.interactive_current_move < len(self.move_history) - 1:
            self.interactive_current_move += 1
            self.go_to_move(self.interactive_current_move)

    def prev_move_second_board(self):
        """Retrocede al movimiento anterior en la reproducción"""
        if self.interactive_current_move > 0:
            self.interactive_current_move -= 1
            self.go_to_move(self.interactive_current_move)

    def reset_game_second_board(self):
        """Reinicia la reproducción al inicio"""
        self.interactive_current_move = 0
        if self.move_history:
            self.go_to_move(0)

    def go_to_move(self, move_index: int):
        """Va a un movimiento específico en el historial"""
        if 0 <= move_index < len(self.move_history):
            self.interactive_current_move = move_index
            board = chess.Board()
            for i in range(move_index + 1):
                move = chess.Move.from_uci(self.move_history[i])
                board.push(move)
            self.fen = board.fen()
            self.update_position()

    def go_to_last_move(self):
        """Ir al último movimiento"""
        if self.move_history:
            self.interactive_current_move = len(self.move_history) - 1
            self.go_to_move(self.interactive_current_move)

    @rx.var
    def format_move_list(self) -> List[Tuple[int, str, str]]:
        """Formatea los movimientos en notación algebraica (SAN)"""
        moves = []
        board = chess.Board()
        san_moves = []

        for uci_move in self.move_history:
            move = board.parse_uci(uci_move)
            san_moves.append(board.san(move))
            board.push(move)

        for i in range(0, len(san_moves), 2):
            white_move = san_moves[i] if i < len(san_moves) else ""
            black_move = san_moves[i + 1] if i + 1 < len(san_moves) else ""
            moves.append((i // 2 + 1, white_move, black_move))

        return moves