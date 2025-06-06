import reflex as rx

def recommendation_component(state):
    return rx.box(
        rx.text(f"Estilo: {state['style']}", color="white"),
        rx.text(f"Apertura: {state['opening']}", color="white"),
        rx.text(f"Descripción: {state['description']}", color="white")
    )
