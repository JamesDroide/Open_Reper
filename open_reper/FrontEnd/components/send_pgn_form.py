import reflex as rx
from open_reper.BackEnd.state import State
from open_reper.FrontEnd.constants import ORANGE, WHITE, FONT_FAMILY

def send_pgn_form():
    return rx.form(
        rx.center(
            rx.heading("Envía tu partida PGN", font_size="1.5em", color="white"),
            width="100%"
        ),
        rx.text_area(
            placeholder="Pega tu PGN aquí...",
            value=State.pgn_text,
            on_change=State.set_pgn_text,
            width="400px",
            height="200px",
            border_radius="8px",
            border="1px solid #808080",
            padding="1em",
            color="black",
            bg="white",
        ),
        rx.heading("Selecciona tu color:", font_size="1.2em", color="white"),
        rx.hstack(
            rx.image(
                src="/white-pawn.png",
                width="64px",
                height="64px",
                border=rx.cond(
                    State.selected_color == "white",
                    "3px solid #F24100",
                    "3px solid transparent"
                ),
                border_radius="8px",
                on_click=lambda: State.set_selected_color("white"),
                cursor="pointer",
                transition="transform 0.2s",
                _hover={"transform": "scale(1.1) rotate(-5deg)"},
                _active={"transform": "scale(0.95) rotate(5deg)"}
            ),
            rx.image(
                src="/black-pawn.png",
                width="64px",
                height="64px",
                border=rx.cond(
                    State.selected_color == "black",
                    "3px solid #F24100",
                    "3px solid transparent"
                ),
                border_radius="8px",
                on_click=lambda: State.set_selected_color("black"),
                cursor="pointer",
                transition="transform 0.2s",
                _hover={"transform": "scale(1.1) rotate(-5deg)"},
                _active={"transform": "scale(0.95) rotate(5deg)"}
            ),
            spacing="4",
            margin_top="2em",
            justify_content="center"
        ),
        rx.center(
            rx.cond(
                State.selected_color == "white",
                rx.badge("Blancas seleccionadas", color_scheme="orange"),
                rx.badge("Negras seleccionadas", color_scheme="orange")
            ),
            width="100%"
        ),
        rx.button(
            "Obtener Recomendación",
            on_click=State.get_recommendation,
            color=WHITE,
            margin_top="1em",
            is_loading=State.is_loading,
            _hover={"bg": "#e03d00"},
            font_family=FONT_FAMILY,
            align_self="center",
            padding="1em",
            bg="#2a5c9a",
            border_radius="8px",
            box_shadow="0 4px 8px rgba(0, 0, 0, 0.2)",
            min_width="400px",
            max_width="400px",
            flex_shrink=0
        ),
        rx.cond(
            State.error,
            rx.text(State.error, color="red", font_weight="bold"),
        ),
        spacing="4",
        align="center",
        width="100%",
        max_width="800px"
    )