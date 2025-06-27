from typing import List
import reflex as rx

def opening_description(description: str):
    return rx.box(
                rx.heading("Sobre esta Apertura",
                        font_size="1.5em",
                        color="white"),
                rx.text(
                    description,
                    color="white",
                    line_height="2"
                ),
                padding="0.5em",
                bg="#2a5c9a",
                border_radius="8px",
                margin_top="2em"
            )
    
def opening_plans(plans: List[str]):
    return rx.box(
                rx.heading("Planes Estratégicos",
                        font_size="1.3em",
                        color="white"),
                rx.unordered_list(
                    rx.foreach(
                        plans,
                        lambda plan: rx.list_item(
                            plan,
                            color="white",
                            margin_bottom="0.5em"
                        )
                    ),
                    padding_left="1.5em"
                ),
                padding="0.5em",
                bg="#2a5c9a",
                border_radius="8px"
            )