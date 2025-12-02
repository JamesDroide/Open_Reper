import reflex as rx
from open_reper.FrontEnd.constants import (
    BLUE_DARK, GRAY, WHITE,
    SIZE_LOGO, FONT_LG, FONT_SM,
    PADDING_SM, SPACING_XS,
    SHADOW_SM, TRANSITION_NORMAL, EASE_IN_OUT
)

def header(header: str, subheader: str):

    return rx.flex(
            # Logo con enlace
            rx.link(
                rx.image(
                    src="/logo_open_reper.webp",
                    width=SIZE_LOGO,  # [80px, 100px, 120px, 140px]
                    height="auto",
                    alt="Logo OpenReper",
                    loading="eager",  # Carga prioritaria para logo
                ),
                href="/",
                _hover={
                    "opacity": "0.85",
                    "transform": "scale(1.02)"
                },
                transition=f"all {TRANSITION_NORMAL[1]} {EASE_IN_OUT}",
            ),
            # Textos centrados
            rx.vstack(
                rx.heading(
                    header,
                    font_size=FONT_LG,  # [1.2em, 1.3em, 1.4em, 1.5em]
                    color=WHITE,
                    text_align="center",
                    as_="h1",
                    font_weight="700",
                    line_height="1.2"
                ),
                rx.text(
                    subheader,
                    color=GRAY,
                    font_size=FONT_SM,  # [0.85em, 0.9em, 0.95em, 1em]
                    text_align="center",
                    display=["none", "block", "block", "block"],  # Oculto en móvil pequeño
                    as_="p",
                    line_height="1.4"
                ),
                spacing="1",
                align_items="center",
                flex_grow=1,
                width="100%"
            ),
            justify_content="space-between",
            align_items="center",
            width="100%",
            padding=PADDING_SM,  # [0.5em, 0.6em, 0.7em, 0.8em]
            gap=SPACING_XS,  # [0.3em, 0.4em, 0.5em, 0.6em]
            bg=BLUE_DARK,
            box_shadow=SHADOW_SM,  # Sombra sutil para profundidad
            position="sticky",  # Header pegajoso
            top="0",
            z_index="200"  # Sobre otros elementos
        ),