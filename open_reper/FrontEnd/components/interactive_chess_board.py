import reflex as rx
from open_reper.BackEnd.state import State
from open_reper.FrontEnd.components.chess_square import chess_square
from open_reper.FrontEnd.constants import ORANGE_HOVER
from open_reper.variables import ORANGE

def chess_board():
    """Componente completo del tablero de ajedrez"""
    return rx.vstack(
        rx.heading("Tablero de Ajedrez Interactivo", color="white", font_size="1.1em"),
        rx.box(
            rx.flex(
                *[chess_square(f"{file}{rank}") for rank in range(8, 0, -1) for file in "abcdefgh"],
                wrap="wrap",
                width="360px",
                height="360px",
            ),
            border="3px solid #333",
            box_shadow="0 8px 20px rgba(0, 0, 0, 0.5)",
            overflow="hidden",
        ),
        rx.hstack(
            rx.button(
                "Reiniciar Tablero",
                on_click=State.reset_board,
                bg=ORANGE,
                color="white",
                _hover={"bg": ORANGE_HOVER},
                font_size="0.85em",
                padding="0.5em 1em"
            ),
            rx.text(
                rx.cond(
                    State.turn == "white",
                    "Turno: Blancas",
                    "Turno: Negras"
                ),
                color="white",
                font_weight="bold",
                margin_left="0.7em",
                font_size="0.9em"
            ),
            spacing="3",
            margin_top="0.7em",
            align_items="center",
            justify_content="center",
        ),
        align="center",
    )