import reflex as rx
from reflex.components.core.breakpoints import Breakpoints
from open_reper.model_loader import analyzer
import asyncio

class State(rx.State):
    pgn_text: str = ""
    recommendation: dict = {}
    is_loading: bool = False
    error: str = ""

    @rx.event
    async def get_recommendation(self):
        self.is_loading = True
        self.error = ""
        try:
            result = await asyncio.get_event_loop().run_in_executor(
            None, 
            lambda: analyzer.recommend_opening(self.pgn_text)
            )
            champion, desc, (eco, name) = result
            self.recommendation = {
                "champion": champion,
                "description": desc,
                "opening": f"{eco} - {name}"
            }
        except Exception as e:
            self.error = f"Error procesando PGN: {str(e)}"
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
                    rx.text(f"Jugador: {State.recommendation['champion']}", color="white"),
                    rx.text(f"Apertura: {State.recommendation['opening']}", color="white"),
                    rx.text(f"Descripción: {State.recommendation['description']}", color="white"),
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
