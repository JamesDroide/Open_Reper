import reflex as rx
from open_reper.BackEnd.state import State
from open_reper.FrontEnd.constants import BLUE_DARK, BLUE_DARK_HOVER, BLUE_HOVER, WHITE

def moves_table():
    return rx.vstack(
        rx.heading("Movimientos de la Partida", color="white", font_size="1.1em"),
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
            margin_top="0.7em",
            bg=BLUE_HOVER,
            padding="0.7em",
            border_radius="8px",
            width="100%",
            height="370px",
            overflow_y="auto",
            font_size="0.85em",
        ),
        rx.hstack(
            rx.button(
                "⏮️",
                on_click=State.reset_game_second_board,
                bg=BLUE_DARK,
                color=WHITE,
                _hover={"bg": BLUE_DARK_HOVER},
                title="Reiniciar reproducción",
                font_size="1.3em",
                margin_right="0.3em",
                padding="0.5em 8px"
            ),
            rx.button(
                "◀️",
                on_click=State.prev_move_second_board,
                bg=BLUE_DARK,
                color=WHITE,
                _hover={"bg": BLUE_DARK_HOVER},
                is_disabled=State.interactive_current_move <= 0,
                title="Movimiento anterior",
                font_size="1.3em",
                margin_right="0.3em",
                padding="0.5em 8px"
            ),
            rx.button(
                "▶️",
                on_click=State.next_move_second_board,
                bg=BLUE_DARK,
                color=WHITE,
                _hover={"bg": BLUE_DARK_HOVER},
                is_disabled=State.interactive_current_move >= State.format_move_list.length()-1,
                title="Siguiente movimiento",
                font_size="1.3em",
                margin_right="0.3em",
                padding="0.5em 8px"
            ),
            rx.button(
                "⏩",
                on_click=State.go_to_last_move,
                bg=BLUE_DARK,
                color=WHITE,
                _hover={"bg": BLUE_DARK_HOVER},
                is_disabled=State.interactive_current_move >= State.format_move_list.length() - 1,
                title="Ir al final",
                font_size="1.3em",
                margin_right="0.3em",
                padding="0.5em 8px"
            ),
            spacing="2",
            margin_top="0.7em",
            justify_content="center"
        ),
        align_items="center",
        width="100%",
    )