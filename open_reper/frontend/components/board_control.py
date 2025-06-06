import reflex as rx

def board_control_component(state):
    return rx.hstack(
        rx.button(
            "← Anterior",
            on_click=state.prev_move,
            bg="#1E3A5F",
            color="white",
            disabled=state.current_move <= 0,
        ),
        rx.text(
            f"Movimiento {state.current_move + 1} de {len(state.game_moves)}",
            color="white",
            padding="0 1em"
        ),
        rx.button(
            "Siguiente →",
            on_click=state.next_move,
            bg="#1E3A5F",
            color="white",
            disabled=state.current_move >= len(state.game_moves) - 1,
        ),
        rx.button(
            "Reiniciar",
            on_click=state.reset_game,
            bg="#F24100",
            color="white",
            margin_left="1em"
        ),
        spacing="3",
        margin_bottom="1em",
        align="center"
    )
