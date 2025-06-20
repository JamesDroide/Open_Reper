import reflex as rx
from open_reper.BackEnd.state import State

def chess_board():
    return rx.vstack(
        rx.heading(f"{State.white_player} vs {State.black_player}",
            font_size="1.5em",
            color="white",
            margin_bottom="1em"),
        rx.image(
            src=State.board_svg,
            width="100%",
            max_width="600px",
            height="auto",
            margin_bottom="1em",
        ),
        rx.hstack(
            rx.button(
                "← Anterior",
                on_click=State.prev_move,
                bg="#1E3A5F",
                color="white",
                disabled=State.current_move <= 0,
            ),
            rx.text(
                f"Movimiento {State.current_move + 1} de {State.game_moves.length()}",
                color="white",
                padding="0 1em"
            ),
            rx.button(
                "Siguiente →",
                on_click=State.next_move,
                bg="#1E3A5F",
                color="white",
                disabled=State.current_move >= State.game_moves.length() - 1,
            ),
            rx.button(
                "Reiniciar",
                on_click=State.reset_game,
                bg="#F24100",
                color="white",
                margin_left="1em"
            ),
            spacing="3",
            align="center"
        ),
        align_items="center",
    )