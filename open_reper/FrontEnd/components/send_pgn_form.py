import reflex as rx
from open_reper.BackEnd.state import State
from open_reper.FrontEnd.constants import (
    GREEN, GREEN_HOVER, ORANGE, ORANGE_HOVER, WHITE, FONT_FAMILY,
    WIDTH_FORM, SIZE_PAWN, FONT_MD, FONT_SM, FONT_XS,
    PADDING_SM, PADDING_MD, SPACING_SM, SPACING_MD,
    RADIUS_MD, RADIUS_LG, SHADOW_MD, SHADOW_PRIMARY,
    TRANSITION_NORMAL, TRANSITION_FAST, EASE_IN_OUT,
    HEIGHT_TEXTAREA, COLOR_ERROR
)

def send_pgn_form():

    return rx.form(
        # Título responsivo
        rx.center(
            rx.heading(
                "Envía tu partida PGN",
                font_size=FONT_MD,  # [1em, 1.05em, 1.1em, 1.15em]
                color=WHITE,
                font_weight="600"
            ),
            width="100%",
            margin_bottom=SPACING_SM,
            margin_top=SPACING_SM,
        ),
        # Textarea responsivo mejorado
        rx.text_area(
            placeholder="Pega tu PGN aquí...",
            value=State.pgn_text,
            on_change=State.set_pgn_text,
            width=WIDTH_FORM,  # [95%, 350px, 400px, 450px]
            height=HEIGHT_TEXTAREA,  # [120px, 140px, 160px, 180px]
            border_radius=RADIUS_MD,
            border="2px solid #808080",
            padding=PADDING_SM,
            color="black",
            bg="white",
            font_size=FONT_SM,
            font_family='"Courier New", monospace',  # Monospace para PGN
            resize="vertical",
            _focus={
                "border_color": GREEN,
                "box_shadow": f"0 0 0 3px rgba(76, 175, 80, 0.1)",
                "outline": "none"
            },
            transition=f"all {TRANSITION_FAST[1]} {EASE_IN_OUT}",
        ),
        # Botón Cargar PGN responsivo
        rx.button(
                "Cargar PGN al Tablero",
                on_click=State.load_pgn_to_board,
                bg=GREEN,
                color="white",
                _hover={
                    "bg": GREEN_HOVER,
                    "transform": "translateY(-2px)",
                    "box_shadow": SHADOW_MD
                },
                margin_top=SPACING_SM,
                font_family=FONT_FAMILY,
                align_self="center",
                padding=PADDING_SM,
                border_radius=RADIUS_MD,
                box_shadow=SHADOW_MD,
                width=WIDTH_FORM,  # Se adapta al contenedor
                max_width=["100%", "380px", "420px", "450px"],
                font_size=FONT_SM,
                font_weight="600",
                cursor="pointer",
                transition=f"all {TRANSITION_NORMAL[1]} {EASE_IN_OUT}",
                _active={"transform": "translateY(0)"}
        ),
        # Mensaje de error de carga
        rx.cond(
            State.error_load_game,
            rx.text(
                State.error_load_game,
                color=COLOR_ERROR,
                font_weight="bold",
                margin_top=SPACING_SM,
                font_size=FONT_XS,
                text_align="center"
            ),
        ),
        # Título selector de color
        rx.heading(
            "Selecciona tu color:",
            font_size=FONT_SM,
            color=WHITE,
            margin_top=SPACING_MD,
            font_weight="600"
        ),
        # Selector de peones interactivo
        rx.hstack(
            # Peón blanco
            rx.box(
                rx.image(
                    src="/white-pawn.webp",
                    width=SIZE_PAWN,  # [36px, 42px, 48px, 54px]
                    height=SIZE_PAWN,
                    alt="Seleccionar blancas",
                    loading="lazy"  # Lazy loading para performance
                ),
                border=rx.cond(
                    State.selected_color == "white",
                    f"3px solid {ORANGE}",
                    "3px solid transparent"
                ),
                border_radius=RADIUS_MD,
                on_click=lambda: State.set_selected_color("white"),
                cursor="pointer",
                padding="4px",
                bg=rx.cond(
                    State.selected_color == "white",
                    "rgba(242, 65, 0, 0.1)",
                    "transparent"
                ),
                transition=f"all {TRANSITION_FAST[1]} {EASE_IN_OUT}",
                _hover={
                    "transform": "scale(1.1) rotate(-5deg)",
                    "box_shadow": f"0 0 15px {ORANGE}"
                },
                _active={"transform": "scale(0.95)"}
            ),
            # Peón negro
            rx.box(
                rx.image(
                    src="/black-pawn.webp",
                    width=SIZE_PAWN,
                    height=SIZE_PAWN,
                    alt="Seleccionar negras",
                    loading="lazy"
                ),
                border=rx.cond(
                    State.selected_color == "black",
                    f"3px solid {ORANGE}",
                    "3px solid transparent"
                ),
                border_radius=RADIUS_MD,
                on_click=lambda: State.set_selected_color("black"),
                cursor="pointer",
                padding="4px",
                bg=rx.cond(
                    State.selected_color == "black",
                    "rgba(242, 65, 0, 0.1)",
                    "transparent"
                ),
                transition=f"all {TRANSITION_FAST[1]} {EASE_IN_OUT}",
                _hover={
                    "transform": "scale(1.1) rotate(-5deg)",
                    "box_shadow": f"0 0 15px {ORANGE}"
                },
                _active={"transform": "scale(0.95)"}
            ),
            spacing="4",
            margin_top=SPACING_SM,
            margin_bottom=SPACING_SM,
            justify_content="center"
        ),
        # Badge de color seleccionado
        rx.center(
            rx.cond(
                State.selected_color == "white",
                rx.badge(
                    "Blancas seleccionadas",
                    color_scheme="orange",
                    font_size=FONT_XS,
                    padding="4px 12px"
                ),
                rx.badge(
                    "Negras seleccionadas",
                    color_scheme="orange",
                    font_size=FONT_XS,
                    padding="4px 12px"
                )
            ),
            width="100%"
        ),
        # Botón principal de recomendación
        rx.button(
            "Obtener Recomendación",
            on_click=State.get_recommendation,
            color=WHITE,
            margin_top=SPACING_MD,
            is_loading=State.is_loading,
            _hover={
                "bg": ORANGE_HOVER,
                "transform": "translateY(-2px)",
                "box_shadow": SHADOW_MD
            },
            font_family=FONT_FAMILY,
            align_self="center",
            padding=PADDING_MD,
            bg=ORANGE,
            border_radius=RADIUS_MD,
            box_shadow=SHADOW_MD,
            width=WIDTH_FORM,
            max_width=["100%", "380px", "420px", "450px"],
            font_size=FONT_SM,
            font_weight="700",
            cursor="pointer",
            transition=f"all {TRANSITION_NORMAL[1]} {EASE_IN_OUT}",
            _active={"transform": "translateY(0)"}
        ),
        # Mensaje de error general
        rx.cond(
            State.error,
            rx.text(
                State.error,
                color=COLOR_ERROR,
                font_weight="bold",
                margin_top=SPACING_SM,
                font_size=FONT_XS,
                text_align="center"
            ),
        ),
        spacing="2",
        align="center",
        width="100%",
        max_width=["100%", "450px", "500px", "550px"]
    )