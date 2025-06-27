import reflex as rx
from open_reper.BackEnd.state import State
from open_reper.FrontEnd.constants import BLUE_DARK, BLUE_HOVER, GREEN, GREEN_HOVER

def opening_recommendation(style: str, description: str, opening: str):
    return rx.cond(
        State.recommendation,
        rx.box(
            rx.vstack(
                rx.heading("Recomendación de Apertura", font_size="1.1em", color="white"),
                rx.hstack(
                    rx.vstack(
                        rx.text("Estilo detectado:", font_weight="bold", color="white"),
                        rx.text(style, color="white", font_size="0.9em"),
                        rx.text("Descripción:", font_weight="bold", color="white", margin_top="0.5em"),
                        rx.text(description, color="white", font_size="0.8em", text_align="justify"),
                        align_items="flex-start",
                        spacing="2",
                        padding="0.5em",
                    ),
                    rx.vstack(
                        rx.text("Apertura recomendada:", font_weight="bold", color="white"),
                        rx.text(opening, color="white", font_size="0.9em"),
                        rx.link(
                            rx.button(
                                "Ver detalles",
                                bg=GREEN,
                                color="white",
                                border_radius="6px",
                                font_size="0.8em",
                                _hover={"bg": GREEN_HOVER}
                            ),
                            href="/opening-recommended",
                            margin_top="0.5em",
                        ),
                        align_items="flex-start",
                        spacing="2",
                        padding="0.5em",
                    ),
                    spacing="3",
                    justify_content="space-between",
                    flex="1 1 100%",
                ),
                bg=BLUE_HOVER,
                padding="1.5em",
                border_radius="6px",
                box_shadow="0 4px 8px rgba(0, 0, 0, 0.2)",
                width="100%",
            ),
            margin_y="1em",
            flex="1 0 calc(50% - 1em)",
            max_width="none",
            min_width="350px",
        ),
    )