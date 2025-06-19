# frontend/views/send_game.py
from open_reper.BackEnd.state import State
import reflex as rx

@rx.page(route="/send-game")
def send_game_view():
    return rx.center(
        rx.vstack(
            rx.heading("Recomendador de Aperturas", font_size="2em", color="white"),
            rx.heading("Envía tu partida PGN", font_size="1.5em", color="white"),
            rx.text_area(
                placeholder="Pega tu PGN aquí...",
                on_change=State.set_pgn_text,
                width="400px",
                height="200px",
                border="1px solid #808080",
                padding="1em",
                color="black",
                bg="white"
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
            rx.cond(
                State.selected_color == "white",
                rx.badge("Blancas seleccionadas", color_scheme="orange"),
                rx.badge("Negras seleccionadas", color_scheme="orange")
            ),
            rx.button(
                "Obtener Recomendación",
                on_click=State.get_recommendation,
                bg="#4CAF50",
                color="white",
                margin_top="1em",
                is_loading=State.is_loading,
                _hover={"bg": "#45a049"}
            ),
            rx.cond(
                State.error,
                rx.text(State.error, color="red", font_weight="bold"),
            ),
            rx.cond(
                State.recommendation,
                rx.box(
                    rx.text("Recomendación:", font_weight="bold", color="white"),
                    rx.text(f"Estilo: {State.recommendation['style']}", color="white"),
                    rx.text(f"Apertura: {State.recommendation['opening']}", color="white"),
                    rx.text(f"Descripción: {State.recommendation['description']}", color="white"),
                    rx.link(
                        rx.button(
                            "Ver detalles de la apertura",
                            bg="#1E3A5F",
                            color="white",
                            border_radius="8px",
                            padding_x=4,
                            margin_top=4
                        ),
                        href="/opening-recommended"
                    ),
                    bg="#1E3A5F",
                    padding="2em",
                    border_radius="8px",
                    margin_top="2em",
                    width="100%",
                    max_width="600px"
                ),
            ),
            spacing="4",
            align="center",
            width="100%",
            max_width="800px"
        ),
        height="auto",
        background_color="#2A5C9A",
        padding="2em",
    )