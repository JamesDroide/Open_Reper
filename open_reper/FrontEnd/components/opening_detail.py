import reflex as rx
from open_reper.BackEnd.state import State

def opening_detail():
    return rx.cond(
        State.opening_detail,
        rx.center(
            rx.box(
                rx.vstack(
                    rx.heading("Detalle de la Apertura", font_size="1.8em", color="white"),
                    rx.text(State.opening_detail.get('name', ''), font_size="1.2em", color="orange"),
                    rx.text(State.opening_detail.get('eco', ''), color="white"),
                    rx.text(State.opening_detail.get('description', ''), color="white", margin_top="1em"),
                    rx.text("Líneas principales:", font_weight="bold", color="white", margin_top="1em"),
                    rx.text(State.opening_detail.get('main_lines', ''), color="white"),
                    align_items="flex-start",
                    spacing="2",
                    padding="1em",
                    min_width="300px"
                ),
                bg="#1E3A5F",
                padding="2em",
                border_radius="8px",
                box_shadow="0 8px 16px rgba(0, 0, 0, 0.3)"
            ),
            width="100%",
            padding="2em",
            bg="#0d223a"
        ),
    )