"""
Vista de Envío de Partidas - 100% Responsiva - Plan 3
Refactorizada para eliminar duplicación y mejorar responsividad
"""

import reflex as rx

from open_reper.BackEnd.state import State
from open_reper.FrontEnd.components.header import header
from open_reper.FrontEnd.components.interactive_chess_board import chess_board
from open_reper.FrontEnd.components.opening_recommendation import opening_recommendation
from open_reper.FrontEnd.constants import (
    BLUE_DARK, FONT_FAMILY,
    PADDING_SM, PADDING_MD, SPACING_SM, SPACING_MD,
    MAX_WIDTH_LG, MAX_WIDTH_XL
)
from open_reper.FrontEnd.components.send_pgn_form import send_pgn_form
from open_reper.FrontEnd.components.moves_table import moves_table


def _main_content_section():
    """
    Sección principal con tablero, movimientos y formulario
    Desktop: 3 columnas (tablero | movimientos | formulario)
    Móvil: todo en columna vertical centrado
    """
    return rx.center(
        rx.flex(
            # Tablero de ajedrez
            rx.center(
                rx.box(
                    chess_board(),
                    padding=PADDING_SM,
                    bg=BLUE_DARK,
                    width=["100%", "100%", "auto", "auto"]
                ),
                width=["100%", "100%", "auto", "auto"]
            ),
            # Tabla de movimientos
            rx.center(
                rx.box(
                    moves_table(),
                    padding=PADDING_SM,
                    bg=BLUE_DARK,
                    min_width=["100%", "100%", "280px", "320px"],
                    width=["100%", "100%", "auto", "auto"]
                ),
                width=["100%", "100%", "auto", "auto"]
            ),
            # Formulario PGN - Centrado en móvil
            rx.center(
                rx.box(
                    send_pgn_form(),
                    width=["95%", "95%", "auto", "auto"],
                    max_width=["400px", "400px", "none", "none"]
                ),
                width=["100%", "100%", "auto", "auto"]
            ),
            # Layout: columna en móvil, fila en desktop
            flex_direction=["column", "column", "row", "row"],
            gap=["1em", "1.2em", "1.5em", "2em"],
            justify_content="center",
            align_items=["center", "center", "flex-start", "flex-start"],
            width="100%",
            max_width=MAX_WIDTH_XL,
            flex_wrap="nowrap"
        ),
        width="100%",
        padding_x=["0.5em", "0.8em", "1em", "1.5em"],
        padding_y=PADDING_MD
    )


def _recommendations_section():
    """
    Cards de recomendaciones
    Móvil: columna vertical (1 card por fila)
    Desktop: grid de 2 columnas
    """
    return rx.center(
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
            padding=["0.8em", "1em", "1.2em", "1.5em"],
            max_width=MAX_WIDTH_LG,
            width="100%",
            align_items=["stretch", "stretch", "flex-start", "flex-start"]
        ),
        width="100%"
    )


@rx.page(route="/send-game", on_load=State.on_load)
def send_game_view():

    return rx.flex(
        # Header responsivo
        header(
            "Envía tu partida",
            "Analiza tus partidas y descubre nuevas aperturas"
        ),

        # Sección principal (tablero + movimientos + formulario)
        _main_content_section(),

        # Grid de recomendaciones
        _recommendations_section(),

        # Layout de página
        flex_direction="column",
        width="100%",
        min_height="100vh",
        bg=BLUE_DARK,
        font_family=FONT_FAMILY,
        overflow_y="auto",
        align_items="center"
    )