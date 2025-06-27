import reflex as rx
from open_reper.FrontEnd.constants import BLUE_DARK, GRAY

def header(header: str, subheader: str):
    return rx.flex(
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
                rx.heading(header, font_size="2em", color="white"),
                rx.text(subheader, color=GRAY),
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