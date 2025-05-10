"""
Aca es donde se almacena toda la informacion sobre el estado actual del tablero
"""

class GameState():
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        # Los guiones es para tener una mejor forma de convertirlo a una pieza en caso que se mueva alguna ahi
        self.white_to_move = True
        self.move_log = []
        # Diccionario para las funciones de los movimientos de las piezas
        self.move_functions = {
            'p': self.get_pawn_moves, 
            'R': self.get_rook_moves,
            'N': self.get_knight_moves,
            'B': self.get_bishop_moves,
            'Q': self.get_queen_moves,
            'K': self.get_king_moves
        }
        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)
        self.in_check = False
        self.checkmate = False
        self.stalemate = False
        self.pins = []
        self.pgn_moves = []
        self.checks = []
        self.enpassant_possible = ()
        self.enpassant_possible_log = [self.enpassant_possible]
        self.current_castling_rights = CastleRights(True, True, True, True)
        self.castle_rights_log = [CastleRights(self.current_castling_rights.wks, self.current_castling_rights.bks, 
                                               self.current_castling_rights.wqs, self.current_castling_rights.bqs)]
        

    def make_move(self, move):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move

        if move.piece_moved == 'wK':
            self.white_king_location = (move.end_row, move.end_col)
        elif move.piece_moved == 'bK':
            self.black_king_location = (move.end_row, move.end_col)

        if move.is_castle_move:
            if move.end_col - move.start_col == 2:
                self.board[move.end_row][move.end_col - 1] = self.board[move.end_row][move.end_col + 1]
                self.board[move.end_row][move.end_col + 1] = "--"
            else:
                self.board[move.end_row][move.end_col + 1] = self.board[move.end_row][move.end_col - 2]
                self.board[move.end_row][move.end_col - 2] = "--"

        if move.is_enpassant_move:
            self.board[move.start_row][move.end_col] = "--"

        self.enpassant_possible_log.append(self.enpassant_possible)
        if move.piece_moved[1] == 'p' and abs(move.start_row - move.end_row) == 2:
            self.enpassant_possible = ((move.start_row + move.end_row) // 2, move.end_col)
        else:
            self.enpassant_possible = ()

        if move.is_pawn_promotion:
            promoted_piece = 'Q'
            self.board[move.end_row][move.end_col] = move.piece_moved[0] + promoted_piece
            move.promoted_piece = promoted_piece

        self.update_castle_rights(move)
        self.castle_rights_log.append(CastleRights(
            self.current_castling_rights.wks,
            self.current_castling_rights.bks,
            self.current_castling_rights.wqs,
            self.current_castling_rights.bqs
        ))

        # Verificación de jaque corregida (sin cambios de turno adicionales)
        self.in_check, self.pins, self.checks = self.check_pins_and_checks()
        move.is_check = self.in_check

        valid_moves = self.get_valid_moves()
        if len(valid_moves) == 0:
            if self.in_check:
                move.is_checkmate = True
                self.checkmate = True
            else:
                move.is_stalemate = True
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False

        if len(self.move_log) % 2 == 1:  # Movimiento de las blancas
            move_number = len(self.move_log) // 2 + 1
            self.pgn_moves.append(f"{move_number}. {str(move)}")
        else:  # Movimiento de las negras
            if self.pgn_moves:  # Asegurarse de que haya un movimiento previo
                self.pgn_moves[-1] += f" {str(move)}"
            else:
                # Si es el primer movimiento de las negras, agregarlo como un nuevo número
                move_number = len(self.move_log) // 2 + 1
                self.pgn_moves.append(f"{move_number}. {str(move)}")

    def undo_move(self):
        if len(self.move_log) != 0: # Solo se puede deshacer movimientos en caso de haber movimientos
            move = self.move_log.pop() # Sacamos el ultimo movimiento
            self.board[move.start_row][move.start_col] = move.piece_moved # Regresamos la pieza a su lugar
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move # Cambiamos el turno de quien juega nuevamente
            if move.piece_moved == 'wK':
                self.white_king_location = (move.start_row, move.start_col)
            elif move.piece_moved == 'bK':
                self.black_king_location = (move.start_row, move.start_col)
            # Deshacer las capturas al paso
            if move.is_enpassant_move:
                self.board[move.end_row][move.end_col] = "--"
                self.board[move.start_row][move.end_col] = move.piece_captured
            self.enpassant_possible_log.pop()
            self.enpassant_possible = self.enpassant_possible_log[-1]
            # Deshacer los enroques
            self.castle_rights_log.pop()
            new_castle_rights = self.castle_rights_log[-1]
            self.current_castling_rights = CastleRights(new_castle_rights.wks, new_castle_rights.bks, new_castle_rights.wqs, new_castle_rights.bqs)

            if move.is_castle_move:
                if move.end_col - move.start_col == 2:
                    self.board[move.end_row][move.end_col + 1] = self.board[move.end_row][move.end_col - 1]
                    self.board[move.end_row][move.end_col - 1] = "--"
                else:
                    self.board[move.end_row][move.end_col - 2] = self.board[move.end_row][move.end_col + 1]
                    self.board[move.end_row][move.end_col + 1] = "--"
            self.checkmate = False
            self.stalemate = False

    def update_castle_rights(self, move):
        if move.piece_moved == "wK":
            self.current_castling_rights.wks = False
            self.current_castling_rights.wqs = False
        elif move.piece_moved == "bK":
            self.current_castling_rights.bks = False
            self.current_castling_rights.bqs = False
        elif move.piece_moved == "wR":
            if move.start_row == 7:
                if move.start_col == 0: # La torre de a1
                    self.current_castling_rights.wqs = False
                elif move.start_col == 7: # La torre de h1
                    self.current_castling_rights.wks = False
            elif move.start_row == 0:
                if move.start_col == 0: # La torre de a8
                    self.current_castling_rights.bqs = False
                elif move.start_col == 7: # La torre de h8
                    self.current_castling_rights.bks = False

        if move.piece_captured == 'wR':
            if move.end_row == 7:
                if move.end_col == 0:
                    self.current_castling_rights.wqs = False
                elif move.end_col == 7:
                    self.current_castling_rights.wks = False
        elif move.piece_captured == 'bR':
            if move.end_row == 0:
                if move.end_col == 0:
                    self.current_castling_rights.bqs = False
                elif move.end_col == 7:
                    self.current_castling_rights.bks = False

    def get_valid_moves(self):
        moves = []
        self.in_check, self.pins, self.checks = self.check_pins_and_checks()
        
        if self.white_to_move:
            king_row, king_col = self.white_king_location
        else:
            king_row, king_col = self.black_king_location

        if self.in_check:
            if len(self.checks) == 1:
                check = self.checks[0]
                check_row, check_col = check[0], check[1]
                piece_checking = self.board[check_row][check_col]
                valid_squares = []

                if piece_checking[1] == 'N':
                    valid_squares = [(check_row, check_col)]
                else:
                    for i in range(1, 8):
                        valid_square = (king_row + check[2] * i, king_col + check[3] * i)
                        valid_squares.append(valid_square)
                        if valid_square == (check_row, check_col):
                            break

                temp_moves = self.get_all_posible_moves()
                for move in temp_moves:
                    if move.piece_moved[1] == 'K' or (move.end_row, move.end_col) in valid_squares:
                        moves.append(move)
            else:
                self.get_king_moves(king_row, king_col, moves)
        else:
            moves = self.get_all_posible_moves()

        # Procesar ambigüedades
        move_dict = {}
        for move in moves:
            key = (move.piece_moved[1], move.end_row, move.end_col)
            if key not in move_dict:
                move_dict[key] = []
            move_dict[key].append(move)
        
        for key in move_dict:
            move_list = move_dict[key]
            if len(move_list) > 1:
                files = set()
                ranks = set()
                for m in move_list:
                    files.add(m.start_col)
                    ranks.add(m.start_row)
                
                if len(files) == 1:
                    for m in move_list:
                        m.disambiguate_rank = True
                elif len(ranks) == 1:
                    for m in move_list:
                        m.disambiguate_file = True
                else:
                    for m in move_list:
                        m.disambiguate_file = True
                        m.disambiguate_rank = True

        if len(moves) == 0:
            self.checkmate = self.in_check
            self.stalemate = not self.in_check
        else:
            self.checkmate = False
            self.stalemate = False

        return moves

    def check_pins_and_checks(self):
        pins = []
        checks = []
        in_check = False
        if self.white_to_move:
            enemy_color = 'b'
            ally_color = 'w'
            start_row = self.white_king_location[0]
            start_col = self.white_king_location[1]
        else:
            enemy_color = 'w'
            ally_color = 'b'
            start_row = self.black_king_location[0]
            start_col = self.black_king_location[1]
        directions = ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            d = directions[j]
            possible_pin = ()
            for i in range(1, 8):
                end_row = start_row + d[0] * i
                end_col = start_col + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] == ally_color and end_piece[1] != 'K':
                        if possible_pin == ():
                            possible_pin = (end_row, end_col, d[0], d[1])
                        else:
                            break
                    elif end_piece[0] == enemy_color:
                        type_piece = end_piece[1]
                        if (0 <= j <= 3 and type_piece == 'R') or \
                            (4 <= j <= 7 and type_piece == 'B') or \
                                (i == 1 and type_piece == 'p' and ((enemy_color == 'w' and 4 <= j <= 5) or (enemy_color == 'b' and 6 <= j <= 7))) or \
                                    (type_piece == 'Q') or (i == 1 and type_piece == 'K'):
                            if possible_pin == ():
                                in_check = True
                                checks.append((end_row, end_col, d[0], d[1]))
                                break
                            else:
                                pins.append(possible_pin)
                                break
                        else:
                            break
                else:
                    break
        knight_moves = ((-2, -1), (-1, -2), (1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1))
        for m in knight_moves:
            end_row = start_row + m[0]
            end_col = start_col + m[1]  # Corregido start_row -> start_col
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] == enemy_color and end_piece[1] == 'N':
                    in_check = True
                    checks.append((end_row, end_col, m[0], m[1]))
        return in_check, pins, checks

    def get_all_posible_moves(self):
        moves = []
        for r in range(len(self.board)): # Numero de filas
            for c in range(len(self.board[r])): # Numero de columnas
                turn = self.board[r][c][0]
                if (turn == 'w' and self.white_to_move) or (turn == 'b' and not self.white_to_move):
                    piece = self.board[r][c][1]
                    self.move_functions[piece](r, c, moves)
        return moves

    def get_pawn_moves(self, r, c , moves):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if self.white_to_move:
            move_amount = -1
            start_row = 6
            enemy_color = 'b'
        else:
            move_amount = 1
            start_row = 1
            enemy_color = 'w'

        if self.board[r + move_amount][c] == "--":
            if not piece_pinned or pin_direction == (move_amount, 0):
                if r + move_amount in [0, 7]:  # Promoción
                    for promoted_piece in ['Q', 'R', 'B', 'N']:  # Opciones de promoción
                        moves.append(Move((r, c), (r + move_amount, c), self.board, promoted_piece=promoted_piece))
                else:
                    moves.append(Move((r, c), (r + move_amount, c), self.board))
                if r == start_row and self.board[r + 2 * move_amount][c] == "--":
                    moves.append(Move((r, c), (r + 2 * move_amount, c), self.board))
        if c - 1 >= 0:
            if not piece_pinned or pin_direction == (move_amount, -1):
                if self.board[r + move_amount][c - 1][0] == enemy_color:
                    moves.append(Move((r, c), (r + move_amount, c - 1), self.board)) 
                if (r + move_amount, c - 1) == self.enpassant_possible:
                    moves.append(Move((r, c), (r + move_amount, c - 1), self.board, is_enpassant_move = True))
        if c + 1 <= 7:
            if not piece_pinned or pin_direction == (move_amount, 1):
                if self.board[r + move_amount][c + 1][0] == enemy_color:
                    moves.append(Move((r, c), (r + move_amount, c + 1), self.board)) 
                if (r + move_amount, c + 1) == self.enpassant_possible:
                    moves.append(Move((r, c), (r + move_amount, c + 1), self.board, is_enpassant_move = True))
        
    def get_rook_moves(self, r, c , moves):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][i] != 'Q':
                    self.pins.remove(self.pins[i])
                break
        directions = ((-1, 0), (1, 0), (0, -1), (0, 1)) # En linea recta
        enemy_color = 'b' if self.white_to_move else 'w'
        for d in directions:
            for i in range(1, 8):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8: # Osea que este en el tablero
                    if not piece_pinned or pin_direction == (-d[0], -d[1]) or pin_direction == d:
                        end_piece = self.board[end_row][end_col]
                        if end_piece == "--": # Verificar que la casilla este vacia
                            moves.append(Move((r, c), (end_row, end_col), self.board))
                        elif end_piece[0] == enemy_color: # Verificar que la pieza sea del enemigo
                            moves.append(Move((r, c), (end_row, end_col), self.board))
                            break
                        else: # Este seria el caso de que la pieza sea del mismo color
                            break
                else: # Si se sale del tablero
                    break

    def get_knight_moves(self, r, c , moves):
        piece_pinned = False
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                self.pins.remove(self.pins[i])
                break
        knight_moves = ((-2, -1), (-1, -2), (1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1)) # Movimientos en L
        ally_color = 'w' if self.white_to_move else 'b'
        for m in knight_moves:
            end_row = r + m[0]
            end_col = c + m[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                if not piece_pinned:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] != ally_color:
                        moves.append(Move((r, c), (end_row, end_col), self.board))

    def get_bishop_moves(self, r, c , moves):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1)) # Diagonales
        enemy_color = 'b' if self.white_to_move else 'w'
        for d in directions:
            for i in range(1, 8):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8: # Osea que este en el tablero
                    if not piece_pinned or pin_direction == (-d[0], -d[1]) or pin_direction == d:
                        end_piece = self.board[end_row][end_col]
                        if end_piece == "--": # Verificar que la casilla este vacia
                            moves.append(Move((r, c), (end_row, end_col), self.board))
                        elif end_piece[0] == enemy_color: # Verificar que la pieza sea del enemigo
                            moves.append(Move((r, c), (end_row, end_col), self.board))
                            break
                        else: # Este seria el caso de que la pieza sea del mismo color
                            break
                else: # Si se sale del tablero
                    break

    def get_queen_moves(self, r, c , moves):
        self.get_bishop_moves(r, c, moves)
        self.get_rook_moves(r, c, moves)

    def get_king_moves(self, r, c , moves):
        row_moves = (-1, -1, -1, 0, 0, 1, 1, 1)
        col_moves = (-1, 0, 1, -1, 1, -1, 0, 1)
        ally_color = 'w' if self.white_to_move else 'b'
        for i in range(8):
            end_row = r + row_moves[i]
            end_col = c + col_moves[i]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color:
                    # Pone al rey en las casillas que estan en jaque para validarlo
                    if ally_color == 'w':
                        self.white_king_location = (end_row, end_col)
                    else:
                        self.black_king_location = (end_row, end_col)
                    in_check, pins, checks = self.check_pins_and_checks()
                    if not in_check:
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                    # Devuelve al rey a su casilla original
                    if ally_color == 'w':
                        self.white_king_location = (r, c)
                    else:
                        self.black_king_location = (r, c)
        self.get_castle_moves(r, c, moves, ally_color)
       
    def get_castle_moves(self, r, c, moves, ally_color):
        in_check = self.square_under_attack(r, c, ally_color)
        if in_check:
            return
        if (self.white_to_move and self.current_castling_rights.wks) or (not self.white_to_move and self.current_castling_rights.bks):
            self.get_kingside_castle_moves(r, c, moves, ally_color)
        if (self.white_to_move and self.current_castling_rights.wqs) or (not self.white_to_move and self.current_castling_rights.bqs):
            self.get_queenside_castle_moves(r, c, moves, ally_color)
        
    def get_kingside_castle_moves(self, r, c, moves, ally_color):
        if self.board[r][c + 1] == '--' and self.board[r][c + 2] == '--':
            if not self.square_under_attack(r, c + 1, ally_color) and not self.square_under_attack(r, c + 2, ally_color):
                moves.append(Move((r, c), (r, c + 2), self.board, is_castle_move = True))

    def get_queenside_castle_moves(self, r, c, moves, ally_color):
        if self.board[r][c - 1] == '--' and self.board[r][c - 2] == '--' and self.board[r][c - 3] == '--':
            if not self.square_under_attack(r, c - 1, ally_color) and not self.square_under_attack(r, c - 2, ally_color):
                moves.append(Move((r, c), (r, c - 2), self.board, is_castle_move=True))

    def square_under_attack(self, r, c, ally_color):
        enemy_color = 'w' if ally_color == 'b' else 'b'
        directions = [(-1,0),(0,-1),(1,0),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]
        
        for j, d in enumerate(directions):
            for i in range(1,8):
                end_row = r + d[0]*i
                end_col = c + d[1]*i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] == ally_color:
                        break
                    elif end_piece[0] == enemy_color:
                        type = end_piece[1]
                        if (0 <= j <=3 and type == 'R') or \
                        (4 <= j <=7 and type == 'B') or \
                        (i == 1 and type == 'p' and ((enemy_color == 'w' and 6 <= j <=7) or (enemy_color == 'b' and 4 <= j <=5))) or \
                        (type == 'Q') or (i == 1 and type == 'K'):
                            return True
                        else:
                            break
                else:
                    break

        knight_moves = [(-2,-1),(-1,-2),(1,-2),(2,-1),(2,1),(1,2),(-1,2),(-2,1)]
        for m in knight_moves:
            end_row = r + m[0]
            end_col = c + m[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece == enemy_color + 'N':
                    return True
        return False
    
    def save_pgn_to_file(self, filename="game.pgn"):
        with open(filename, "w") as file:
            # Escribir encabezados básicos del PGN
            file.write('[Event "Chess Game"]\n')
            file.write('[White "Player1"]\n')
            file.write('[Black "Player2"]\n')
            file.write('[Result "' + ("1-0" if self.checkmate and not self.white_to_move else "0-1" if self.checkmate else "*") + '"]\n\n')

            # Escribir los movimientos
            for move in self.pgn_moves:
                file.write(move + " ")
            file.write("\n")

class Move():

    # Mapeo de las filas y columnas a los indices del tablero
    rank_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_rank = {v: k for k, v in rank_to_rows.items()}
    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def __init__(self, start_sq, end_sq, board, is_enpassant_move=False, is_castle_move=False, promoted_piece='Q', is_check=False, is_checkmate=False, is_stalemate=False, disambiguate_file=False, disambiguate_rank=False):
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.is_pawn_promotion = self.piece_moved[1] == 'p' and (self.end_row == 0 or self.end_row == 7)
        self.is_enpassant_move = is_enpassant_move
        if self.is_enpassant_move:
            self.piece_captured = 'wp' if self.piece_moved == 'bp' else 'bp'
        self.is_castle_move = is_castle_move
        self.promoted_piece = promoted_piece.upper() if promoted_piece else None
        self.is_check = is_check
        self.is_checkmate = is_checkmate
        self.is_stalemate = is_stalemate
        self.disambiguate_file = disambiguate_file
        self.disambiguate_rank = disambiguate_rank
        self.is_captured = self.piece_captured != '--'
        self.move_id = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col # Para identificar el movimiento

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False

    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_col) + "-" + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self, r, c):
        return self.cols_to_files[c] + self.rows_to_rank[r]
    
    def __str__(self):
        if self.is_castle_move:
            return "O-O" if self.end_col == 6 else "O-O-O"
        
        end_square = self.get_rank_file(self.end_row, self.end_col)
        move_str = ''

        if self.piece_moved[1] == 'p':
            if self.is_captured:
                move_str += self.cols_to_files[self.start_col] + 'x'
            move_str += end_square
            if self.is_pawn_promotion:
                move_str += f"={self.promoted_piece}"
        else:
            move_str += self.piece_moved[1]
            if self.disambiguate_file:
                move_str += self.cols_to_files[self.start_col]
            elif self.disambiguate_rank:
                move_str += self.rows_to_rank[self.start_row]
            if self.is_captured:
                move_str += 'x'
            move_str += end_square

        if self.is_checkmate:
            move_str += '#'
        elif self.is_check:
            move_str += '+'
        return move_str

class CastleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs