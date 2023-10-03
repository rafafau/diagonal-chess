import ai


class Piece:
    WHITE = "W"
    BLACK = "B"

    def __init__(self, x, y, color, piece_type, value):
        self.x = x
        self.y = y
        self.color = color
        self.piece_type = piece_type
        self.value = value


    def get_possible_diagonal_moves(self, board):
        moves = []

        for i in range(1, 8):
            if not board.in_bounds(self.x + i, self.y + i):
                break

            piece = board.get_piece(self.x + i, self.y + i)
            moves.append(self.get_move(board, self.x + i, self.y + i))
            if piece != 0:
                break

        for i in range(1, 8):
            if not board.in_bounds(self.x + i, self.y - i):
                break

            piece = board.get_piece(self.x + i, self.y - i)
            moves.append(self.get_move(board, self.x + i, self.y - i))
            if piece != 0:
                break

        for i in range(1, 8):
            if not board.in_bounds(self.x - i, self.y - i):
                break

            piece = board.get_piece(self.x - i, self.y - i)
            moves.append(self.get_move(board, self.x - i, self.y - i))
            if piece != 0:
                break

        for i in range(1, 8):
            if not board.in_bounds(self.x - i, self.y + i):
                break

            piece = board.get_piece(self.x - i, self.y + i)
            moves.append(self.get_move(board, self.x - i, self.y + i))
            if piece != 0:
                break

        return self.remove_null_from_list(moves)

    def get_possible_horizontal_moves(self, board):
        moves = []

        # Moves to the right of the piece.
        for i in range(1, 8 - self.x):
            piece = board.get_piece(self.x + i, self.y)
            moves.append(self.get_move(board, self.x + i, self.y))

            if piece != 0:
                break

        # Moves to the left of the piece.
        for i in range(1, self.x + 1):
            piece = board.get_piece(self.x - i, self.y)
            moves.append(self.get_move(board, self.x - i, self.y))
            if piece != 0:
                break

        # Downward moves.
        for i in range(1, 8 - self.y):
            piece = board.get_piece(self.x, self.y + i)
            moves.append(self.get_move(board, self.x, self.y + i))
            if piece != 0:
                break

        # Upward moves.
        for i in range(1, self.y + 1):
            piece = board.get_piece(self.x, self.y - i)
            moves.append(self.get_move(board, self.x, self.y - i))
            if piece != 0:
                break

        return self.remove_null_from_list(moves)

    def get_move(self, board, xto, yto):
        move = 0
        if board.in_bounds(xto, yto):
            piece = board.get_piece(xto, yto)
            if piece != 0:
                if piece.color != self.color:
                    move = ai.Move(self.x, self.y, xto, yto)
            else:
                move = ai.Move(self.x, self.y, xto, yto)
        return move

    def remove_null_from_list(self, l):
        return [move for move in l if move != 0]

    def to_string(self):
        return self.color + self.piece_type


class Rook(Piece):
    PIECE_TYPE = "R"
    VALUE = 5

    def __init__(self, x, y, color):
        super(Rook, self).__init__(x, y, color, Rook.PIECE_TYPE, Rook.VALUE)

    def get_possible_moves(self, board):
        return self.get_possible_horizontal_moves(board)

    def clone(self):
        return Rook(self.x, self.y, self.color)


class Knight(Piece):
    PIECE_TYPE = "N"
    VALUE = 3

    def __init__(self, x, y, color):
        super(Knight, self).__init__(x, y, color, Knight.PIECE_TYPE, Knight.VALUE)

    def get_possible_moves(self, board):
        moves = [self.get_move(board, self.x + 2, self.y + 1), self.get_move(board, self.x - 1, self.y + 2),
                 self.get_move(board, self.x - 2, self.y + 1), self.get_move(board, self.x + 1, self.y - 2),
                 self.get_move(board, self.x + 2, self.y - 1), self.get_move(board, self.x + 1, self.y + 2),
                 self.get_move(board, self.x - 2, self.y - 1), self.get_move(board, self.x - 1, self.y - 2)]

        return self.remove_null_from_list(moves)

    def clone(self):
        return Knight(self.x, self.y, self.color)


class Bishop(Piece):
    PIECE_TYPE = "B"
    VALUE = 3

    def __init__(self, x, y, color):
        super(Bishop, self).__init__(x, y, color, Bishop.PIECE_TYPE, Bishop.VALUE)

    def get_possible_moves(self, board):
        return self.get_possible_diagonal_moves(board)

    def clone(self):
        return Bishop(self.x, self.y, self.color)


class Queen(Piece):
    PIECE_TYPE = "Q"
    VALUE = 9

    def __init__(self, x, y, color):
        super(Queen, self).__init__(x, y, color, Queen.PIECE_TYPE, Queen.VALUE)

    def get_possible_moves(self, board):
        diagonal = self.get_possible_diagonal_moves(board)
        horizontal = self.get_possible_horizontal_moves(board)
        return horizontal + diagonal

    def clone(self):
        return Queen(self.x, self.y, self.color)


class King(Piece):
    PIECE_TYPE = "K"
    VALUE = 35

    def __init__(self, x, y, color):
        super(King, self).__init__(x, y, color, King.PIECE_TYPE, King.VALUE)
    
    def is_starting_position(self, x):
        return x == 4

    def get_possible_moves(self, board):
        moves = [self.get_move(board, self.x + 1, self.y), self.get_move(board, self.x + 1, self.y + 1),
                 self.get_move(board, self.x, self.y + 1), self.get_move(board, self.x - 1, self.y + 1),
                 self.get_move(board, self.x - 1, self.y), self.get_move(board, self.x - 1, self.y - 1),
                 self.get_move(board, self.x, self.y - 1), self.get_move(board, self.x + 1, self.y - 1),
                 self.get_black_down_castling_move(board), self.get_black_left_castling_move(board),
                 self.get_white_up_castling_move(board), self.get_white_right_castling_move(board)]

        return self.remove_null_from_list(moves)

    def get_black_down_castling_move(self, board):
        if self.color == Piece.BLACK and board.black_king_moved:
            return 0

        piece = board.get_piece(self.x, self.y - 3)
        if piece != 0:
            if piece.color == self.color and piece.piece_type == Rook.PIECE_TYPE:
                if (board.get_piece(self.x, self.y - 1) == 0 and
                        board.get_piece(self.x, self.y - 2) == 0):
                    return ai.Move(self.x, self.y, self.x, self.y - 2, castling_move=True)
        return 0

    def get_black_left_castling_move(self, board):
        if self.color == Piece.BLACK and board.black_king_moved:
            return 0

        piece = board.get_piece(self.x - 3, self.y)
        if piece != 0:
            if piece.color == self.color and piece.piece_type == Rook.PIECE_TYPE:
                if (board.get_piece(self.x - 1, self.y) == 0 and
                        board.get_piece(self.x - 2, self.y) == 0):
                    return ai.Move(self.x, self.y, self.x - 2, self.y, castling_move=True)
        return 0

    def get_white_up_castling_move(self, board):
        if self.color == Piece.WHITE and board.white_king_moved:
            return 0
        piece = board.get_piece(self.x, self.y + 3)
        if piece != 0:
            if piece.color == self.color and piece.piece_type == Rook.PIECE_TYPE:
                if (board.get_piece(self.x, self.y + 1) == 0 and
                        board.get_piece(self.x, self.y + 2) == 0):
                    return ai.Move(self.x, self.y, self.x, self.y + 2, castling_move=True)
        return 0
    
    def get_white_right_castling_move(self, board):
        if self.color == Piece.WHITE and board.white_king_moved:
            return 0

        piece = board.get_piece(self.x + 3, self.y)
        if piece != 0:
            if piece.color == self.color and piece.piece_type == Rook.PIECE_TYPE:
                if (board.get_piece(self.x + 1, self.y) == 0 and
                        board.get_piece(self.x + 2, self.y) == 0):
                    return ai.Move(self.x, self.y, self.x + 2, self.y, castling_move=True)
        return 0

    def clone(self):
        return King(self.x, self.y, self.color)


class Pawn(Piece):
    PIECE_TYPE = "P"
    VALUE = 1

    def __init__(self, x, y, color):
        super(Pawn, self).__init__(x, y, color, Pawn.PIECE_TYPE, Pawn.VALUE)

    def is_starting_position(self, x):
        if self.color == Piece.BLACK:
            if x == 3:
                return self.y == 0
            if x == 4:
                return self.y == 1 
            if x == 5:
                return self.y == 2 or self.y == 1
            if x == 6:
                return self.y == 3 or self.y == 2
            if x == 7:
                return self.y == 4
        else:
            if x == 0:
                return self.y == 3
            if x == 1:
                return self.y == 4 or self.y == 5
            if x == 2:
                return self.y == 5 or self.y == 6
            if x == 3:
                return self.y == 6 
            if x == 4:
                return self.y == 7

    def get_possible_moves(self, board):
        moves = []

        # Direction the pawn can move in.
        direction = -1
        if self.color == Piece.BLACK:
            direction = 1

        # The general 1 step forward move.
        if board.get_piece(self.x, self.y + direction) == 0:
            moves.append(self.get_move(board, self.x, self.y + direction))
        if board.get_piece(self.x - direction, self.y) == 0:
            moves.append(self.get_move(board, self.x - direction, self.y))

        # The Pawn can take 2 steps as the first move.
        if self.is_starting_position(self.x) and board.get_piece(self.x, self.y + direction) == 0 and board.get_piece(
                self.x, self.y + direction * 2) == 0:
            moves.append(self.get_move(board, self.x, self.y + direction * 2))
        if self.is_starting_position(self.x) and board.get_piece(self.x - direction, self.y) == 0 and board.get_piece(
                self.x - direction * 2, self.y) == 0:
            moves.append(self.get_move(board, self.x - direction * 2, self.y))

        # Eating pieces.
        piece = board.get_piece(self.x + 1, self.y + direction)
        if piece != 0:
            moves.append(self.get_move(board, self.x + 1, self.y + direction))

        piece = board.get_piece(self.x - 1, self.y + direction)
        if piece != 0:
            moves.append(self.get_move(board, self.x - 1, self.y + direction))

        if self.color == Piece.WHITE:
            piece = board.get_piece(self.x + 1, self.y - direction)
            if piece != 0:
                moves.append(self.get_move(board, self.x + 1, self.y - direction))

        if self.color == Piece.BLACK:
            piece = board.get_piece(self.x - 1, self.y - direction)
            if piece != 0:
                moves.append(self.get_move(board, self.x - 1, self.y - direction))

        # en passant
        if self.color == Piece.WHITE:
            piece = board.get_piece(self.x + 1, self.y)
            if piece != 0:
                if piece.piece_type == Pawn.PIECE_TYPE:
                    if piece.color == Piece.BLACK:
                        if piece.x == board.last_move.xto and piece.y == board.last_move.yto:
                            if (board.last_move.yto - board.last_move.yfrom) == 2:
                                xy = str(self.x + 1) + str(self.y)
                                moves.append(ai.Move(self.x, self.y, self.x + 1, self.y - 1, en_passant=xy))
            piece = board.get_piece(self.x, self.y - 1)
            if piece != 0:
                if piece.piece_type == Pawn.PIECE_TYPE:
                    if piece.color == Piece.BLACK:
                        if piece.x == board.last_move.xto and piece.y == board.last_move.yto:
                            if (board.last_move.xfrom - board.last_move.xto) == 2:
                                xy = str(self.x) + str(self.y - 1)
                                moves.append(ai.Move(self.x, self.y, self.x + 1, self.y - 1, en_passant=xy))
            piece = board.get_piece(self.x - 1, self.y)
            if piece != 0:
                if piece.piece_type == Pawn.PIECE_TYPE:
                    if piece.color == Piece.BLACK:
                        if piece.x == board.last_move.xto and piece.y == board.last_move.yto:
                            if (board.last_move.yto - board.last_move.yfrom) == 2:
                                xy = str(self.x - 1) + str(self.y)
                                moves.append(ai.Move(self.x, self.y, self.x - 1, self.y - 1, en_passant=xy))
            piece = board.get_piece(self.x, self.y + 1)
            if piece != 0:
                if piece.piece_type == Pawn.PIECE_TYPE:
                    if piece.color == Piece.BLACK:
                        if piece.x == board.last_move.xto and piece.y == board.last_move.yto:
                            if (board.last_move.xfrom - board.last_move.xto) == 2:
                                xy = str(self.x) + str(self.y + 1)
                                moves.append(ai.Move(self.x, self.y, self.x + 1, self.y + 1, en_passant=xy))
            
        if self.color == Piece.BLACK:
            piece = board.get_piece(self.x - 1, self.y)
            if piece != 0:
                if piece.piece_type == Pawn.PIECE_TYPE:
                    if piece.color == Piece.WHITE:
                        if piece.x == board.last_move.xto and piece.y == board.last_move.yto:
                            if (board.last_move.yfrom - board.last_move.yto) == 2:
                                xy = str(self.x - 1) + str(self.y)
                                moves.append(ai.Move(self.x, self.y, self.x - 1, self.y + 1, en_passant=xy))
            piece = board.get_piece(self.x, self.y + 1)
            if piece != 0:
                if piece.piece_type == Pawn.PIECE_TYPE:
                    if piece.color == Piece.WHITE:
                        if piece.x == board.last_move.xto and piece.y == board.last_move.yto:
                            if (board.last_move.xto - board.last_move.xfrom) == 2:
                                xy = str(self.x) + str(self.y + 1)
                                moves.append(ai.Move(self.x, self.y, self.x - 1, self.y + 1, en_passant=xy))
            piece = board.get_piece(self.x, self.y - 1)
            if piece != 0:
                if piece.piece_type == Pawn.PIECE_TYPE:
                    if piece.color == Piece.WHITE:
                        if piece.x == board.last_move.xto and piece.y == board.last_move.yto:
                            if (board.last_move.xto - board.last_move.xfrom) == 2:
                                xy = str(self.x) + str(self.y - 1)
                                moves.append(ai.Move(self.x, self.y, self.x - 1, self.y - 1, en_passant=xy))
            piece = board.get_piece(self.x + 1, self.y)
            if piece != 0:
                if piece.piece_type == Pawn.PIECE_TYPE:
                    if piece.color == Piece.WHITE:
                        if piece.x == board.last_move.xto and piece.y == board.last_move.yto:
                            if (board.last_move.yfrom - board.last_move.yto) == 2:
                                xy = str(self.x + 1) + str(self.y)
                                moves.append(ai.Move(self.x, self.y, self.x + 1, self.y + 1, en_passant=xy))

        return self.remove_null_from_list(moves)

    def clone(self):
        return Pawn(self.x, self.y, self.color)
