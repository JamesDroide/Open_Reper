import reflex as rx
from reflex.components.core.breakpoints import Breakpoints
from models.chess_model import ChessStyleAnalyzer

class State(rx.State):
    pgn_content: str = ""
    recommendation: dict = {}
    _model: ChessStyleAnalyzer = None
    is_loading: bool = False

    @classmethod
    def initialize_model(cls):
        if cls._model is None:
            cls._model = ChessStyleAnalyzer.load_model("models/chess_model")
        return cls._model

    @property
    def model(self):
        return self.initialize_model()

    def handle_text_input(self, text: str):
        self.pgn_content = text

    async def get_recommendation(self):
        """Realiza la predicción con el modelo"""
        if not self.pgn_content.strip():
            return rx.window_alert("Ingresa un PGN válido")

        self.is_loading = True
        try:
            champion, desc, opening = model.recommend_opening(self.pgn_content)
            self.recommendation = {
                "champion": champion,
                "description": desc,
                "opening": opening,
            }
        except Exception as e:
            self.recommendation = {"error": str(e)}
        finally:
            self.is_loading = False

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

@rx.page(route = "/send-game")
def send_game():
    return rx.center(
        rx.vstack(
            rx.heading("Recomendador de Aperturas", font_size="2em"),
            rx.text_area(
                placeholder = "Pega tu PGN aquí...",
                on_change = State.handle_text_input,
                height = "200px",
                border = "1px solid #808080",
                padding = "1em"
            ),
            rx.button(
                "Obtener Recomendación",
                on_click=State.get_recommendation,  # Vincular con la función
                bg="#4CAF50",
                color="white",
                margin_top="1em",
            ),
            rx.cond(
                State.recommendation,
                rx.box(
                    rx.text("Recomendación:", font_weight="bold"),
                    rx.text(f"Jugador: {State.recommendation['champion']}"),
                    rx.text(f"Apertura: {State.recommendation['opening']}"),
                    rx.text(f"Descripción: {State.recommendation['description']}"),
                    bg="blue",
                    padding="2em",
                    border_radius="8px",
                    margin_top="2em",
                ),
            ),
            spacing="4",
        ),
        height="100vh",
        background_color="#2A5C9A",
        padding="2em",
    )

@rx.page(route="/opening-recommended")
def opening_recommended():
    return rx.center(
        rx.vstack(
            rx.heading("¡Apertura Recomendada!", font_size="2em"),
            rx.text(f"Apertura: {State.recommendation['opening']}"),
            rx.text(f"Jugador: {State.recommendation['champion']}"),
            rx.text(f"Descripción: {State.recommendation['description']}"),
            rx.link(
                rx.button("Volver a intentar"),
                href="/send-game",
                margin_top="2em"
            ),
            bg="white",
            padding="2em",
            border_radius="8px",
        ),
        height="100vh",
        background_color="#2A5C9A",
        padding="2em",
    )

app = rx.App()
app.add_page(index)
