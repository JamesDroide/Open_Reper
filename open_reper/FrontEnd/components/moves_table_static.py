import reflex as rx
from open_reper.BackEnd.state import State
from open_reper.FrontEnd.constants import (
    BLUE_DARK, BLUE_HOVER, WHITE,
    FONT_MD, FONT_XS,
    PADDING_SM, SPACING_SM,
    RADIUS_MD, SHADOW_SM
)

def moves_table_static():

    return rx.box(
                rx.heading(
                    "Secuencia de Movimientos",
                    font_size=FONT_MD,  # [1em, 1.05em, 1.1em, 1.15em]
                    color=WHITE,
                    margin_bottom=SPACING_SM,
                    font_weight="600"
                ),
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
                                rx.table.cell(f"{i+1}.", color=WHITE),
                                rx.table.cell(
                                    rx.cond(
                                        i*2 < State.game_moves.length(),
                                        State.game_moves[i*2],
                                        ""
                                    ),
                                    color=WHITE
                            ),
                                rx.table.cell(
                                    rx.cond(
                                        i*2+1 < State.game_moves.length(),
                                        State.game_moves[i*2+1],
                                        ""
                                    ),
                                    color=WHITE
                            )
                            )
                        )
                    ),
                    bg=BLUE_HOVER,
                    padding=PADDING_SM,
                    border_radius=RADIUS_MD,
                    box_shadow=SHADOW_SM,
                    width="100%",
                    height=["350px", "400px", "450px", "480px"],  # Altura responsiva
                    overflow_y="auto",
                    font_size=FONT_XS  # [0.75em, 0.8em, 0.85em, 0.9em]
                ),
                padding=PADDING_SM,
                bg=BLUE_DARK,
                margin_right="0.7em",
                min_width="280px"
            )