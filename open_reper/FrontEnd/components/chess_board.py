import reflex as rx
from open_reper.BackEnd.state import State
from open_reper.FrontEnd.constants import BLUE_HOVER, ORANGE, ORANGE_HOVER

def chess_board():
    return rx.vstack(
        rx.heading(f"{State.white_player} vs {State.black_player}",
            font_size="1.1em",
            color="white",
            margin_bottom="0.7em"),
        rx.image(
            src=State.board_svg,
            width="100%",
            max_width="450px",
            height="auto",
            margin_bottom="0.7em",
        ),
        rx.hstack(
            rx.button(
                "← Anterior",
                on_click=State.prev_move,
                bg=BLUE_HOVER,
                color="white",
                disabled=State.current_move <= 0,
                cursor="pointer",
                font_size="0.85em",
                padding="0.5em 0.8em"
            ),
            rx.text(
                f"Movimiento {State.current_move + 1} de {State.game_moves.length()}",
                color="white",
                padding="0 0.7em",
                font_size="0.85em"
            ),
            rx.button(
                "Siguiente →",
                on_click=State.next_move,
                bg=BLUE_HOVER,
                color="white",
                disabled=State.current_move >= State.game_moves.length() - 1,
                cursor="pointer",
                font_size="0.85em",
                padding="0.5em 0.8em"
            ),
            rx.button(
                "Reiniciar",
                on_click=State.reset_game,
                bg=ORANGE,
                color="white",
                margin_left="0.7em",
                cursor="pointer",
                _hover={"bg": ORANGE_HOVER},
                font_size="0.85em",
                padding="0.5em 0.8em"
            ),
            spacing="2",
            align="center"
        ),
        align_items="center",
    )