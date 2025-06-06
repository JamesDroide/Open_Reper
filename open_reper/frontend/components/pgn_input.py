import reflex as rx

def pgn_input_component(on_change):
    return rx.text_area(
        placeholder="Pega tu PGN aquí...",
        on_change=on_change,
        width="400px",
        height="200px",
        border="1px solid #808080",
        padding="1em",
        color="black",
        bg="white"
    )
