from typing import List
import reflex as rx

def opening_description(description: str):
    return rx.box(
                rx.heading("Sobre esta Apertura",
                        font_size="1.1em",
                        color="white"),
                rx.text(
                    description,
                    color="white",
                    line_height="1.6",
                    font_size="0.9em"
                ),
                padding="0.7em",
                bg="#2a5c9a",
                border_radius="8px",
                margin_top="1.5em"
            )
    
def opening_plans(plans: List[str]):
    return rx.box(
                rx.heading("Planes Estratégicos",
                        font_size="1.05em",
                        color="white"),
                rx.unordered_list(
                    rx.foreach(
                        plans,
                        lambda plan: rx.list_item(
                            plan,
                            color="white",
                            margin_bottom="0.4em",
                            font_size="0.9em"
                        )
                    ),
                    padding_left="1.2em"
                ),
                padding="0.7em",
                bg="#2a5c9a",
                border_radius="8px",
                margin_top="1.5em"
            )