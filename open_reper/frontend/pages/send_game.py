import reflex as rx
from open_reper.frontend.components import header_component, pgn_input_component, recommendation_component

@rx.page(route="/send-game")
def send_game(state):
    return rx.center(
        rx.vstack(
            header_component(),
            pgn_input_component(state.set_pgn_text),
            rx.button(
                "Obtener Recomendación",
                on_click=state.get_recommendation,
                bg="#4CAF50",
                color="white",
                margin_top="1em",
                is_loading=state.is_loading,
                _hover={"bg": "#45a049"}
            ),
            rx.cond(
                state.error,
                rx.text(state.error, color="red", font_weight="bold"),
            ),
            rx.cond(
                state.recommendation,
                recommendation_component(state.recommendation),
            ),
            spacing="4",
            align="center",
            width="100%",
            max_width="800px"
        ),
        height="100vh",
        background_color="#2A5C9A",
        padding="2em",
    )
