import reflex as rx
from open_reper.BackEnd.state import State
from open_reper.FrontEnd.constants import BLUE_DARK, BLUE_HOVER

def moves_table_static():
    return rx.box(
                rx.heading("Secuencia de Movimientos",
                        font_size="1.5em",
                        color="white",
                        margin_bottom="1em"),
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
                            State.move_pairs,
                            lambda i: rx.table.row(
                                rx.table.cell(f"{i+1}.", color="white"),
                                rx.table.cell(
                                    rx.cond(
                                        i*2 < State.game_moves.length(),
                                        State.game_moves[i*2],
                                        ""
                                    ),
                                    color="white"
                            ),
                                rx.table.cell(
                                    rx.cond(
                                        i*2+1 < State.game_moves.length(),
                                        State.game_moves[i*2+1],
                                        ""
                                    ),
                                    color="white"
                            )
                            )
                        )
                    ),
                    bg=BLUE_HOVER,
                    padding="1em",
                    border_radius="8px",
                    width="100%",
                    height="650px",
                    overflow_y="auto"
                ),
                padding="1em",
                bg=BLUE_DARK,
                margin_right="1em",
                min_width="350px"
            )