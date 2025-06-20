import reflex as rx
from open_reper.BackEnd.state import State

def opening_recommendation():
    return rx.cond(
        State.recommendation,
        rx.center(
            rx.box(
                rx.vstack(
                    rx.heading("Recomendación de Apertura", font_size="1.8em", color="white"),
                    rx.hstack(
                        rx.vstack(
                            rx.text("Estilo detectado:", font_weight="bold", color="white"),
                            rx.text(State.recommendation['style'], color="white", font_size="1.2em"),
                            rx.text("Descripción:", font_weight="bold", color="white", margin_top="1em"),
                            rx.text(State.recommendation['description'], color="white"),
                            align_items="flex-start",
                            spacing="2",
                            padding="1em",
                            min_width="300px"
                        ),
                        rx.vstack(
                            rx.text("Apertura recomendada:", font_weight="bold", color="white"),
                            rx.text(State.recommendation['opening'], color="white", font_size="1.2em"),
                            rx.link(
                                rx.button(
                                    "Ver detalles de la apertura",
                                    bg="#FF9800",  # Naranja brillante
                                    color="white",
                                    border_radius="8px",
                                    font_weight="bold",
                                    font_size="1.1em",
                                    cursor="pointer",
                                ),
                                href="/opening-recommended"
                            ),
                            align_items="flex-start",
                            spacing="2",
                            padding="1em",
                            min_width="300px"
                        ),
                        spacing="4",
                        justify_content="center"
                    ),
                    bg="#1E3A5F",
                    padding="2em",
                    border_radius="8px",
                    margin_top="2em",
                    width="100%",
                    max_width="800px",
                    box_shadow="0 8px 16px rgba(0, 0, 0, 0.3)"
                ),
            ),
            width="100%",
            padding="2em",
            bg="#0d223a"
        ),
    )