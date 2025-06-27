# frontend/views/recommended.py
from open_reper.BackEnd.state import State
from open_reper.FrontEnd.constants import BLUE_DARK, FONT_FAMILY
import reflex as rx

@rx.page(route="/opening-recommended")
def recommended_opening_view():
    return rx.box(
        rx.box(
            rx.flex(
                rx.flex(
                    rx.link(
                        rx.image(
                            src="/logo_open_reper.png",
                            width="200px",
                            height="auto",
                        ),
                        href="/",
                        _hover={"cursor: pointer"},
                    ),
                    rx.vstack(
                        rx.heading("Recomendación de apertura", font_size="2em", color="white"),
                        rx.text("Mejora tu juego con recomendaciones basadas en tu estilo", color="#d1e0e0"),
                        spacing="1",
                        align_items="center",
                        flex_grow=1
                    ),
                    justify_content="space-between",
                    align_items="center",
                    width="100%",
                    padding="1em",
                    bg=BLUE_DARK
                ),
                rx.flex(
                    rx.vstack(
                        rx.heading("Apertura Recomendada",
                                font_size="2em",
                                color="white"),
                        rx.heading(
                            State.recommended_opening['name'],
                            font_size="3.5em",
                            color="white",
                            margin_bottom="1em"
                        ),
                        spacing="5",
                        width="100%",
                        max_width="1200px",
                        padding_x="2em",
                        align_items="center"
                    ),
                    bg=BLUE_DARK,
                    width="100%",
                    padding_y="2em"
                ),
                rx.flex(
                    rx.box(
                        rx.vstack(
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
                        ),
                        padding="1em",
                        bg="#2a5c9a",
                        border_radius="8px",
                        box_shadow="0 4px 8px rgba(0, 0, 0, 0.2)",
                        margin_right="1em"
                    ),
                    rx.box(
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
                            bg="#1E3A5F",
                            padding="1em",
                            border_radius="8px",
                            width="100%",
                            height="650px",
                            overflow_y="auto"
                        ),
                        padding="1em",
                        bg="#2a5c9a",
                        border_radius="8px",
                        box_shadow="0 4px 8px rgba(0, 0, 0, 0.2)",
                        margin_right="1em",
                        min_width="350px"
                    ),
                    width="100%",
                    max_width="1200px",
                    margin_x="auto",
                    padding_x=4,
                    justify_content="space-between",
                ),
                rx.box(
                    rx.heading("Sobre esta Apertura",
                                font_size="1.5em",
                                color="white"),
                    rx.text(
                        State.recommended_opening['description'],
                        color="white",
                        line_height="2"
                    ),
                    padding="0.5em",
                    bg="#2a5c9a",
                    border_radius="8px",
                    margin_top="2em"
                ),
                rx.box(
                    rx.heading("Planes Estratégicos",
                                font_size="1.3em",
                                color="white"),
                    rx.unordered_list(
                        rx.foreach(
                            State.recommended_opening["plans"],
                            lambda plan: rx.list_item(
                                plan,
                                color="white",
                                margin_bottom="0.5em"
                            )
                        ),
                        padding_left="1.5em"
                    ),
                    padding="0.5em",
                    bg="#2a5c9a",
                    border_radius="8px"
                ),
                width="100%",
                max_width="1200px",
                margin_x="auto",
                flex_direction="column",
            ),
            background_color=BLUE_DARK,
            width="100%"
        ),
        rx.center(
            rx.button(
                "Analizar Otra Partida",
                bg="#F24100",
                color="white",
                padding="1em 4em",
                on_click=lambda: rx.redirect("/send-game"),
                border_radius="8px",
                _hover={"bg": "#e03d00"}
            ),
            bg="#2A5C9A",
            width="100%",
            padding_y="2em"
        ),
        style={
            "position": "fixed",
            "top": 0,
            "left": 0,
            "right": 0,
            "bottom": 0,
            "overflow": "auto",
            "background": BLUE_DARK,
            "font-family": FONT_FAMILY
        }
    )