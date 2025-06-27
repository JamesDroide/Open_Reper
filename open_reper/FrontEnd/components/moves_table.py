import reflex as rx
from open_reper.BackEnd.state import State
from open_reper.FrontEnd.constants import BLUE_DARK, WHITE

def moves_table():
    return rx.vstack(
        rx.heading("Movimientos de la Partida", color="white", font_size="1.5em"),
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
            margin_top="1em",
            bg="#1E3A5F",
            padding="1em",
            border_radius="8px",
            width="100%",
            height="490px",
            overflow_y="auto",
        ),
        rx.hstack(
            rx.button(
                "⏮️",
                on_click=State.reset_game_second_board,
                bg=BLUE_DARK,
                color=WHITE,
                _hover={"bg": "#152942"},
                title="Reiniciar reproducción",
                font_size="2em",
                margin_right="0.5em",
                padding="1em 10px"
            ),
            rx.button(
                "◀️",
                on_click=State.prev_move_second_board,
                bg=BLUE_DARK,
                color=WHITE,
                _hover={"bg": "#152942"},
                is_disabled=State.interactive_current_move <= 0,
                title="Movimiento anterior",
                font_size="2em",
                margin_right="0.5em",
                padding="1em 10px"
            ),
            rx.button(
                "▶️",
                on_click=State.next_move_second_board,
                bg=BLUE_DARK,
                color=WHITE,
                _hover={"bg": "#152942"},
                is_disabled=State.interactive_current_move >= State.format_move_list.length()-1,
                title="Siguiente movimiento",
                font_size="2em",
                margin_right="0.5em",
                padding="1em 10px"
            ),
            rx.button(
                "⏩",
                on_click=State.go_to_last_move,
                bg=BLUE_DARK,
                color=WHITE,
                _hover={"bg": "#152942"},
                is_disabled=State.interactive_current_move >= State.format_move_list.length() - 1,
                title="Ir al final",
                font_size="2em",
                margin_right="0.5em",
                padding="1em 10px"
            ),
            spacing="2",
            margin_top="1em",
            justify_content="center"
        ),
        align_items="center",
        width="100%",
    )