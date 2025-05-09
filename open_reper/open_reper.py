import reflex as rx
from fastapi import FastAPI
from reflex.components.core.breakpoints import Breakpoints

fastapi_app = FastAPI(title = "Open Reper")

@fastapi_app.get("/api/items")
async def get_items():
    return dict(items = ["Item 1", "Item 2", "Item 3"])

class State(rx.State):
    pass

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
            height="100vh",
        ),
    )

def customize_component(value):
    return rx.progress(value = value)

@rx.page(route = "/send-game")
def send_game():
    return rx.text("Envia tu partida aqui")

@rx.page(route = "/opening-recommended")
def opening_recommended():
    return rx.heading("Apertura recomendada es")

app = rx.App(api_transformer=fastapi_app)
app.add_page(index)
