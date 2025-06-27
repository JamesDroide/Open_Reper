import reflex as rx
from open_reper.FrontEnd.constants import BLUE_DARK

def header():
    return rx.hstack(
        rx.flex(
            rx.link(
                rx.image(
                    src="/logo_open_reper.png",
                    width="200px",
                    height="auto",
                ),
                href="/",
                _hover={"cursor: pointer"},
            ),
            rx.vstack(
                rx.heading("Recomendación de apertura", font_size="2em", color="white"),
                rx.text("Mejora tu juego con recomendaciones basadas en tu estilo", color="#d1e0e0"),
                spacing="1",
                align_items="center",
                flex_grow=1
            ),
            justify_content="space-between",
            align_items="center",
            width="100%",
            padding="1em",
            bg=BLUE_DARK
        ),

    )