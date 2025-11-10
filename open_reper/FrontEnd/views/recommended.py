from open_reper.BackEnd.state import State
from open_reper.FrontEnd.components.chess_board import chess_board
from open_reper.FrontEnd.components.header import header
from open_reper.FrontEnd.components.moves_table_static import moves_table_static
from open_reper.FrontEnd.components.opening_description import opening_description, opening_plans
from open_reper.FrontEnd.components.opening_recommendation import opening_recommendation
from open_reper.FrontEnd.constants import BLUE_DARK, FONT_FAMILY, ORANGE, ORANGE_HOVER
import reflex as rx

@rx.page(route="/opening-recommended")
def recommended_opening_view():
    return rx.box(
        rx.box(
            rx.flex(
                header("Recomendación de apertura", "Mejora tu juego con recomendaciones basadas en tu estilo"),
                rx.flex(
                    rx.vstack(
                        rx.heading("Apertura Recomendada",
                                font_size="1.4em",
                                color="white"),
                        rx.heading(
                            State.recommended_opening['name'],
                            font_size="2.2em",
                            color="white",
                            margin_bottom="0.7em"
                        ),
                        spacing="3",
                        width="100%",
                        max_width="1000px",
                        padding_x="1.5em",
                        align_items="center"
                    ),
                    bg=BLUE_DARK,
                    width="100%",
                    padding_y="1.5em"
                ),
                rx.flex(
                    rx.box(
                        chess_board(),
                        padding="0.7em",
                        bg="#2a5c9a",
                        margin_right="0.7em"
                    ),
                    moves_table_static(),
                    width="100%",
                    max_width="1000px",
                    margin_x="auto",
                    padding_x=3,
                    justify_content="space-between",
                ),
                opening_description(State.recommended_opening['description']),
                opening_plans(State.recommended_opening['plans']),
                width="100%",
                max_width="1000px",
                margin_x="auto",
                flex_direction="column",
            ),
            background_color=BLUE_DARK,
            width="100%"
        ),
        rx.flex(
            rx.heading("Otras recomendaciones",
                        font_size="1.2em",
                        color="white"),
            justify_content="center",
            margin_y="1.5em",
        ),
        rx.flex(
            rx.foreach(
                State.recommended_openings,
                lambda opening: opening_recommendation(
                    type_recommendation=opening["type"],
                    style=opening["style"],
                    description=opening["description"],
                    opening=opening["name"]
                )
            ),
            display="grid",
            grid_template_columns="repeat(2, 1fr)",
            gap="1.5em",
            justify_content="center",
            padding="1.5em",
            max_width="1000px",
            margin="0 auto",
        ),
        rx.center(
            rx.button(
                "Analizar Otra Partida",
                bg=ORANGE,
                color="white",
                padding="0.7em 2.5em",
                on_click=lambda: rx.redirect("/send-game"),
                border_radius="8px",
                _hover={"bg": ORANGE_HOVER},
                cursor="pointer",
                font_size="0.9em"
            ),
            bg="#2A5C9A",
            width="100%",
            padding_y="1.5em"
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