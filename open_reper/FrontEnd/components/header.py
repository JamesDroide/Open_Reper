import reflex as rx
from open_reper.FrontEnd.constants import BLUE_DARK, GRAY

def header(header: str, subheader: str):
    return rx.flex(
            rx.link(
                rx.image(
                    src="/logo_open_reper.webp",
                    width="130px",
                    height="auto",
                ),
                href="/",
                _hover={"cursor: pointer"},
            ),
            rx.vstack(
                rx.heading(header, font_size="1.4em", color="white"),
                rx.text(subheader, color=GRAY, font_size="0.9em"),
                spacing="1",
                align_items="center",
                flex_grow=1
            ),
            justify_content="space-between",
            align_items="center",
            width="100%",
            padding="0.7em",
            bg=BLUE_DARK
        ),