import reflex as rx
from open_reper.BackEnd.state import State
from open_reper.FrontEnd.constants import BLUE_HOVER, GREEN, GREEN_HOVER

def opening_recommendation(type_recommendation: str, style: str, description: str, opening: str):
    return rx.cond(
        State.recommendation,
        rx.box(
            rx.vstack(
                rx.heading(f"Recomendación de Apertura - {type_recommendation}", font_size="0.95em", color="white"),
                rx.hstack(
                    rx.vstack(
                        rx.text("Estilo detectado:", font_weight="bold", color="white", font_size="0.85em"),
                        rx.text(style, color="white", font_size="0.8em"),
                        rx.text("Descripción:", font_weight="bold", color="white", margin_top="0.4em", font_size="0.85em"),
                        rx.text(description, color="white", font_size="0.75em", text_align="justify"),
                        align_items="flex-start",
                        spacing="2",
                        padding="0.4em",
                    ),
                    rx.vstack(
                        rx.text("Apertura recomendada:", font_weight="bold", color="white", font_size="0.85em"),
                        rx.text(opening, color="white", font_size="0.8em"),
                        rx.link(
                            rx.button(
                                "Ver detalles",
                                bg=GREEN,
                                color="white",
                                border_radius="6px",
                                font_size="0.75em",
                                padding="0.4em 0.8em",
                                _hover={"bg": GREEN_HOVER},
                                on_click= lambda: State.set_recommend_opening(type_recommendation, opening, style)
                            ),
                            href="/opening-recommended",
                            margin_top="0.4em",
                        ),
                        align_items="flex-start",
                        spacing="2",
                        padding="0.4em",
                    ),
                    spacing="2",
                    justify_content="space-between",
                    flex="1 1 100%",
                ),
                bg=BLUE_HOVER,
                padding="1em",
                border_radius="6px",
                box_shadow="0 4px 8px rgba(0, 0, 0, 0.2)",
                width="100%",
            ),
            margin_y="0.7em",
            flex="1 0 calc(50% - 0.7em)",
            max_width="none",
            min_width="280px",
        ),
    )