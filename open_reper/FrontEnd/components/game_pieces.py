import reflex as rx

PIECE_MAP = {
    'r': rx.image(src="/game_pieces/bR.png", width="50px", height="50px"),
    'n': rx.image(src="/game_pieces/bN.png", width="50px", height="50px"),
    'b': rx.image(src="/game_pieces/bB.png", width="50px", height="50px"),
    'q': rx.image(src="/game_pieces/bQ.png", width="50px", height="50px"),
    'k': rx.image(src="/game_pieces/bK.png", width="50px", height="50px"),
    'p': rx.image(src="/game_pieces/bp.png", width="50px", height="50px"),
    'R': rx.image(src="/game_pieces/wR.png", width="50px", height="50px"),
    'N': rx.image(src="/game_pieces/wN.png", width="50px", height="50px"),
    'B': rx.image(src="/game_pieces/wB.png", width="50px", height="50px"),
    'Q': rx.image(src="/game_pieces/wQ.png", width="50px", height="50px"),
    'K': rx.image(src="/game_pieces/wK.png", width="50px", height="50px"),
    'P': rx.image(src="/game_pieces/wp.png", width="50px", height="50px"),
}