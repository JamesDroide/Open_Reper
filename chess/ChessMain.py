import pygame as p
import ChessEngine, SmartMoveFinder

BOARD_WIDTH = BOARD_HEIGHT = 512
MOVE_LOG_PANEL_WIDTH = 250
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
DIMENSION = 8
SQ_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

BACKGROUND_COLOR = (42, 92, 154)
BUTTON_COLOR = (242, 65, 0)
TEXT_COLOR = (255, 255, 255)

class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = p.Rect(x, y, width, height)
        self.text = text
        self.action = action

    def draw(self, screen):
        p.draw.rect(screen, BUTTON_COLOR, self.rect)
        font = p.font.Font(None, 30)
        text_surf = font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

def main_menu():
    p.init()
    screen = p.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
    p.display.set_caption("Ajedrez - Menú Principal")

    try:
        logo = p.image.load("logo.png")
        logo = p.transform.scale(logo, (int(logo.get_width()*0.5), int(logo.get_height()*0.5)))
        logo_rect = logo.get_rect(center=(BOARD_WIDTH//2, 100))
    except:
        logo = None

    button_width = 300
    button_height = 60
    button_y = 250
    button_spacing = 70

    play_button = Button(
        BOARD_WIDTH//2 - button_width//2,
        button_y,
        button_width,
        button_height,
        "Reproducir Partida",
        action=lambda: start_game(screen, True, True)
    )
    ai_button = Button(
        BOARD_WIDTH//2 - button_width//2,
        button_y + button_spacing,
        button_width,
        button_height,
        "Juega contra la máquina",
        action=lambda: start_game(screen, True, False)
    )
    exit_button = Button(
        BOARD_WIDTH//2 - button_width//2,
        button_y + button_spacing*2,
        button_width,
        button_height,
        "Salir",
        action=lambda: p.event.post(p.event.Event(p.QUIT))
    )

    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)
        
        if logo:
            screen.blit(logo, logo_rect)
        play_button.draw(screen)
        ai_button.draw(screen)
        exit_button.draw(screen)
        
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
            if event.type == p.MOUSEBUTTONDOWN:
                if play_button.rect.collidepoint(event.pos):
                    play_button.action()
                elif ai_button.rect.collidepoint(event.pos):
                    ai_button.action()
                elif exit_button.rect.collidepoint(event.pos):
                    exit_button.action()
        
        p.display.flip()
    
    p.quit()

def start_game(screen, player1, player2):
    main(screen, player1, player2)
    main_menu()

def load_images():
    pieces = ["wK", "wQ", "wB", "wN", "wR", "wp",
              "bK", "bQ", "bB", "bN", "bR", "bp"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(f"images/{piece}.png"), (SQ_SIZE, SQ_SIZE))

def main(screen, player_one, player_two):
    clock = p.time.Clock()
    gs = ChessEngine.GameState()
    valid_moves = gs.get_valid_moves()
    move_made = False
    animate = False
    load_images()
    running = True
    sq_selected = ()
    player_clicks = []
    game_over = False
    font = p.font.SysFont("Arial", 14, False, False)

    while running:
        human_turn = (gs.white_to_move and player_one) or (not gs.white_to_move and player_two)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
                gs.save_pgn_to_file("game.pgn")
            elif e.type == p.MOUSEBUTTONDOWN and not game_over and human_turn:
                location = p.mouse.get_pos()
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sq_selected == (row, col) or col >= 8:
                    sq_selected = ()
                    player_clicks = []
                else:
                    sq_selected = (row, col)
                    player_clicks.append(sq_selected)
                if len(player_clicks) == 2:
                    move = ChessEngine.Move(player_clicks[0], player_clicks[1], gs.board)
                    for valid_move in valid_moves:
                        if move == valid_move:
                            gs.make_move(valid_move)
                            move_made = True
                            animate = True
                            sq_selected = ()
                            player_clicks = []
                            break
                    if not move_made:
                        player_clicks = [sq_selected]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undo_move()
                    valid_moves = gs.get_valid_moves()
                    move_made = True
                    animate = False
                    game_over = False
                if e.key == p.K_r:
                    gs = ChessEngine.GameState()
                    valid_moves = gs.get_valid_moves()
                    sq_selected = ()
                    player_clicks = []
                    move_made = False
                    animate = False
                    game_over = False

        # Movimiento de la IA
        if not game_over and not human_turn:
            ai_move = SmartMoveFinder.find_best_move(gs, valid_moves)
            if ai_move is None:
                ai_move = SmartMoveFinder.find_random_move(valid_moves)
            gs.make_move(ai_move)
            move_made = True
            animate = True

        if move_made:
            if animate:
                animate_move(screen, gs.move_log[-1], gs.board, clock)
            valid_moves = gs.get_valid_moves()
            move_made = False
            animate = False

        draw_game_state(screen, gs, valid_moves, sq_selected, font)

        if gs.checkmate or gs.stalemate:
            game_over = True
            result_text = "Tablas por ahogado" if gs.stalemate else "Negras ganan" if gs.white_to_move else "Blancas ganan"
            draw_text(screen, result_text)
            gs.save_pgn_to_file("game.pgn")

        clock.tick(MAX_FPS)
        p.display.flip()

    # Reiniciar el estado al salir
    gs.save_pgn_to_file("game.pgn")

def draw_game_state(screen, gs, valid_moves, sq_selected, move_log_font):
    draw_board(screen)
    highlight_squares(screen, gs, valid_moves, sq_selected)
    draw_pieces(screen, gs.board)
    draw_move_log(screen, gs, move_log_font)

def draw_board(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def draw_pieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def draw_move_log(screen, gs, font):
    move_log_rect = p.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    p.draw.rect(screen, p.Color("black"), move_log_rect)
    move_log = gs.move_log
    move_texts = []
    for i in range(0, len(move_log), 2):
        move_str = f"{i//2 + 1}. {move_log[i]}"
        if i+1 < len(move_log):
            move_str += f" {move_log[i+1]}"
        move_texts.append(move_str)
    y = 5
    for text in move_texts:
        text_obj = font.render(text, True, p.Color("white"))
        screen.blit(text_obj, (BOARD_WIDTH + 5, y))
        y += text_obj.get_height() + 2

def highlight_squares(screen, gs, valid_moves, sq_selected):
    if sq_selected != ():
        r, c = sq_selected
        if gs.board[r][c][0] == ('w' if gs.white_to_move else 'b'):
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color('blue'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            s.fill(p.Color('yellow'))
            for move in valid_moves:
                if move.start_row == r and move.start_col == c:
                    screen.blit(s, (move.end_col*SQ_SIZE, move.end_row*SQ_SIZE))

def animate_move(screen, move, board, clock):
    colors = [p.Color("white"), p.Color("gray")]
    dr = move.end_row - move.start_row
    dc = move.end_col - move.start_col
    fps = 5
    frame_count = (abs(dr) + abs(dc)) * fps
    for frame in range(frame_count + 1):
        r = move.start_row + dr * frame / frame_count
        c = move.start_col + dc * frame / frame_count
        draw_board(screen)
        draw_pieces(screen, board)
        color = colors[(move.end_row + move.end_col) % 2]
        p.draw.rect(screen, color, (move.end_col*SQ_SIZE, move.end_row*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        if move.piece_captured != "--" and not move.is_enpassant_move:
            screen.blit(IMAGES[move.piece_captured], (move.end_col*SQ_SIZE, move.end_row*SQ_SIZE))
        screen.blit(IMAGES[move.piece_moved], (c*SQ_SIZE, r*SQ_SIZE))
        p.display.flip()
        clock.tick(60)

def draw_text(screen, text):
    font = p.font.SysFont("Helvetica", 32, True, False)
    text_obj = font.render(text, True, p.Color("gray"))
    text_rect = text_obj.get_rect(center=(BOARD_WIDTH//2, BOARD_HEIGHT//2))
    screen.blit(text_obj, text_rect)

if __name__ == "__main__":
    main_menu()