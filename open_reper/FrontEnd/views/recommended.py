# frontend/views/recommended.py
from open_reper.BackEnd.state import State
import reflex as rx

@rx.page(route="/opening-recommended")
def recommended_opening_view():
    return rx.center(
        rx.vstack(
            rx.heading("Apertura Recomendada", font_size="2em", color="white"),
            rx.heading(
                State.recommended_opening['name'],
                font_size="3em",
                color="white",
                margin_bottom="1em"
            ),

            # Sección del tablero y controles
            rx.vstack(
                rx.image(
                    src=State.board_svg,
                    width=["300px", "400px"],
                    height=["300px", "400px"],
                    alt="Tablero de Ajedrez",
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
                    margin_bottom="1em",
                    align="center"
                ),
                align_items="center",
            ),

            # Visualización de la secuencia de movimientos
            rx.box(
                rx.heading("Secuencia de Movimientos", font_size="1.5em", color="white", margin_bottom="0.5em"),
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("#", width="50px"),
                            rx.table.column_header_cell("Blancas", width="150px"),
                            rx.table.column_header_cell("Negras", width="150px"),
                        )
                    ),
                    rx.table.body(
                        rx.foreach(
                            State.move_pairs,
                            lambda i: rx.table.row(
                                rx.table.cell(f"{i + 1}.", color="white"),
                                rx.table.cell(
                                    rx.cond(
                                        i * 2 < State.game_moves.length(),
                                        State.game_moves[i * 2],
                                        ""
                                    ),
                                    color="white"
                                ),
                                rx.table.cell(
                                    rx.cond(
                                        i * 2 + 1 < State.game_moves.length(),
                                        State.game_moves[i * 2 + 1],
                                        ""
                                    ),
                                    color="white"
                                )
                            )
                        )
                    ),
                    bg="#1E3A5F",
                    padding="1em",
                    border_radius="8px",
                    width="100%"
                ),
                width="100%",
                max_width="600px",
                margin_bottom="2em"
            ),

            # Información de la apertura
            rx.box(
                rx.heading("Sobre esta Apertura", font_size="1.5em", color="white", margin_bottom="0.5em"),
                rx.text(
                    State.recommended_opening['description'],
                    color="white",
                    font_size="1.1em",
                    line_height="1.6",
                    margin_bottom="1em"
                ),
                rx.heading("Planes Estratégicos", font_size="1.3em", color="white", margin_bottom="0.5em"),
                rx.unordered_list(
                    rx.foreach(
                        State.recommended_opening["plans"],
                        lambda plan: rx.list_item(
                            plan,
                            color="white",
                            margin_bottom="0.5em",
                            font_size="1.1em"
                        )
                    ),
                    padding_left="1.5em"
                ),
                width="100%",
                max_width="800px"
            ),

            # Botones de acción
            rx.vstack(
                rx.button(
                    "Analizar Otra Partida",
                    bg="#F24100",
                    color="white",
                    padding="1em 2em",
                    on_click=lambda: rx.redirect("/send-game"),
                    margin_bottom="1em"
                ),

                align_items="center"
            ),

            spacing="4",
            align_items="center",
            width="100%",
            padding="1em"
        ),
        height="auto",
        background_color="#2A5C9A",
        padding="2em"
    )