import reflex as rx
from open_reper.BackEnd.state import State
from open_reper.FrontEnd.constants import (
    BLUE_DARK, BLUE_DARK_HOVER, BLUE_HOVER, WHITE,
    FONT_MD, FONT_XS,
    PADDING_SM, SPACING_SM,
    RADIUS_MD, SHADOW_SM,
    TRANSITION_FAST, EASE_IN_OUT
)

def moves_table():

    return rx.vstack(
        # Título responsivo
        rx.heading(
            "Movimientos de la Partida",
            color=WHITE,
            font_size=FONT_MD,  # [1em, 1.05em, 1.1em, 1.15em]
            font_weight="600"
        ),
        # Tabla con scroll
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell("#"),
                    rx.table.column_header_cell("Blancas"),
                    rx.table.column_header_cell("Negras"),
                )
            ),
            rx.table.body(
                rx.foreach(
                    State.format_move_list,
                    lambda move: rx.table.row(
                        rx.table.cell(move[0]),
                        rx.table.cell(move[1]),
                        rx.table.cell(move[2]),
                    )
                )
            ),
            margin_top=SPACING_SM,
            bg=BLUE_HOVER,
            padding=PADDING_SM,
            border_radius=RADIUS_MD,
            box_shadow=SHADOW_SM,
            width="100%",
            height=["300px", "350px", "370px", "400px"],  # Altura responsiva
            overflow_y="auto",
            font_size=FONT_XS,  # [0.75em, 0.8em, 0.85em, 0.9em]
        ),
        # Controles de navegación responsivos
        rx.hstack(
            rx.button(
                "⏮️",
                on_click=State.reset_game_second_board,
                bg=BLUE_DARK,
                color=WHITE,
                _hover={
                    "bg": BLUE_DARK_HOVER,
                    "transform": "scale(1.1)"
                },
                title="Reiniciar reproducción",
                font_size=["1.1em", "1.2em", "1.3em", "1.4em"],  # Responsivo
                margin_right=SPACING_SM,
                padding=["0.4em 6px", "0.45em 7px", "0.5em 8px", "0.5em 8px"],
                border_radius=RADIUS_MD,
                cursor="pointer",
                transition=f"all {TRANSITION_FAST[1]} {EASE_IN_OUT}"
            ),
            rx.button(
                "◀️",
                on_click=State.prev_move_second_board,
                bg=BLUE_DARK,
                color=WHITE,
                _hover={
                    "bg": BLUE_DARK_HOVER,
                    "transform": "scale(1.1)"
                },
                is_disabled=State.interactive_current_move <= 0,
                title="Movimiento anterior",
                font_size=["1.1em", "1.2em", "1.3em", "1.4em"],
                margin_right=SPACING_SM,
                padding=["0.4em 6px", "0.45em 7px", "0.5em 8px", "0.5em 8px"],
                border_radius=RADIUS_MD,
                cursor="pointer",
                opacity=rx.cond(State.interactive_current_move <= 0, "0.5", "1"),
                transition=f"all {TRANSITION_FAST[1]} {EASE_IN_OUT}"
            ),
            rx.button(
                "▶️",
                on_click=State.next_move_second_board,
                bg=BLUE_DARK,
                color=WHITE,
                _hover={
                    "bg": BLUE_DARK_HOVER,
                    "transform": "scale(1.1)"
                },
                is_disabled=State.interactive_current_move >= State.format_move_list.length()-1,
                title="Siguiente movimiento",
                font_size=["1.1em", "1.2em", "1.3em", "1.4em"],
                margin_right=SPACING_SM,
                padding=["0.4em 6px", "0.45em 7px", "0.5em 8px", "0.5em 8px"],
                border_radius=RADIUS_MD,
                cursor="pointer",
                opacity=rx.cond(
                    State.interactive_current_move >= State.format_move_list.length()-1,
                    "0.5",
                    "1"
                ),
                transition=f"all {TRANSITION_FAST[1]} {EASE_IN_OUT}"
            ),
            rx.button(
                "⏩",
                on_click=State.go_to_last_move,
                bg=BLUE_DARK,
                color=WHITE,
                _hover={
                    "bg": BLUE_DARK_HOVER,
                    "transform": "scale(1.1)"
                },
                is_disabled=State.interactive_current_move >= State.format_move_list.length() - 1,
                title="Ir al final",
                font_size=["1.1em", "1.2em", "1.3em", "1.4em"],
                padding=["0.4em 6px", "0.45em 7px", "0.5em 8px", "0.5em 8px"],
                border_radius=RADIUS_MD,
                cursor="pointer",
                opacity=rx.cond(
                    State.interactive_current_move >= State.format_move_list.length() - 1,
                    "0.5",
                    "1"
                ),
                transition=f"all {TRANSITION_FAST[1]} {EASE_IN_OUT}"
            ),
            spacing="2",
            margin_top=SPACING_SM,
            justify_content="center",
            flex_wrap="wrap"  # Permite ajuste en pantallas pequeñas
        ),
        align_items="center",
        width="100%",
        spacing="3"  # VStack solo acepta valores literales '0'-'9'
    )