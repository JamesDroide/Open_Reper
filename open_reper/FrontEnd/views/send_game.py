import reflex as rx

from open_reper.BackEnd.state import State
from open_reper.FrontEnd.components.interactive_chess_board import chess_board
from open_reper.FrontEnd.components.opening_recommendation import opening_recommendation
from open_reper.FrontEnd.constants import BLUE_DARK, FONT_FAMILY
from open_reper.FrontEnd.components.send_pgn_form import send_pgn_form
from open_reper.FrontEnd.components.moves_table import moves_table

@rx.page(route="/send-game", on_load=State.on_load)
def send_game_view():
    return rx.box(
        rx.box(
            rx.flex(
                rx.flex(
                    rx.link(
                        rx.image(
                            src="/logo_open_reper.png",
                            width="200px",
                            height="auto",
                        ),
                        href="/",
                        _hover={"cursor: pointer"},
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
                        margin_right="1em"
                    ),
                    rx.box(
                        moves_table(),
                        padding="1em",
                        bg="#2a5c9a",
                        border_radius="8px",
                        box_shadow="0 4px 8px rgba(0, 0, 0, 0.2)",
                        margin_right="1em",
                        min_width="350px"
                    ),
                    rx.box(
                        send_pgn_form(),
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
        opening_recommendation(),
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