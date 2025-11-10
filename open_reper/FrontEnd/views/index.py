# frontend/views/index.py
import reflex as rx

from open_reper.FrontEnd.constants import BLUE_DARK, ORANGE_HOVER, WHITE, ORANGE, FONT_FAMILY

@rx.page(route="/")
def index_view():
    return rx.box(
        rx.box(
            rx.flex(
                rx.link(
                    rx.image(
                        src="logo_open_reper.png",
                        width="140px",
                        height="auto",
                    ),
                    href="/",
                    _hover={"cursor: pointer"},
                ),
                rx.flex(
                    rx.vstack(
                        rx.text(
                            "Domina el juego desde el primer movimiento",
                            font_size="1.8em",
                            color=WHITE,
                            font_weight="bold",
                            text_align="left",
                            line_height="1.2",
                        ),
                        rx.text(
                            "Nuestra app analiza tu estilo de juego, nivel para recomendarte aperturas hechas a tu medida. Con una base de datos de más de 20,000 partidas profesionales, aprenderás no solo a elegir la mejor primera jugada, sino a entender la estrategia detrás de cada movimiento.",
                            font_size="0.95em",
                            color=WHITE,
                            max_width="450px",
                            text_align="justify",
                        ),
                        rx.text(
                            "¿Listo para dejar de improvisar y convertir tus aperturas en victorias?",
                            font_size="0.95em",
                            color=WHITE,
                            max_width="450px",
                            text_align="justify",
                        ),
                        rx.link(
                            rx.button(
                                "USAR LA APP",
                                bg=ORANGE,
                                color=WHITE,
                                border_radius="25px",
                                padding="10px 20px",
                                font_weight="bold",
                                cursor="pointer",
                                width="100%",
                                max_width="220px",
                                height="40px",
                                margin_y=2,
                                _hover={"bg": ORANGE_HOVER, "transform": "translateY(-2px)"},
                                font_size="1.1em",
                            ),
                            href="/send-game",
                            margin_top="15px"
                        ),
                        align_items="center",
                        width="100%",
                        max_width="450px",
                    ),

                    rx.image(
                        src="pieces.png",
                        width="45%",
                        max_width="550px",
                        max_height="500px",
                        object_fit="contain",
                        margin_left="30px",
                    ),
                    width="100%",
                    max_width="1000px",
                    margin_x="auto",
                    padding_x=3,
                ),
                width="100%",
                max_width="1000px",
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
            "font-family": FONT_FAMILY
        }
    )