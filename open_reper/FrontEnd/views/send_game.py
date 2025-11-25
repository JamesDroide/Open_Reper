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
        # Versión Desktop
        rx.desktop_only(
            rx.box(
                rx.flex(
                    header("Envía tu partida", "Analiza tus partidas y descubre nuevas aperturas"),
                    rx.flex(
                        rx.box(
                            chess_board(),
                            padding="0.7em",
                            bg=BLUE_DARK,
                            margin_right="0.7em"
                        ),
                        rx.box(
                            moves_table(),
                            padding="0.7em",
                            bg=BLUE_DARK,
                            margin_right="0.7em",
                            min_width="280px"
                        ),
                        rx.box(
                            send_pgn_form(),
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
                    gap="1.5em",
                    justify_content="center",
                    padding="1.5em",
                    max_width="1000px",
                    margin="0 auto",
                ),
                background_color=BLUE_DARK,
                width="100%",
            )
        ),
        
        # Versión Tablet
        rx.tablet_only(
            rx.box(
                rx.flex(
                    header("Envía tu partida", "Analiza tus partidas"),
                    rx.vstack(
                        rx.center(
                            rx.box(
                                chess_board(),
                                padding="0.6em",
                                bg=BLUE_DARK,
                            ),
                            width="100%",
                        ),
                        rx.flex(
                            rx.box(
                                moves_table(),
                                padding="0.6em",
                                bg=BLUE_DARK,
                                width="50%",
                            ),
                            rx.box(
                                send_pgn_form(),
                                width="50%",
                            ),
                            width="100%",
                            gap="0.6em",
                        ),
                        width="100%",
                        padding_x=2,
                        spacing="2",
                    ),
                    width="100%",
                    margin_x="auto",
                    flex_direction="column",
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
                    gap="1em",
                    justify_content="center",
                    padding="1em",
                    margin="0 auto",
                ),
                background_color=BLUE_DARK,
                width="100%",
            )
        ),
        
        # Versión Mobile
        rx.mobile_only(
            rx.box(
                rx.vstack(
                    header("Envía tu partida", "Analiza tus partidas"),
                    rx.center(
                        rx.box(
                            chess_board(),
                            padding="0.5em",
                            bg=BLUE_DARK,
                        ),
                        width="100%",
                    ),
                    rx.center(
                        rx.box(
                            moves_table(),
                            padding="0.5em",
                            bg=BLUE_DARK,
                            max_width="95%",
                        ),
                        width="100%",
                    ),
                    rx.center(
                        rx.box(
                            send_pgn_form(),
                            padding="0.5em",
                            max_width="95%",
                        ),
                        width="100%",
                    ),
                    rx.vstack(
                        rx.foreach(
                            State.recommended_openings,
                            lambda opening: opening_recommendation(
                                type_recommendation=opening["type"],
                                style=opening["style"],
                                description=opening["description"],
                                opening=opening["name"]
                            )
                        ),
                        width="100%",
                        spacing="3",
                        padding="0.8em",
                    ),
                    width="100%",
                    padding_x="0.5em",
                    spacing="2",
                ),
                background_color=BLUE_DARK,
                width="100%",
            )
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