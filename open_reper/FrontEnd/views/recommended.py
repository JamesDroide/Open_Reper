from open_reper.BackEnd.state import State
from open_reper.FrontEnd.components.chess_board import chess_board
from open_reper.FrontEnd.components.header import header
from open_reper.FrontEnd.components.moves_table_static import moves_table_static
from open_reper.FrontEnd.components.opening_description import opening_description, opening_plans
from open_reper.FrontEnd.constants import BLUE_DARK, FONT_FAMILY, ORANGE, ORANGE_HOVER
import reflex as rx

@rx.page(route="/opening-recommended")
def recommended_opening_view():
    return rx.box(
        rx.box(
            rx.flex(
                header("Recomendación de apertura", "Mejora tu juego con recomendaciones basadas en tu estilo"),
                rx.flex(
                    rx.vstack(
                        rx.heading("Apertura Recomendada",
                                font_size="2em",
                                color="white"),
                        rx.heading(
                            State.recommended_opening['name'],
                            font_size="3.5em",
                            color="white",
                            margin_bottom="1em"
                        ),
                        spacing="5",
                        width="100%",
                        max_width="1200px",
                        padding_x="2em",
                        align_items="center"
                    ),
                    bg=BLUE_DARK,
                    width="100%",
                    padding_y="2em"
                ),
                rx.flex(
                    rx.box(
                        chess_board(),
                        padding="1em",
                        bg="#2a5c9a",
                        border_radius="8px",
                        box_shadow="0 4px 8px rgba(0, 0, 0, 0.2)",
                        margin_right="1em"
                    ),
                    moves_table_static(),
                    width="100%",
                    max_width="1200px",
                    margin_x="auto",
                    padding_x=4,
                    justify_content="space-between",
                ),
                opening_description(State.recommended_opening['description']),
                opening_plans(State.recommended_opening['plans']),
                width="100%",
                max_width="1200px",
                margin_x="auto",
                flex_direction="column",
            ),
            background_color=BLUE_DARK,
            width="100%"
        ),
        rx.center(
            rx.button(
                "Analizar Otra Partida",
                bg=ORANGE,
                color="white",
                padding="1em 4em",
                on_click=lambda: rx.redirect("/send-game"),
                border_radius="8px",
                _hover={"bg": ORANGE_HOVER},
                cursor="pointer"
            ),
            bg="#2A5C9A",
            width="100%",
            padding_y="2em"
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