import reflex as rx
from open_reper.BackEnd.state import State
from open_reper.FrontEnd.constants import (
    BLUE_HOVER, ORANGE, ORANGE_HOVER, WHITE,
    WIDTH_BOARD, FONT_MD, FONT_SM, FONT_XS,
    SPACING_SM, SPACING_XS, PADDING_SM, PADDING_XS,
    RADIUS_MD, SHADOW_SM, SHADOW_MD,
    TRANSITION_FAST, TRANSITION_NORMAL, EASE_IN_OUT
)

def chess_board():

    return rx.vstack(
        # Título con jugadores
        rx.heading(
            f"{State.white_player} vs {State.black_player}",
            font_size=FONT_MD,  # [1em, 1.05em, 1.1em, 1.15em]
            color=WHITE,
            margin_bottom=SPACING_SM,
            text_align="center",
            font_weight="600",
            line_height="1.3"
        ),
        # Imagen del tablero con lazy loading
        rx.image(
            src=State.board_svg,
            width="100%",
            max_width=WIDTH_BOARD,  # [95%, 380px, 450px, 520px]
            height="auto",
            margin_bottom=SPACING_SM,
            alt="Tablero de ajedrez",
            loading="lazy",  # Lazy loading para performance
            border_radius=RADIUS_MD,
            box_shadow=SHADOW_MD
        ),
        # Controles de navegación responsivos
        rx.hstack(
            # Botón Anterior
            rx.button(
                "← Anterior",
                on_click=State.prev_move,
                bg=BLUE_HOVER,
                color=WHITE,
                disabled=State.current_move <= 0,
                cursor=rx.cond(State.current_move <= 0, "not-allowed", "pointer"),
                font_size=FONT_XS,  # [0.75em, 0.8em, 0.85em, 0.9em]
                padding=PADDING_XS,  # [0.3em, 0.4em, 0.5em, 0.6em]
                border_radius=RADIUS_MD,
                opacity=rx.cond(State.current_move <= 0, "0.5", "1"),
                _hover={
                    "bg": rx.cond(State.current_move > 0, "#152942", BLUE_HOVER),
                    "transform": rx.cond(State.current_move > 0, "translateY(-1px)", "none")
                },
                transition=f"all {TRANSITION_FAST[1]} {EASE_IN_OUT}",
                min_width=["70px", "80px", "90px", "100px"]
            ),
            # Contador de movimientos (oculto en móviles muy pequeños)
            rx.text(
                f"Movimiento {State.current_move + 1} de {State.game_moves.length()}",
                color=WHITE,
                padding=SPACING_XS,
                font_size=FONT_XS,
                display=["none", "block", "block", "block"],  # Oculto en móvil pequeño
                white_space="nowrap"
            ),
            # Botón Siguiente
            rx.button(
                "Siguiente →",
                on_click=State.next_move,
                bg=BLUE_HOVER,
                color=WHITE,
                disabled=State.current_move >= State.game_moves.length() - 1,
                cursor=rx.cond(State.current_move >= State.game_moves.length() - 1, "not-allowed", "pointer"),
                font_size=FONT_XS,
                padding=PADDING_XS,
                border_radius=RADIUS_MD,
                opacity=rx.cond(State.current_move >= State.game_moves.length() - 1, "0.5", "1"),
                _hover={
                    "bg": rx.cond(State.current_move < State.game_moves.length() - 1, "#152942", BLUE_HOVER),
                    "transform": rx.cond(State.current_move < State.game_moves.length() - 1, "translateY(-1px)", "none")
                },
                transition=f"all {TRANSITION_FAST[1]} {EASE_IN_OUT}",
                min_width=["70px", "80px", "90px", "100px"]
            ),
            # Botón Reiniciar
            rx.button(
                "Reiniciar",
                on_click=State.reset_game,
                bg=ORANGE,
                color=WHITE,
                margin_left=["0.3em", "0.5em", "0.7em", "0.9em"],
                cursor="pointer",
                _hover={
                    "bg": ORANGE_HOVER,
                    "transform": "translateY(-1px)",
                    "box_shadow": SHADOW_SM
                },
                font_size=FONT_XS,
                padding=PADDING_XS,
                border_radius=RADIUS_MD,
                transition=f"all {TRANSITION_FAST[1]} {EASE_IN_OUT}",
                min_width=["70px", "80px", "90px", "100px"]
            ),
            spacing="2",
            align="center",
            justify="center",
            flex_wrap="wrap",  # Permite que se ajusten en móviles muy pequeños
            width="100%"
        ),
        align_items="center",
        width="100%",
        spacing="3"  # VStack spacing: valores literales '0'-'9'
    )