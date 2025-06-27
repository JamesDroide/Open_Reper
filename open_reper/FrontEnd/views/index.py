# frontend/views/index.py
import reflex as rx

from open_reper.FrontEnd.constants import BLUE_DARK, WHITE, ORANGE, FONT_FAMILY

@rx.page(route="/")
def index_view():
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
            "font-family": FONT_FAMILY
        }
    )