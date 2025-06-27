import reflex as rx
from open_reper.BackEnd.state import State
from open_reper.FrontEnd.components.chess_square import chess_square
from open_reper.FrontEnd.constants import GREEN, GREEN_HOVER, ORANGE_HOVER
from open_reper.variables import ORANGE

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
                bg=ORANGE,
                color="white",
                _hover={"bg": ORANGE_HOVER}
            ),
            rx.button(
                "Cargar PGN al Tablero",
                on_click=State.load_pgn_to_board,
                bg=GREEN,
                color="white",
                _hover={"bg": GREEN_HOVER},
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