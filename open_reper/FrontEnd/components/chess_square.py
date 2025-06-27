import reflex as rx
from open_reper.BackEnd.state import State
from open_reper.FrontEnd.components.game_pieces import PIECE_MAP
from open_reper.FrontEnd.constants import DARK_SQUARE, LEGAL_MOVE_SQUARE, LIGHT_SQUARE, SELECTED_SQUARE

def chess_square(square: str):
    """Componente para una casilla del tablero con imágenes"""
    is_selected = State.selected_square == square
    is_legal_move = State.legal_moves.contains(square)

    is_light = (ord(square[0]) - ord('a') + int(square[1])) % 2 == 0
    base_bg_color = LIGHT_SQUARE if is_light else DARK_SQUARE

    bg_color = rx.cond(
        is_selected,
        SELECTED_SQUARE,
        rx.cond(is_legal_move, LEGAL_MOVE_SQUARE, base_bg_color)
    )

    piece_symbol = rx.cond(
        State.position.contains(square),
        State.position[square],
        ""
    )

    piece_component = rx.match(
        piece_symbol,
        *[(symbol, component) for symbol, component in PIECE_MAP.items()],
        rx.box(width="50px", height="50px")
    )

    return rx.box(
        piece_component,
        on_click=lambda: State.select_square(square),
        width="60px",
        height="60px",
        display="flex",
        justify_content="center",
        align_items="center",
        bg=bg_color,
        border="1px solid #444",
        _hover={"cursor": "pointer", "filter": "brightness(1.2)"}
    )