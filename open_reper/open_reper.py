import reflex as rx
from open_reper.model_loader import analyzer, recommender
import asyncio
import chess
import chess.svg
import urllib.parse
from typing import Dict, List, Tuple, TypedDict

from open_reper.variables import BLUE_DARK, FONT_FAMILY, ORANGE, WHITE

class ChessState(rx.State):
    """Estado para el tablero de ajedrez"""
    fen: str = chess.Board().fen()
    selected_square: str = ""
    move_from: str = ""
    move_to: str = ""
    legal_moves: list[str] = []
    turn: str = "white"
    position: dict = {}
    
    def on_load(self):
        self.reset_board()
    
    def update_position(self):
        """Actualizar posición de piezas desde el FEN"""
        board = chess.Board(self.fen)
        self.position = {}
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                square_name = chess.square_name(square)
                self.position[square_name] = piece.symbol()
    
    def select_square(self, square: str):
        if not self.move_from:
            self.move_from = square
            self.selected_square = square
            board = chess.Board(self.fen)
            self.legal_moves = [
                move.uci()[-2:] 
                for move in board.legal_moves 
                if move.uci()[:2] == square
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
                    self.update_position()
                    self.turn = "white" if board.turn == chess.WHITE else "black"
            except Exception:
                pass
            finally:
                self.reset_selection()
    
    def reset_selection(self):
        self.move_from = ""
        self.move_to = ""
        self.selected_square = ""
        self.legal_moves = []
    
    def reset_board(self):
        self.fen = chess.Board().fen()
        self.update_position()
        self.turn = "white"
        self.reset_selection()

class RecommendedOpening(TypedDict):
    eco: str
    name: str
    style: str
    description: str
    plans: List[str]

class State(rx.State):
    pgn_text: str = ""
    recommendation: dict = {}
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
    game_metadata: dict = {}
    selected_color: str = "white"

    # Mapeo de aperturas
    opening_mapping: Dict[str, List[Tuple[str, str]]] = {
        'posicional': [
            ('E00', 'Apertura Catalana'),
            ('A10', 'Apertura Inglesa'),
            ('D02', 'Sistema Londres')
        ],
        'combinativo': [
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
    
    style_descriptions = {
        'Posicional': 'Aperturas que priorizan el control posicional y estructural.',
        'Combinativo': 'Aperturas dinámicas con combinaciones tácticas agresivas.',
        'Universal': 'Aperturas versátiles que combinan estrategia y táctica.'
    }
    
    openings = {
            'Catalana': 'E00',
            'Inglesa': 'A10',
            'Londres': 'D02',
            'Escocesa': 'C44',
            'Gambito_de_Rey': 'C39',
            'Gambito_Danes': 'C21',
            'Italiana': 'C50',
            'Española': 'C60',
            'Gambito_de_Dama': 'D00'
        }

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
                "description": self.style_descriptions.get(style, ""),
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
            eco_code = self.openings.get(recommended_opening)
            
            if not eco_code:
                self.error = f"No se encontró código ECO para {recommended_opening}"
                return

            # Actualización de estado
            self.recommendation['opening'] = f"Apertura {recommended_opening.replace('_', ' ')}"
            self.set_recommended_opening(recommended_opening, style)
            self.game_moves = self._get_model_games(eco_code)
            self.current_move = 0
            
            if self.game_moves:
                self.board_svg = self._render_board(self.game_moves[:self.current_move+1])

        except Exception as e:
            self.error = f"Error procesando PGN: {str(e)}"
        finally:
            self.is_loading = False

    def set_recommended_opening(self, opening: str, style: str):
        self.recommended_opening = {
            "eco": self.openings[opening],
            "name": f"Apertura {opening.replace('_', ' ')}",
            "style": style,
            "description": self._get_opening_description(self.openings[opening]),
            "plans": self._get_plans(self.openings[opening])
        }

    def _get_opening_name(self, eco_code: str) -> str:
        """Obtiene el nombre de la apertura por código ECO"""
        for style in self.opening_mapping.values():
            for code, name in style:
                if code == eco_code:
                    return name
        return "Desconocida"

    def _get_opening_description(self, eco_code: str) -> str:
        """Descripciones técnicas de las aperturas"""
        descriptions = {
            'E00': "La Apertura Catalana combina desarrollo armónico con presión en el flanco de dama. Ideal para jugadores estratégicos que disfrutan de posiciones sólidas con potencial de ataque en el medio juego.",
            'A10': "La Apertura Inglesa es una estructura flexible que controla el centro con piezas menores. Permite transposiciones a múltiples sistemas y es popular entre jugadores posicionales.",
            'D02': "El Sistema Londres es una apertura universal que crea una estructura de peones sólida. Prioriza el desarrollo rápido y el control del centro con piezas en lugar de peones.",
            'C39': "El Gambito de Rey sacrifica un peón para obtener ventaja en desarrollo. Recomendado para jugadores tácticos que disfrutan de posiciones abiertas y dinámicas.",
            'C44': "La Apertura Escocesa busca el control central inmediato con 1.e4 e5 2.Cf3 Cc6 3.d4. Favorece a jugadores que prefieren posiciones abiertas con juego activo.",
            'C21': "El Gambito Danés ofrece dos peones por un rápido desarrollo. Ideal para jugadores agresivos que buscan ataques directos desde la apertura.",
            'C50': "La Apertura Italiana desarrolla piezas rápidamente hacia el centro. Combina principios clásicos con moderna teoría de desarrollo.",
            'C60': "La Apertura Española es una de las más estudiadas. Crea tensión central con 3.Ab5, llevando a estructuras ricas en estrategia.",
            'D00': "El Gambito de Dama combina desarrollo con presión en el centro. La variante 3.c4 crea dinámicas posiciones con posibilidades para ambos bandos."
        }
        return descriptions.get(eco_code, "Descripción no disponible")

    def _get_plans(self, eco_code: str) -> List[str]:
        """Planes estratégicos por apertura"""
        plans = {
            'E00': [
                "Desarrollar alfiles a g5 y f4",
                "Preparar e4 para controlar el centro",
                "Crear peones colgantes en d4 y e4"
            ],
            'A10': [
                "Controlar el centro con c4 y d3",
                "Desarrollar caballos a f3 y c3",
                "Preparar fianchetto de alfil en g2"
            ],
            'D02': [
                "Desarrollar alfiles a f4 y g5",
                "Crear peón en d4 con c3",
                "Mantener estructura de peones sólida"
            ],
            'C39': [
                "Aprovechar el desarrollo rápido",
                "Atacar el enroque enemigo con Dh5",
                "Mantener presión en columna f"
            ],
            'C44': [
                "Mantener tensión en el centro",
                "Desarrollar alfiles a c4 y b5",
                "Preparar enroque corto"
            ],
            'C21': [
                "Sacar máximo provecho de los peones entregados",
                "Desarrollar piezas con ganancia de tiempo",
                "Lanzar ataque rápido en el flanco rey"
            ],
            'C50': [
                "Desarrollar alfiles a c4 y b5",
                "Preparar enroque corto",
                "Crear tensión en e5"
            ],
            'C60': [
                "Mantener tensión con Ab5",
                "Preparar d4 para abrir el centro",
                "Desarrollar caballo a c3"
            ],
            'D00': [
                "Controlar el centro con peones",
                "Desarrollar alfiles a g5 y f4",
                "Preparar e4 para romper el centro"
            ]
        }
        return plans.get(eco_code, [])

    def _get_opening_moves(self, eco_code: str) -> List[str]:
        """Secuencia de movimientos por apertura"""
        moves = {
            'E00': ["d4", "nf6", "c4", "e6", "g3"],
            'A10': ["c4", "e5", "Nf3", "Nf6", "g3"],
            'D02': ["d4", "d5", "Nf3", "Nf6", "Bf4"],
            'C39': ["e4", "e5", "f4", "exf4"],
            'C44': ["e4", "e5", "Nf3", "Nc6", "d4"],
            'C21': ["e4", "e5", "d4", "exd4", "c3"],
            'C50': ["e4", "e5", "Nf3", "Nc6", "Bc4"],
            'C60': ["e4", "e5", "Nf3", "Nc6", "Bb5"],
            'D00': ["d4", "d5", "c4", "e6", "Nc3"]
        }
        return moves.get(eco_code, [])
    
    def _get_model_games(self, eco_code: str) -> List[str]:
        """Obtiene una lista de movimientos de una partida modelo para la apertura dada"""
        model_games = {
            'E00': [
                        "Nf3", "Nf6",
                        "c4", "e6",
                        "g3", "d5",
                        "d4", "Be7",
                        "Bg2", "O-O",
                        "O-O", "dxc4",
                        "Qc2", "a6",
                        "Qxc4", "b5",
                        "Qc2", "Bb7",
                        "Bd2", "Nc6",
                        "e3", "Nb4",
                        "Bxb4", "Bxb4",
                        "a3", "Be7",
                        "Nbd2", "Rc8",
                        "b4", "a5",
                        "Ne5", "Nd5",
                        "Nb3", "axb4",
                        "Na5", "Ba8",
                        "Nac6", "Bxc6",
                        "Nxc6", "Qd7",
                        "Bxd5", "exd5",
                        "axb4", "Rfe8",
                        "Ra5", "Bf8",
                        "Ne5", "Qe6",
                        "Rxb5", "Rb8",
                        "Rxb8", "Rxb8",
                        "Qxc7", "Bd6",
                        "Qa5", "Bxb4",
                        "Rb1", "Qd6",
                        "Qa4"
                    ],
            'A10': [
                        "c4", "e5",
                        "Nc3", "Nf6",
                        "Nf3", "Nc6",
                        "g3", "d5",
                        "cxd5", "Nxd5",
                        "d3", "Be7",
                        "Bg2", "Be6",
                        "O-O", "O-O",
                        "Bd2", "f5",
                        "Rc1", "Nb6",
                        "a3", "Kh8",
                        "b4", "a5",
                        "b5", "Nd4",
                        "Nxd4", "exd4",
                        "Na4", "Bxa3",
                        "Ra1", "Bd6",
                        "Bxb7", "f4",
                        "Qc2", "Bh3",
                        "Bxa8", "Qxa8",
                        "Qc6", "Qxc6",
                        "bxc6", "fxg3",
                        "hxg3", "Bxf1",
                        "Kxf1", "Bxg3",
                        "Kg2", "Bd6",
                        "Bxa5", "Nxa4",
                        "Rxa4", "Ra8",
                        "e3", "dxe3",
                        "fxe3", "h5",
                        "d4", "Re8",
                        "Bd2", "Kh7",
                        "Ra5", "Kg6",
                        "Kf3", "Rf8+",
                        "Ke2", "h4",
                        "e4", "Be7",
                        "Be3", "Rf6",
                        "Rg5+", "Kf7",
                        "d5", "Rd6",
                        "Rf5+", "Ke8",
                        "Bf4", "g6",
                        "Bxd6", "gxf5",
                        "Bxe7"
                    ],
            'D02': [
                        "d4", "e6",
                        "Nf3", "f5",
                        "Bf4", "Nf6",
                        "e3", "Be7",
                        "Bd3", "O-O",
                        "Nbd2", "d6",
                        "c3", "Nc6",
                        "Qc2", "Qe8",
                        "h3", "Bd7",
                        "Bh2", "g6",
                        "e4", "fxe4",
                        "Nxe4", "Nxe4",
                        "Bxe4", "d5",
                        "Bd3", "Bd6",
                        "Qe2", "Qe7",
                        "O-O", "Bxh2+",
                        "Kxh2", "Rf4",
                        "Bb5", "Qd6",
                        "g3", "Rf5",
                        "Bxc6", "Bxc6",
                        "Ne5", "Raf8",
                        "f3", "Be8",
                        "h4", "c5",
                        "Rfe1", "cxd4",
                        "cxd4", "Qb4",
                        "Qf2", "g5",
                        "hxg5", "Rxg5",
                        "a3", "Qe7",
                        "Rac1", "Rg7",
                        "Qe3", "Bh5",
                        "Kh3", "Qf6",
                        "g4", "Be8",
                        "Kg3", "Qd8",
                        "Rh1", "Qb6",
                        "Rh2", "Qd8",
                        "Rh6", "Qd6",
                        "Kg2", "Bg6",
                        "Rc5", "Qb6",
                        "Qc3", "Qd8",
                        "Qc1", "Qf6",
                        "Rc8", "Qe7",
                        "Rxf8+", "Qxf8",
                        "Rh1", "Qd8",
                        "Qh6", "Qd6",
                        "Qf4", "Qb6",
                        "Rc1", "Qd8",
                        "Kg3", "Be8",
                        "Qh6", "Bg6",
                        "Rc3", "Qf8",
                        "Qc1", "Be8",
                        "Rc8", "Re7",
                        "Qg5+", "Kh8",
                        "Nd3", "Qg7",
                        "Qh5", "Qf8",
                        "Qe5+", "Qg7",
                        "Qb8", "Qf8",
                        "Qxa7", "h5",
                        "Qb8", "hxg4",
                        "fxg4", "Kh7",
                        "Rc7", "b5",
                        "Nf4", "Kg8",
                        "Rxe7", "Qxe7",
                        "Qe5", "Kf7",
                        "g5", "Bd7",
                        "g6+"
                    ],
            'C39': [
                        "e4", "e5",
                        "f4", "exf4",
                        "Bc4", "Nf6",
                        "Nc3", "Bb4",
                        "Nge2", "d5",
                        "exd5", "f3",
                        "gxf3", "O-O",
                        "d4", "Bh3",
                        "Bg5", "Bg2",
                        "Rg1", "Bxf3",
                        "Qd2", "Be7",
                        "O-O-O", "Bh5",
                        "Rde1", "Nbd7",
                        "Nf4", "Bg6",
                        "h4", "Re8",
                        "Qg2", "Bf8",
                        "h5", "Bf5",
                        "Ne6", "fxe6",
                        "dxe6", "Kh8",
                        "exd7", "Rxe1+",
                        "Rxe1", "Bxd7",
                        "h6", "Bc6",
                        "d5", "Bd7",
                        "Rf1", "b5",
                        "Bb3", "Qe8",
                        "d6", "Nh5",
                        "Bf7", "Qe5",
                        "Qxa8"
                    ],
            'C44': [
                        "e4", "e5",
                        "Nf3", "Nc6",
                        "d4", "exd4",
                        "Nxd4", "Bc5",
                        "Be3", "Qf6",
                        "c3", "Nge7",
                        "Bc4", "O-O",
                        "O-O", "Bb6",
                        "Nc2", "d6",
                        "Bxb6", "axb6",
                        "f4", "g5",
                        "f5", "Ne5",
                        "Be2", "Bd7",
                        "c4", "g4",
                        "Nc3", "h5",
                        "Qd2", "Kh8",
                        "Qf4", "Bc6",
                        "Ne3", "Nd7",
                        "Bxg4", "hxg4",
                        "Nxg4", "Qh4",
                        "Rf3", "Ng6",
                        "Qe3", "Qxg4",
                        "Qh6+", "Kg8",
                        "Rh3", "Qxh3",
                        "gxh3", "Nge5",
                        "f6", "Nxf6",
                        "Qxf6", "Rae8",
                        "Kh1", "Ng6",
                        "h4", "Re6",
                        "Qg5", "Rfe8",
                        "h5", "Re5",
                        "Qh6", "Rxe4",
                        "Nxe4", "Rxe4",
                        "Kg1", "Ne5",
                        "Qg5+", "Kh7",
                        "Qf5+", "Kh6",
                        "Rf1", "Re2",
                        "Qf6+", "Kh7",
                        "Qg5", "Be4",
                        "h6", "Bg6",
                        "h4", "Re4",
                        "h5", "Rg4+",
                        "Qxg4", "Nxg4",
                        "hxg6+", "fxg6",
                        "Rf7+", "Kxh6",
                        "Rxc7", "Ne5",
                        "Rxb7", "Nxc4",
                        "b3"
                    ],
            'C21': [
                        "e4", "e5",
                        "d4", "exd4",
                        "c3", "dxc3",
                        "Nxc3", "Bb4",
                        "Bc4", "Bxc3+",
                        "bxc3", "d6",
                        "Qb3", "Qe7",
                        "Ne2", "Nc6",
                        "O-O", "Nf6",
                        "Nd4", "Nxd4",
                        "cxd4", "O-O",
                        "Re1", "h6",
                        "Ba3", "Ng4",
                        "f3", "Nf6",
                        "e5", "Nd7",
                        "exd6", "Qf6",
                        "dxc7", "Qxd4+",
                        "Kh1", "Nc5",
                        "Bxf7+", "Rxf7",
                        "Bxc5", "Qf6",
                        "Rad1", "b6",
                        "Rd6", "Qf5",
                        "Rd5", "Qf6",
                        "Be7", "Rxe7",
                        "Re7", "Kf8",
                        "Re1", "Bb7",
                        "Rd7", "Bc6",
                        "Qb4+", "Kg8",
                        "Qc4+", "Kh8",
                        "Qxc6", "Rc8",
                        "Rd8", "Rxd8",
                        "cxd8=Q"
                    ],
            'C50': [
                        "e4", "e5",
                        "Nf3", "Nc6",
                        "Bc4", "Bc5",
                        "Nc3", "Nf6",
                        "d3", "d6",
                        "Be3", "Bxe3",
                        "fxe3", "Na5",
                        "Bb3", "Nxb3",
                        "axb3", "Ng4",
                        "Qe2", "f6",
                        "d4", "c6",
                        "O-O-O", "Qe7",
                        "h3", "Nh6",
                        "g4", "Bd7",
                        "Nh4", "g6",
                        "Nf3", "Nf7",
                        "Rdg1", "O-O-O",
                        "b4", "Kb8",
                        "Qf2", "Rdf8",
                        "Qg3", "h6",
                        "Rf1", "Nd8",
                        "Rhg1", "Ne6",
                        "Rf2", "Nc7",
                        "Rgf1", "Rfg8",
                        "Nh4", "Ne8",
                        "b5", "Ka8",
                        "bxc6", "bxc6",
                        "Nf3", "g5",
                        "Rg2", "h5",
                        "b3", "Rh6",
                        "Kb2", "Rgh8",
                        "Qf2", "Nc7",
                        "Ra1", "Rb8",
                        "Qe2", "Rb7",
                        "Rgg1", "Rh8",
                        "Rad1", "hxg4",
                        "hxg4", "Rc8",
                        "Qd3", "Be6",
                        "Nd2", "Nb5",
                        "Ndb1", "Rbc7",
                        "Na4", "Rb7",
                        "Kc1", "Rcb8",
                        "Rg2", "Rd7",
                        "Nbc3", "Nc7",
                        "d5", "cxd5",
                        "exd5", "Bg8",
                        "Qc4", "Rc8",
                        "Kb2", "Rb8",
                        "e4", "Rdd8",
                        "Rf2", "Rf8",
                        "Rdf1", "Bh7",
                        "Rxf6", "Rxf6",
                        "Rxf6", "Qxf6",
                        "Qxc7", "Qh8",
                        "Qc6+", "Rb7",
                        "Nb5", "Kb8",
                        "Qxd6+", "Kc8",
                        "Qc6+"
                    ],
            'C60': [
                        "e4", "e5",
                        "Nf3", "Nc6",
                        "Bb5", "a6",
                        "Ba4", "Nf6",
                        "O-O", "Be7",
                        "Re1", "b5",
                        "Bb3", "d6",
                        "c3", "O-O",
                        "h3", "Bb7",
                        "d4", "Re8",
                        "Ng5", "Rf8",
                        "Nf3", "Re8",
                        "Nbd2", "Bf8",
                        "Bc2", "g6",
                        "a4", "Bg7",
                        "d5", "Nb8",
                        "Bd3", "bxa4",
                        "Qxa4", "c6",
                        "c4", "Qc7",
                        "Nb3", "Nbd7",
                        "Bd2", "Reb8",
                        "Qa3", "Ne8",
                        "dxc6", "Bxc6",
                        "Na5", "Nc5",
                        "b4", "Nxd3",
                        "Qxd3", "Bd7",
                        "Rac1", "Rd8",
                        "Nh2", "Nf6",
                        "Nf1", "Nh5",
                        "Ne3", "Nf4",
                        "Qa3", "Rdc8",
                        "Nd5", "Nxd5",
                        "exd5", "f5",
                        "f4", "Re8",
                        "Bc3", "exf4",
                        "Bxg7", "Kxg7",
                        "Qc3+", "Kg8",
                        "c5", "Bb5",
                        "Qd2", "g5",
                        "Nb3", "Qf7",
                        "cxd6", "Re4",
                        "Nc5", "Rae8",
                        "Ne6", "R8xe6",
                        "dxe6", "Qxe6",
                        "Rxe4", "fxe4",
                        "Rc5", "h6",
                        "Qd5"
                    ],
            'D00': [
                        "d4", "Nf6",
                        "c4", "e6",
                        "Nf3", "d5",
                        "Nc3", "c6",
                        "Bg5", "h6",
                        "Bh4", "dxc4",
                        "e4", "g5",
                        "Bg3", "b5",
                        "Be2", "b4",
                        "Na4", "Nxe4",
                        "Be5", "Nf6",
                        "Nc5", "c3",
                        "bxc3", "bxc3",
                        "O-O", "Nbd7",
                        "Nxd7", "Bxd7",
                        "Qb3", "Bg7",
                        "Qa3", "g4",
                        "Ne1", "c5",
                        "dxc5", "O-O",
                        "Bxc3", "h5",
                        "Rd1", "Nd5",
                        "Bxg7", "Kxg7",
                        "Bc4", "Bc6",
                        "Nc2", "Qf6",
                        "Nd4", "Ne7",
                        "f3", "g3",
                        "hxg3", "Rfd8",
                        "Nxc6", "Nxc6",
                        "Qe3", "Nd4",
                        "g4", "Rac8",
                        "g5", "Qf5",
                        "Rxd4", "Qxc5",
                        "Bxe6", "Rc6",
                        "Re4", "Qxe3+",
                        "Rxe3", "Rxe6",
                        "Rxe6", "fxe6",
                        "Re1", "Rd6",
                        "Kh2", "Kg6",
                        "f4", "Kf5",
                        "Kg3", "h4+",
                        "Kxh4", "Kxf4",
                        "g6", "Rd8",
                        "Rf1+", "Ke3",
                        "Kg5", "e5",
                        "g7"
                    ]
        }
        return model_games.get(eco_code, [])

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
        if self.current_move < len(self.game_moves)-1:
            self.current_move += 1
            self.board_svg = self._render_board(self.game_moves[:self.current_move+1])

    def prev_move(self):
        if self.current_move > 0:
            self.current_move -= 1
            self.board_svg = self._render_board(self.game_moves[:self.current_move+1])

    def reset_game(self):
        self.current_move = 0
        self.board_svg = self._render_board([self.game_moves[0]])

    def rate_recommendation(self, stars: int):
        self.rating = stars

    @rx.var
    def move_pairs(self) -> List[int]:
        return list(range((len(self.game_moves) + 1) // 2))

@rx.page(route="/")
def index():
    return rx.box(
        rx.box(
            rx.flex(
                rx.link(
                    rx.image(
                    src="logo_open_reper.png",
                    width="200px",
                    height="auto",
                    ),
                    href="/",
                    _hover={"cursor: pointer"},
                ),
                rx.flex(
                    rx.vstack(
                        rx.text(
                            "Domina el juego desde el primer movimiento",
                            font_size="2.8em",
                            color=WHITE,
                            font_weight="bold",
                            text_align="left",
                            line_height="1.2",
                        ),
                        rx.text(
                            "Nuestra app analiza tu estilo de juego, nivel para recomendarte aperturas hechas a tu medida. Con una base de datos de más de 20,000 partidas profesionales, aprenderás no solo a elegir la mejor primera jugada, sino a entender la estrategia detrás de cada movimiento.",
                            font_size="1.3em",
                            color=WHITE,
                            max_width="600px",
                            text_align="justify",
                        ),
                        rx.text(
                            "¿Listo para dejar de improvisar y convertir tus aperturas en victorias?",
                            font_size="1.3em",
                            color=WHITE,
                            max_width="600px",
                            text_align="justify",
                        ),
                        rx.link(
                            rx.button(
                                "USAR LA APP",
                                bg=ORANGE,
                                color=WHITE,
                                border_radius="30px",
                                padding="15px 30px",
                                font_weight="bold",
                                cursor="pointer",
                                width="100%",
                                max_width="300px",
                                height="50px",
                                margin_y=4,
                                _hover={"bg": "#e03d00", "transform": "translateY(-2px)"},
                                font_size="1.5em",
                            ),
                            href="/send-game",
                            margin_top="20px"
                        ),
                        align_items="center",
                        width="100%",
                        max_width="600px",
                    ),
                    
                    rx.image(
                        src="pieces.png",
                        width="50%",
                        max_width="800px",
                        max_height="700px",
                        object_fit="contain",
                        margin_left="50px",
                    ),
                    width="100%",
                    max_width="1200px",
                    margin_x="auto",
                    padding_x=4,
                ),
                width="100%",
                max_width="1200px",
                margin_x="auto",
                flex_direction="column",
            ),
            background_color=BLUE_DARK,
            width="100%",
        ),
        style={
            "position": "fixed",
            "top": 0,
            "left": 0,
            "right": 0,
            "bottom": 0,
            "overflow": "auto",
            "background": BLUE_DARK,
            "font-family" : FONT_FAMILY
        }
    )

@rx.page(route="/send-game")
def send_game():
    ChessState.on_load()
    return rx.box(
        rx.box(
            rx.flex(
                rx.flex(
                    rx.image(
                        src="/logo_open_reper.png",
                        width="200px",
                        height="auto",
                        border_radius="8px"
                    ),
                    rx.vstack(
                        rx.heading("Aprende y mejora tus aperturas", font_size="2em", color="white"),
                        rx.text("Analiza tus partidas y descubre nuevas estrategias", color="#d1e0e0"),
                        spacing="1",
                        align_items="center",
                        flex_grow=1
                    ),
                    justify_content="space-between",
                    align_items="center",
                    width="100%",
                    padding="1em",
                    bg=BLUE_DARK
                ),
                rx.flex(
                    rx.box(
                             chess_board(),
                             padding="1em",
                             bg="#2a5c9a",
                             border_radius="8px",
                             box_shadow="0 4px 8px rgba(0, 0, 0, 0.2)",
                             margin_right="2em"
                         ),
                    
                    rx.box(
                            rx.vstack(
                                rx.heading("Envía tu partida PGN", font_size="1.5em", color="white"),
                                rx.text_area(
                                    placeholder="Pega tu PGN aquí...",
                                    on_change=State.set_pgn_text,
                                    width="400px",
                                    height="200px",
                                    border="1px solid #808080",
                                    padding="1em",
                                    color="black",
                                    bg="white"
                                ),
                                rx.heading("Selecciona tu color:", font_size="1.2em", color="white"),
                                rx.hstack(
                                    rx.image(
                                        src="/white-pawn.png",
                                        width="64px",
                                        height="64px",
                                        border=rx.cond(
                                            State.selected_color == "white",
                                            "3px solid #F24100",
                                            "3px solid transparent"
                                        ),
                                        border_radius="8px",
                                        on_click=lambda: State.set_selected_color("white"),
                                        cursor="pointer",
                                        transition="transform 0.2s",
                                        _hover={"transform": "scale(1.1) rotate(-5deg)"},
                                        _active={"transform": "scale(0.95) rotate(5deg)"}
                                    ),
                                    rx.image(
                                        src="/black-pawn.png",
                                        width="64px",
                                        height="64px",
                                        border=rx.cond(
                                            State.selected_color == "black",
                                            "3px solid #F24100",
                                            "3px solid transparent"
                                        ),
                                        border_radius="8px",
                                        on_click=lambda: State.set_selected_color("black"),
                                        cursor="pointer",
                                        transition="transform 0.2s",
                                        _hover={"transform": "scale(1.1) rotate(-5deg)"},
                                        _active={"transform": "scale(0.95) rotate(5deg)"}
                                    ),
                                    spacing="4",
                                    margin_top="2em",
                                    justify_content="center"
                                ),
                                rx.cond(
                                    State.selected_color == "white",
                                    rx.badge("Blancas seleccionadas", color_scheme="orange"),
                                    rx.badge("Negras seleccionadas", color_scheme="orange")
                                ),
                                rx.button(
                                    "Obtener Recomendación",
                                    on_click=State.get_recommendation,
                                    bg=ORANGE,
                                    color=WHITE,
                                    margin_top="1em",
                                    is_loading=State.is_loading,
                                    _hover={"bg": "#e03d00"},
                                    font_family=FONT_FAMILY
                                ),
                                rx.cond(
                                    State.error,
                                    rx.text(State.error, color="red", font_weight="bold"),
                                ),
                                rx.cond(
                                    State.recommendation,
                                    rx.box(
                                        rx.text("Recomendación:", font_weight="bold", color="white"),
                                        rx.text(f"Estilo: {State.recommendation['style']}", color="white"),
                                        rx.text(f"Apertura: {State.recommendation['opening']}", color="white"),
                                        rx.link(
                                            rx.button(
                                                "Ver detalles de la apertura",
                                                bg="#1E3A5F",
                                                color="white",
                                                border_radius="8px",
                                                padding_x=4,
                                                margin_top=4
                                            ),
                                            href="/opening-recommended"
                                        ),
                                        bg="#1E3A5F",
                                        padding="2em",
                                        border_radius="8px",
                                        margin_top="2em",
                                        width="100%",
                                        max_width="600px"
                                    ),
                                ),
                                spacing="4",
                                align="center",
                                width="100%",
                                max_width="800px"
                            ),
                        ),
                    width="100%",
                    max_width="1200px",
                    margin_x="auto",
                    padding_x=4,
                ),
                width="100%",
                max_width="1200px",
                margin_x="auto",
                flex_direction="column",
            ),
            background_color=BLUE_DARK,
            width="100%",
        ),
        style={
            "position": "fixed",
            "top": 0,
            "left": 0,
            "right": 0,
            "bottom": 0,
            "overflow": "auto",
            "background": BLUE_DARK,
            "font-family" : FONT_FAMILY
        }
    )

def chess_square(square: str):
    """Componente para una casilla del tablero con imágenes"""
    is_selected = ChessState.selected_square == square
    is_legal_move = ChessState.legal_moves.contains(square)
    
    is_light = (ord(square[0]) - ord('a') + int(square[1])) % 2 == 1
    base_bg_color = "#f0d9b5" if is_light else "#b58863"
    
    bg_color = rx.cond(
        is_selected,
        "#bbcb2b",
        rx.cond(is_legal_move, "#86a666", base_bg_color)
    )
    
    piece_symbol = rx.cond(
        ChessState.position.contains(square),
        ChessState.position[square],
        ""
    )
    
    piece_component = rx.match(
        piece_symbol,
        *[(symbol, component) for symbol, component in PIECE_MAP.items()],
        rx.box(width="50px", height="50px")
    )
    
    return rx.box(
        piece_component,
        on_click=lambda: ChessState.select_square(square),
        width="60px",
        height="60px",
        display="flex",
        justify_content="center",
        align_items="center",
        bg=bg_color,
        border="1px solid #444",
        _hover={"cursor": "pointer", "filter": "brightness(1.2)"}
    )

def chess_board():
    """Componente completo del tablero de ajedrez"""
    ranks = range(8, 0, -1)  # Filas 8 a 1
    files = "abcdefgh"       # Columnas a a h
    
    return rx.vstack(
        rx.heading("Tablero de Ajedrez Interactivo", color="white", font_size="1.5em"),
        rx.box(
            rx.flex(
                *[chess_square(f"{file}{rank}") for rank in ranks for file in files],
                wrap="wrap",
                width="480px",
                height="480px",
            ),
            border="4px solid #333",
            box_shadow="0 10px 25px rgba(0, 0, 0, 0.5)",
            overflow="hidden",
        ),
        rx.hstack(
            rx.button(
                "Reiniciar Tablero",
                on_click=ChessState.reset_board,
                bg="#FF5722",
                color="white",
                _hover={"bg": "#E64A19"}
            ),
            rx.text(
                rx.cond(
                    ChessState.turn == "white",
                    "Turno: Blancas",
                    "Turno: Negras"
                ),
                color="white",
                font_weight="bold"
            ),
            spacing="4",
            margin_top="1em"
        ),
        align="center",
    )

PIECE_MAP = {
    'r': rx.image(src="/game_pieces/bR.png", width="50px", height="50px"),
    'n': rx.image(src="/game_pieces/bN.png", width="50px", height="50px"),
    'b': rx.image(src="/game_pieces/bB.png", width="50px", height="50px"),
    'q': rx.image(src="/game_pieces/bQ.png", width="50px", height="50px"),
    'k': rx.image(src="/game_pieces/bK.png", width="50px", height="50px"),
    'p': rx.image(src="/game_pieces/bP.png", width="50px", height="50px"),
    'R': rx.image(src="/game_pieces/wR.png", width="50px", height="50px"),
    'N': rx.image(src="/game_pieces/wN.png", width="50px", height="50px"),
    'B': rx.image(src="/game_pieces/wB.png", width="50px", height="50px"),
    'Q': rx.image(src="/game_pieces/wQ.png", width="50px", height="50px"),
    'K': rx.image(src="/game_pieces/wK.png", width="50px", height="50px"),
    'P': rx.image(src="/game_pieces/wP.png", width="50px", height="50px"),
}

@rx.page(route="/opening-recommended")
def recommended_opening():
    return rx.center(
        rx.vstack(
            rx.heading("Apertura Recomendada", font_size="2em", color="white"),
            rx.heading(
                State.recommended_opening['name'],
                font_size="3em",
                color="white",
                margin_bottom="1em"
            ),
            
            # Sección del tablero y controles
            rx.vstack(
                rx.image(
                    src=State.board_svg,
                    width=["300px", "400px"],
                    height=["300px", "400px"],
                    alt="Tablero de Ajedrez",
                    margin_bottom="1em",
                ),
                rx.hstack(
                    rx.button(
                        "← Anterior",
                        on_click=State.prev_move,
                        bg="#1E3A5F",
                        color="white",
                        disabled=State.current_move <= 0,
                    ),
                    rx.text(
                        f"Movimiento {State.current_move + 1} de {State.game_moves.length()}",
                        color="white",
                        padding="0 1em"
                    ),
                    rx.button(
                        "Siguiente →",
                        on_click=State.next_move,
                        bg="#1E3A5F",
                        color="white",
                        disabled=State.current_move >= State.game_moves.length() - 1,
                    ),
                    rx.button(
                        "Reiniciar",
                        on_click=State.reset_game,
                        bg="#F24100",
                        color="white",
                        margin_left="1em"
                    ),
                    spacing="3",
                    margin_bottom="1em",
                    align="center"
                ),
                align_items="center",
            ),
            
            # Visualización de la secuencia de movimientos
            rx.box(
                rx.heading("Secuencia de Movimientos", font_size="1.5em", color="white", margin_bottom="0.5em"),
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("#", width="50px"),
                            rx.table.column_header_cell("Blancas", width="150px"),
                            rx.table.column_header_cell("Negras", width="150px"),
                        )
                    ),
                    rx.table.body(
                        rx.foreach(
                            State.move_pairs,
                            lambda i: rx.table.row(
                                rx.table.cell(f"{i+1}.", color="white"),
                                rx.table.cell(
                                    rx.cond(
                                        i*2 < State.game_moves.length(),
                                        State.game_moves[i*2],
                                        ""
                                    ),
                                    color="white"
                                ),
                                rx.table.cell(
                                    rx.cond(
                                        i*2+1 < State.game_moves.length(),
                                        State.game_moves[i*2+1],
                                        ""
                                    ),
                                    color="white"
                                )
                            )
                        )
                    ),
                    bg="#1E3A5F",
                    padding="1em",
                    border_radius="8px",
                    width="100%"
                ),
                width="100%",
                max_width="600px",
                margin_bottom="2em"
            ),
            
            # Información de la apertura
            rx.box(
                rx.heading("Sobre esta Apertura", font_size="1.5em", color="white", margin_bottom="0.5em"),
                rx.text(
                    State.recommended_opening['description'],
                    color="white",
                    font_size="1.1em",
                    line_height="1.6",
                    margin_bottom="1em"
                ),
                rx.heading("Planes Estratégicos", font_size="1.3em", color="white", margin_bottom="0.5em"),
                rx.unordered_list(
                    rx.foreach(
                        State.recommended_opening["plans"],
                        lambda plan: rx.list_item(
                            plan,
                            color="white",
                            margin_bottom="0.5em",
                            font_size="1.1em"
                        )
                    ),
                    padding_left="1.5em"
                ),
                width="100%",
                max_width="800px"
            ),
            
            # Botones de acción
            rx.vstack(
                rx.button(
                    "Analizar Otra Partida",
                    bg="#F24100",
                    color="white",
                    padding="1em 2em",
                    on_click=lambda: rx.redirect("/send-game"),
                    margin_bottom="1em"
                ),
                
                align_items="center"
            ),
            
            spacing="4",
            align_items="center",
            width="100%",
            padding="1em"
        ),
        height="auto",
        background_color="#2A5C9A",
        padding="2em"
    )

app = rx.App(stylesheets=["https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&display=swap"])
app.add_page(index, route = "/")
app.add_page(send_game, route = "/send-game")
app.add_page(recommended_opening, route = "/opening-recommended")