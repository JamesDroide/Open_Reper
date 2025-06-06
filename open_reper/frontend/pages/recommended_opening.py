import reflex as rx
from open_reper.frontend.components import header_component, recommendation_component, board_control_component

@rx.page(route="/opening-recommended")
def recommended_opening(state):
    return rx.center(
        rx.vstack(
            header_component(),
            rx.heading(State.recommended_opening['name'], font_size="3em", color="white", margin_bottom="1em"),
            recommendation_component(state.recommended_opening),
            board_control_component(state),
            rx.box(
                rx.heading("Sobre esta Apertura", font_size="1.5em", color="white", margin_bottom="0.5em"),
                rx.text(
                    State.recommended_opening['description'],
                    color="white",
                    font_size="1.1em",
                    line_height="1.6",
                    margin_bottom="1em"
                ),
                rx.heading("Planes Estratégicos", font_size="1.3em", color="white", margin_bottom="0.5em"),
                rx.unordered_list(
                    rx.foreach(
                        State.recommended_opening["plans"],
                        lambda plan: rx.list_item(
                            plan,
                            color="white",
                            margin_bottom="0.5em",
                            font_size="1.1em"
                        )
                    ),
                    padding_left="1.5em"
                ),
                width="100%",
                max_width="800px"
            ),
            spacing="4",
            align_items="center",
            width="100%",
            padding="1em"
        ),
        height="auto",
        background_color="#2A5C9A",
        padding="2em"
    )
