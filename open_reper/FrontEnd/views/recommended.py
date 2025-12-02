from open_reper.BackEnd.state import State
from open_reper.FrontEnd.components.chess_board import chess_board
from open_reper.FrontEnd.components.header import header
from open_reper.FrontEnd.components.moves_table_static import moves_table_static
from open_reper.FrontEnd.components.opening_description import opening_description, opening_plans
from open_reper.FrontEnd.components.opening_recommendation import opening_recommendation
from open_reper.FrontEnd.constants import (
    BLUE_DARK, FONT_FAMILY, ORANGE, ORANGE_HOVER, WHITE,
    FONT_XL, FONT_LG, FONT_MD,
    PADDING_SM, PADDING_MD, PADDING_LG,
    SPACING_MD, SPACING_LG,
    MAX_WIDTH_LG
)
import reflex as rx


def _opening_title_section():
    """Sección del título de la apertura - responsiva"""
    return rx.center(
        rx.vstack(
            rx.heading(
                "Apertura Recomendada",
                font_size=FONT_MD,  # [1em, 1.05em, 1.1em, 1.15em]
                color=WHITE,
                font_weight="600"
            ),
            rx.heading(
                State.recommended_opening['name'],
                font_size=FONT_XL,  # [1.4em, 1.6em, 1.8em, 2em]
                color=WHITE,
                margin_bottom=SPACING_MD,
                text_align="center",
                font_weight="700",
                line_height="1.2"
            ),
            spacing="2",
            width="100%",
            max_width=MAX_WIDTH_LG,
            padding_x=PADDING_MD,
            align_items="center"
        ),
        bg=BLUE_DARK,
        width="100%",
        padding_y=PADDING_LG
    )


def _board_and_moves_section():
    """Tablero y movimientos - layout responsivo"""
    return rx.center(
        rx.flex(
            rx.box(
                chess_board(),
                padding=PADDING_SM,
                bg=BLUE_DARK,
                margin_right=["0", "0", "0.7em", "0.7em"],
                width=["100%", "100%", "auto", "auto"]
            ),
            rx.box(
                moves_table_static(),
                width=["100%", "100%", "auto", "auto"]
            ),
            flex_direction=["column", "column", "row", "row"],
            gap=SPACING_MD,
            justify_content="center",
            align_items=["center", "center", "flex-start", "flex-start"],
            width="100%",
            max_width=MAX_WIDTH_LG,
            padding_x=PADDING_SM
        ),
        width="100%"
    )


def _recommendations_grid():
    """
    Grid de otras recomendaciones
    Móvil: columna vertical (1 card por fila)
    Desktop: grid de 2 columnas
    """
    return rx.center(
        rx.vstack(
            rx.heading(
                "Otras recomendaciones",
                font_size=FONT_LG,
                color=WHITE,
                font_weight="600"
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
                # Móvil: flex column, Desktop: grid 2 columnas
                display=["flex", "flex", "grid", "grid"],
                flex_direction=["column", "column", "row", "row"],
                grid_template_columns=["none", "none", "repeat(2, 1fr)", "repeat(2, 1fr)"],
                gap=["0.8em", "1em", "1.2em", "1.5em"],
                justify_content="center",
                width="100%",
                align_items=["stretch", "stretch", "flex-start", "flex-start"]
            ),
            spacing="4",
            width="100%",
            max_width=MAX_WIDTH_LG,
            padding=["0.8em", "1em", "1.2em", "1.5em"],
            align_items="center"
        ),
        width="100%"
    )

@rx.page(route="/opening-recommended")
def recommended_opening_view():

    return rx.flex(
        # Header
        header(
            "Recomendación de apertura",
            "Mejora tu juego con recomendaciones basadas en tu estilo"
        ),
        
        # Título de la apertura
        _opening_title_section(),

        # Tablero y movimientos
        _board_and_moves_section(),

        # Descripción y planes
        rx.center(
            rx.vstack(
                opening_description(State.recommended_opening['description']),
                opening_plans(State.recommended_opening['plans']),
                width="100%",
                max_width=MAX_WIDTH_LG,
                spacing="4",  # VStack spacing: valores literales '0'-'9'
                padding_x=PADDING_MD
            ),
            width="100%"
        ),

        # Grid de otras recomendaciones
        _recommendations_grid(),

        # Botón para analizar otra partida
        rx.center(
            rx.link(
                rx.button(
                    "Analizar Otra Partida",
                    bg=ORANGE,
                    color=WHITE,
                    _hover={
                        "bg": ORANGE_HOVER,
                        "transform": "translateY(-2px)"
                    },
                    font_family=FONT_FAMILY,
                    padding=PADDING_MD,
                    border_radius="8px",
                    font_size=["0.8em", "0.85em", "0.9em", "0.95em"],
                    font_weight="600",
                    cursor="pointer",
                    transition="all 0.3s ease",
                    min_width=["150px", "180px", "200px", "220px"]
                ),
                href="/send-game"
            ),
            width="100%",
            padding_y=PADDING_LG
        ),

        # Layout de página
        flex_direction="column",
        width="100%",
        min_height="100vh",
        bg=BLUE_DARK,
        font_family=FONT_FAMILY,
        overflow_y="auto",
        align_items="center"
    )