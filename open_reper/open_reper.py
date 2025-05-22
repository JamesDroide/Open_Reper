import reflex as rx
from reflex.components.core.breakpoints import Breakpoints
from open_reper.model_loader import analyzer
import asyncio
import chess
import chess.svg
import urllib.parse
from typing import Dict, List, Tuple, TypedDict

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

    @rx.event
    async def get_recommendation(self):
        self.is_loading = True
        self.error = ""
        try:
            result = await asyncio.get_event_loop().run_in_executor(
                None, 
                lambda: analyzer.recommend_opening(self.pgn_text)
            )
            
            if result['status'] == 'success':
                style = result['style']
                opening = result['opening']
                eco_code = opening['eco']
                self.recommendation = {
                    "champion": style,
                    "description": self.style_descriptions.get(style, ""),
                    "opening": f"{eco_code} - {opening['name']}"
                }
                # Actualizar recommended_opening y movimientos
                self.set_recommended_opening(eco_code, style)
                self.game_moves = self._get_opening_moves(eco_code)
                self.current_move = 0
                if self.game_moves:
                    self.board_svg = self._render_board(self.game_moves[:self.current_move+1])
            else:
                self.error = result['message']
        except Exception as e:
            self.error = f"Error procesando PGN: {str(e)}"
        finally:
            self.is_loading = False

    def set_recommended_opening(self, eco_code: str, style: str):
        self.recommended_opening = {
            "eco": eco_code,
            "name": self._get_opening_name(eco_code),
            "style": style,
            "description": self._get_opening_description(eco_code),
            "plans": self._get_plans(eco_code)
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
            'E00': ["d4", "Cf6", "c4", "e6", "g3"],
            'A10': ["c4", "e5", "Cf3", "Cf6", "g3"],
            'D02': ["d4", "d5", "Cf3", "Cf6", "Ab5+"],
            'C39': ["e4", "e5", "Cf3", "exf4", "Ac4"],
            'C44': ["e4", "e5", "Cf3", "Cc6", "d4"],
            'C21': ["e4", "e5", "Cf3", "d5", "exd5"],
            'C50': ["e4", "e5", "Cf3", "Cc6", "Ac4"],
            'C60': ["e4", "e5", "Cf3", "Cc6", "Ab5"],
            'D00': ["d4", "d5", "c4", "e6", "Cc3"]
        }
        return moves.get(eco_code, [])

    def _render_board(self, moves: List[str]) -> str:
        """Genera SVG del tablero como Data URI"""
        board = chess.Board()
        try:
            for move in moves:
                board.push_san(move)
            svg_content = chess.svg.board(board=board, size=400)
            encoded_svg = urllib.parse.quote(svg_content)
            return f"data:image/svg+xml;utf8,{encoded_svg}"
        except Exception:
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

def index():
    return rx.box(
        rx.flex(
            rx.box(
                rx.image(
                    src="logo_open_reper.png",
                    width="auto",
                    height="150px",
                    margin_bottom=4,
                ),
                rx.vstack(
                    rx.text("Domina el juego desde", 
                            font_size=["2em", "3em"],
                            color="white", 
                            font_weight="bold"),
                    rx.text("el primer movimiento", 
                            font_size=["2em", "3em"], 
                            color="white", 
                            font_weight="bold"),
                    rx.text(
                        "Nuestra app analiza tu estilo de juego, nivel para recomendarte aperturas hechas a tu medida. Con una base de datos de más de 20,000 partidas profesionales, aprenderás no solo a elegir la mejor primera jugada, sino a entender la estrategia detrás de cada movimiento.",
                        font_size=["1em", "1.2em"],
                        color="white",
                        margin_top=4,
                    ),
                    rx.text(
                        "¿Listo para dejar de improvisar y convertir tus aperturas en victorias?",
                        font_size=["1em", "1.2em"],
                        color="white",
                        margin_top=2,
                    ),
                    rx.link(
                        rx.button(
                            "USAR LA APP",
                            bg="#F24100",
                            color="white",
                            border_radius="30px",
                            padding_x=8,
                            padding_y=4,
                            margin_top=6,
                            font_weight="bold",
                            align_self="center",
                            cursor="pointer"
                        ),
                        href="/send-game"
                    ),
                    spacing="4",
                    align_items="flex-start",
                    width="100%",
                ),
                width="50%",
                display=Breakpoints(
                mobile="none",
                desktop="block"
            ),
            ),
            rx.image(
                src="pieces.png",
                width=["100%", "50%"],
                max_width="700px",
                max_height="600px",
                object_fit="contain",
                margin_left=["0", "8"],
                display=Breakpoints(
                mobile="block",
                desktop="block"
            ),
            ),
            direction=Breakpoints(
                mobile="column",
                desktop="row"
            ),
            align_items="center",
            justify_content="space-between",
            padding_x=8,
            padding_y=8,
            background_color="#2A5C9A",
            height="100%",
        ),
    )

@rx.page(route="/send-game")
def send_game():
    return rx.center(
        rx.vstack(
            rx.heading("Recomendador de Aperturas", font_size="2em", color="white"),
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
            rx.button(
                "Obtener Recomendación",
                on_click=State.get_recommendation,
                bg="#4CAF50",
                color="white",
                margin_top="1em",
                is_loading=State.is_loading,
                _hover={"bg": "#45a049"}
            ),
            rx.cond(
                State.error,
                rx.text(State.error, color="red", font_weight="bold"),
            ),
            rx.cond(
                State.recommendation,
                rx.box(
                    rx.text("Recomendación:", font_weight="bold", color="white"),
                    rx.text(f"Estilo: {State.recommendation['champion']}", color="white"),
                    rx.text(f"Apertura: {State.recommendation['opening']}", color="white"),
                    rx.text(f"Descripción: {State.recommendation['description']}", color="white"),
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
        height="100vh",
        background_color="#2A5C9A",
        padding="2em",
    )

@rx.page(route="/opening-recommended")
def recommended_opening():
    return rx.center(
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.image(
                        src="logo_open_reper.png",
                        width="150px",
                        margin_bottom=4,
                    ),
                    rx.heading(
                        "Recomendación de Apertura",
                        font_size="2em",
                        color="white"
                    )
                ),
                rx.heading(
                    State.recommended_opening['name'],
                    font_size="3em",
                    color="white",
                    margin_y="1em"
                ),
                rx.box(
                    rx.image(
                        src=State.board_svg,
                        alt="Tablero de ajedrez",
                        width="100%",
                        max_width="600px"
                    ),
                    rx.hstack(
                        rx.button(
                            "⏮",
                            on_click=State.reset_game,
                            bg="#4CAF50",
                            color="white",
                            border_radius="50%",
                            padding="0.5em",
                            margin="0.5em"
                        ),
                        rx.button(
                            "⏪",
                            on_click=State.prev_move,
                            bg="#4CAF50",
                            color="white",
                            border_radius="50%",
                            padding="0.5em",
                            margin="0.5em"
                        ),
                        rx.text(
                            f"{State.current_move+1}/{State.game_moves.length}",
                            color="white",
                            font_size="1.2em"
                        ),
                        rx.button(
                            "⏩",
                            on_click=State.next_move,
                            bg="#4CAF50",
                            color="white",
                            border_radius="50%",
                            padding="0.5em",
                            margin="0.5em"
                        ),
                        spacing="1",
                        align_items="center"
                    ),
                    align_items="center"
                ),
                rx.vstack(
                    rx.heading("Movimientos", font_size="1.5em", color="white"),
                    rx.foreach(
                        State.game_moves,
                        lambda move, index: rx.button(
                            f"{index+1}. {move}",
                            bg="#1E3A5F",
                            color="white",
                            border_radius="8px",
                            padding="0.5em 1em",
                            margin="0.2em",
                            on_click=lambda: State.set_current_move(index)
                        )
                    ),
                    spacing="1"
                ),
                rx.box(
                    rx.heading("Descripción", font_size="1.5em", color="white"),
                    rx.text(
                        State.recommended_opening['description'],
                        color="white",
                        margin_y="1em"
                    ),
                    rx.heading("Planes de Juego", font_size="1.5em", color="white"),
                    rx.unordered_list(
                        rx.foreach(
                            State.recommended_opening["plans"],
                            lambda plan: rx.list_item(plan, color="white")
                        )
                    ),
                    margin_top="2em"
                ),
                rx.hstack(
                    rx.button(
                        "Nueva Consulta",
                        bg="#F24100",
                        color="white",
                        padding="1em 2em",
                        on_click=lambda: rx.redirect("/send-game")
                    ),
                    rx.text("Califica esta recomendación:", color="white"),
                    rx.foreach(
                        [1,2,3,4,5],
                        lambda star: rx.icon(
                            tag="star",
                            on_click=lambda s=star: State.rate_recommendation(s),
                            color=rx.cond(
                                star <= State.rating,
                                "gold",
                                "gray"
                            ),
                            cursor="pointer"
                        )
                    ),
                    spacing="2"
                ),
                spacing="2",
                align_items="center"
            ),
            bg="#2A5C9A",
            padding="2em",
            border_radius="8px",
            width="100%",
            max_width="1200px"
        ),
        height="100vh",
        background_color="#2A5C9A",
        padding="2em"
    )

app = rx.App()
app.add_page(index)