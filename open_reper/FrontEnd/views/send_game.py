import reflex as rx

from open_reper.BackEnd.state import State
from open_reper.FrontEnd.components.header import header
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
                header("Envía tu partida", "Analiza tus partidas y descubre nuevas aperturas"),
                rx.flex(
                    rx.box(
                        chess_board(),
                        padding="1em",
                        bg=BLUE_DARK,
                        margin_right="1em"
                    ),
                    rx.box(
                        moves_table(),
                        padding="1em",
                        bg=BLUE_DARK,
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
        rx.flex(
            rx.foreach(
                State.recommended_openings,
                lambda opening: opening_recommendation(
                    type_recommendation=opening["type"],
                    style=opening["style"],
                    description=opening["description"],
                    opening=opening["name"]
                )
            ),
            display="grid",
            grid_template_columns="repeat(2, 1fr)",
            gap="2em",
            justify_content="center",
            padding="2em",
            max_width="1200px",
            margin="0 auto",
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