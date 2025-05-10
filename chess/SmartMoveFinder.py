import random

piece_score = {
    "K" : 0,
    "Q" : 9,
    "R" : 5,
    "B" : 3,
    "N" : 3,
    "p" : 1
}

CHECKMATE = 1000
STALEMATE = 0
DEPTH = 2

def find_random_move(valid_moves):
    return valid_moves[random.randint(0, len(valid_moves) - 1)]

def find_best_move(gs, valid_moves):
    global next_move, counter
    next_move = None
    counter = 0
    find_move_negamax_alphabeta(gs, valid_moves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.white_to_move else -1)
    return next_move

def find_move_negamax_alphabeta(gs, valid_moves, depth, alpha, beta, turn_multiplier):
    global next_move, counter
    counter += 1
    if depth == 0:
        return turn_multiplier * score_board(gs)
    
    # Ordenamiento de movimientos
    max_score = -CHECKMATE
    for move in valid_moves:
        gs.make_move(move)
        next_moves = gs.get_valid_moves()
        score = -find_move_negamax_alphabeta(gs, next_moves, depth - 1, -beta, -alpha, -turn_multiplier)
        if score > max_score:
            max_score = score
            if depth == DEPTH:
                next_move = move
        gs.undo_move()
        if max_score > alpha:
            alpha = max_score
        if alpha >= beta:
            break
    return max_score
    
def score_board(gs):
    if gs.checkmate:
        if gs.white_to_move:
            return -CHECKMATE # Negras ganan
        else:
            return CHECKMATE # Blancas ganan
    elif gs.stalemate:
        return STALEMATE # Tablas por ahogado
    
    score = 0
    for row in gs.board:
        for square in row:
            if square[0] == "w":
                score += piece_score[square[1]]
            elif square[0] == "b":
                score -= piece_score[square[1]]
    return score