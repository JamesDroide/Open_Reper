# frontend/views/send_game.py
import reflex as rx

from open_reper.BackEnd.state import State
from open_reper.FrontEnd.components.opening_recommendation import opening_recommendation
from open_reper.FrontEnd.constants import BLUE_DARK, FONT_FAMILY
from open_reper.FrontEnd.components.send_pgn_form import send_pgn_form
from open_reper.FrontEnd.components.chess_board import chess_board
from open_reper.FrontEnd.components.moves_table import moves_table
from open_reper.FrontEnd.components.game_pieces import PIECE_MAP

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

def chess_square(square: str):
    """Componente para una casilla del tablero con imágenes"""
    is_selected = State.selected_square == square
    is_legal_move = State.legal_moves.contains(square)

    is_light = (ord(square[0]) - ord('a') + int(square[1])) % 2 == 1
    base_bg_color = "#f0d9b5" if is_light else "#b58863"

    bg_color = rx.cond(
        is_selected,
        "#bbcb2b",
        rx.cond(is_legal_move, "#86a666", base_bg_color)
    )

    piece_symbol = rx.cond(
        State.position.contains(square),
        State.position[square],
        ""
    )

    piece_component = rx.match(
        piece_symbol,
        *[(symbol, component) for symbol, component in PIECE_MAP.items()],
        rx.box(width="50px", height="50px")
    )

    return rx.box(
        piece_component,
        on_click=lambda: State.select_square(square),
        width="60px",
        height="60px",
        display="flex",
        justify_content="center",
        align_items="center",
        bg=bg_color,
        border="1px solid #444",
        _hover={"cursor": "pointer", "filter": "brightness(1.2)"}
    )

def chess_board():
    """Componente completo del tablero de ajedrez"""
    return rx.vstack(
        rx.heading("Tablero de Ajedrez Interactivo", color="white", font_size="1.5em"),
        rx.box(
            rx.flex(
                *[chess_square(f"{file}{rank}") for rank in range(8, 0, -1) for file in "abcdefgh"],
                wrap="wrap",
                width="480px",
                height="480px",
            ),
            border="4px solid #333",
            box_shadow="0 10px 25px rgba(0, 0, 0, 0.5)",
            overflow="hidden",
        ),
        rx.hstack(
            rx.button(
                "Reiniciar Tablero",
                on_click=State.reset_board,
                bg="#FF5722",
                color="white",
                _hover={"bg": "#E64A19"}
            ),
            rx.button(
                "Cargar PGN al Tablero",
                on_click=State.load_pgn_to_board,
                bg="#4CAF50",
                color="white",
                _hover={"bg": "#388E3C"},
                margin_left="1em"
            ),
            rx.text(
                rx.cond(
                    State.turn == "white",
                    "Turno: Blancas",
                    "Turno: Negras"
                ),
                color="white",
                font_weight="bold",
                margin_left="1em"
            ),
            spacing="4",
            margin_top="1em"
        ),
        align="center",
    )

