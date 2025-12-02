import reflex as rx
from open_reper.BackEnd.state import State
from open_reper.FrontEnd.constants import (
    BLUE_HOVER, GREEN, GREEN_HOVER, WHITE,
    FONT_SM, FONT_XS, FONT_XXS,
    PADDING_XS, PADDING_MD, SPACING_SM, SPACING_XS,
    RADIUS_MD, SHADOW_MD,
    TRANSITION_NORMAL, EASE_IN_OUT
)

def opening_recommendation(type_recommendation: str, style: str, description: str, opening: str):

    return rx.cond(
        State.recommendation,
        rx.box(
            rx.vstack(
                # Título de la recomendación
                rx.heading(
                    f"Recomendación de Apertura - {type_recommendation}",
                    font_size=FONT_SM,  # [0.85em, 0.9em, 0.95em, 1em]
                    color=WHITE,
                    font_weight="600",
                    text_align="center"
                ),
                # Contenido principal - layout responsivo
                rx.flex(
                    # Columna izquierda: Estilo y descripción
                    rx.vstack(
                        rx.text(
                            "Estilo detectado:",
                            font_weight="bold",
                            color=WHITE,
                            font_size=FONT_XS  # [0.75em, 0.8em, 0.85em, 0.9em]
                        ),
                        rx.text(
                            style,
                            color=WHITE,
                            font_size=FONT_XXS  # [0.65em, 0.7em, 0.75em, 0.8em]
                        ),
                        rx.text(
                            "Descripción:",
                            font_weight="bold",
                            color=WHITE,
                            margin_top=SPACING_XS,
                            font_size=FONT_XS
                        ),
                        rx.text(
                            description,
                            color=WHITE,
                            font_size=FONT_XXS,
                            text_align="justify"
                        ),
                        align_items="flex-start",
                        spacing="2",
                        padding=PADDING_XS,
                        width=["100%", "100%", "60%", "60%"]  # Responsivo
                    ),
                    # Columna derecha: Apertura y botón
                    rx.vstack(
                        rx.text(
                            "Apertura recomendada:",
                            font_weight="bold",
                            color=WHITE,
                            font_size=FONT_XS
                        ),
                        rx.text(
                            opening,
                            color=WHITE,
                            font_size=FONT_XXS,
                            text_align="center"
                        ),
                        rx.link(
                            rx.button(
                                "Ver detalles",
                                bg=GREEN,
                                color=WHITE,
                                border_radius=RADIUS_MD,
                                font_size=FONT_XXS,
                                padding=PADDING_XS,
                                _hover={
                                    "bg": GREEN_HOVER,
                                    "transform": "translateY(-2px)"
                                },
                                on_click=lambda: State.set_recommend_opening(
                                    type_recommendation,
                                    opening,
                                    style
                                ),
                                cursor="pointer",
                                transition=f"all {TRANSITION_NORMAL[1]} {EASE_IN_OUT}",
                                width="100%"
                            ),
                            href="/opening-recommended",
                            margin_top=SPACING_SM,
                            width="100%"
                        ),
                        align_items="flex-start",
                        spacing="2",
                        padding=PADDING_XS,
                        width=["100%", "100%", "40%", "40%"]  # Responsivo
                    ),
                    # Layout: columna en móvil, fila en desktop
                    flex_direction=["column", "column", "row", "row"],
                    gap=SPACING_SM,
                    justify_content="space-between",
                    width="100%"
                ),
                bg=BLUE_HOVER,
                padding=PADDING_MD,  # [0.7em, 0.9em, 1em, 1.2em]
                border_radius=RADIUS_MD,
                box_shadow=SHADOW_MD,
                width="100%",
                spacing="3",  # VStack spacing: valores literales '0'-'9'
                _hover={
                    "box_shadow": "0 6px 12px rgba(0, 0, 0, 0.25)",
                    "transform": "translateY(-2px)"
                },
                transition=f"all {TRANSITION_NORMAL[1]} {EASE_IN_OUT}"
            ),
            margin_y=SPACING_SM,
            width="100%",
            min_width=["0", "280px", "300px", "320px"]  # Ancho mínimo responsivo
        ),
    )