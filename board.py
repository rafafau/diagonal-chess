import pieces
import numpy as np
import hashlib


class Board:
    w = 8
    h = 8

    def __init__(self, chesspieces, white_king_moved=False, black_king_moved=False):
        self.chesspieces = chesspieces
        self.white_king_moved = white_king_moved
        self.black_king_moved = black_king_moved
        self.last_move = None

    @classmethod
    def clone(cls, chessboard):
        chesspieces = np.zeros((Board.w, Board.h), dtype=pieces.Piece)
        for x in range(Board.w):
            for y in range(Board.h):
                piece = chessboard.chesspieces[x][y]
                if piece != 0:
                    chesspieces[x][y] = piece.clone()
        return cls(chesspieces, chessboard.white_king_moved, chessboard.black_king_moved)

    @classmethod
    def new(cls):
        chess_pieces = np.zeros((Board.w, Board.h), dtype=pieces.Piece)
        # Create white pawns
        for x in range(0, 5):
            chess_pieces[x][x + 3] = pieces.Pawn(x, x + 3, pieces.Piece.WHITE)

        chess_pieces[Board.w - 7][Board.h - 3] = pieces.Pawn(1, 5, pieces.Piece.WHITE)
        chess_pieces[Board.w - 6][6] = pieces.Pawn(2, 6, pieces.Piece.WHITE)

        # Create black pawns
        for x in range(3, 8):
            chess_pieces[x][x - 3] = pieces.Pawn(x, x - 3, pieces.Piece.BLACK)

        chess_pieces[5][1] = pieces.Pawn(5, 1, pieces.Piece.BLACK)
        chess_pieces[6][2] = pieces.Pawn(6, 2, pieces.Piece.BLACK)

        # Create white rooks
        chess_pieces[0][4] = pieces.Rook(0, 4, pieces.Piece.WHITE)
        chess_pieces[3][7] = pieces.Rook(3, 7, pieces.Piece.WHITE)

        # Create black rooks
        chess_pieces[4][0] = pieces.Rook(4, 0, pieces.Piece.BLACK)
        chess_pieces[Board.w - 1][3] = pieces.Rook(Board.w - 1, 3, pieces.Piece.BLACK)

        # Create white Knights
        chess_pieces[0][6] = pieces.Knight(0, 6, pieces.Piece.WHITE)
        chess_pieces[2][7] = pieces.Knight(2, 7, pieces.Piece.WHITE)

        # Create black Knights
        chess_pieces[5][0] = pieces.Knight(5, 0, pieces.Piece.BLACK)
        chess_pieces[7][1] = pieces.Knight(7, 1, pieces.Piece.BLACK)

        # Create white Bishops
        chess_pieces[0][5] = pieces.Bishop(0, 5, pieces.Piece.WHITE)
        chess_pieces[1][Board.h - 1] = pieces.Bishop(1, Board.h - 1, pieces.Piece.WHITE)

        # Create black Bishops
        chess_pieces[6][0] = pieces.Bishop(6, 0, pieces.Piece.BLACK)
        chess_pieces[7][2] = pieces.Bishop(7, 2, pieces.Piece.BLACK)

        # Create white King & Queen
        chess_pieces[0][7] = pieces.King(0, 7, pieces.Piece.WHITE)
        chess_pieces[1][6] = pieces.Queen(1, 6, pieces.Piece.WHITE)

        # Create white King & Queen
        chess_pieces[7][0] = pieces.King(7, 0, pieces.Piece.BLACK)
        chess_pieces[6][1] = pieces.Queen(6, 1, pieces.Piece.BLACK)

        return cls(chess_pieces, False, False)

    def get_possible_moves(self, color):
        moves = np.array([])
        for x in range(Board.w):
            for y in range(Board.h):
                piece = self.chesspieces[x][y]
                if piece != 0 and piece.color == color:
                    moves = np.append(moves, piece.get_possible_moves(self))
        return moves

    def perform_move(self, move):
        if move is not int:
            piece = self.chesspieces[move.xfrom][move.yfrom]
        else:
            piece = 0
        self.last_move = move
        if piece != 0:
            piece.x = move.xto
            piece.y = move.yto
            self.chesspieces[move.xto][move.yto] = piece
            self.chesspieces[move.xfrom][move.yfrom] = 0

            # zamiana pionka na inna figure
            if piece.piece_type == pieces.Pawn.PIECE_TYPE:
                if piece.y == 0 and piece.x > 3 and piece.color == pieces.Piece.WHITE:
                    if self.get_queen(piece.color) == 0:
                        self.chesspieces[piece.x][piece.y] = pieces.Queen(piece.x, piece.y, piece.color)
                    elif self.get_rook(piece.color) == 0:
                        self.chesspieces[piece.x][piece.y] = pieces.Rook(piece.x, piece.y, piece.color)
                    elif self.get_bishop(piece.color) == 0:
                        self.chesspieces[piece.x][piece.y] = pieces.Bishop(piece.x, piece.y, piece.color)
                    else:
                        self.chesspieces[piece.x][piece.y] = pieces.Knight(piece.x, piece.y, piece.color)
                elif piece.x == 7 and piece.y <= 3 and piece.color == pieces.Piece.WHITE:
                    if self.get_queen(piece.color) == 0:
                        self.chesspieces[piece.x][piece.y] = pieces.Queen(piece.x, piece.y, piece.color)
                    elif self.get_rook(piece.color) == 0:
                        self.chesspieces[piece.x][piece.y] = pieces.Rook(piece.x, piece.y, piece.color)
                    elif self.get_bishop(piece.color) == 0:
                        self.chesspieces[piece.x][piece.y] = pieces.Bishop(piece.x, piece.y, piece.color)
                    else:
                        self.chesspieces[piece.x][piece.y] = pieces.Knight(piece.x, piece.y, piece.color)
                elif piece.y == 7 and piece.x <= 3 and piece.color == pieces.Piece.BLACK:
                    if self.get_queen(piece.color) == 0:
                        self.chesspieces[piece.x][piece.y] = pieces.Queen(piece.x, piece.y, piece.color)
                    elif self.get_rook(piece.color) == 0:
                        self.chesspieces[piece.x][piece.y] = pieces.Rook(piece.x, piece.y, piece.color)
                    elif self.get_bishop(piece.color) == 0:
                        self.chesspieces[piece.x][piece.y] = pieces.Bishop(piece.x, piece.y, piece.color)
                    else:
                        self.chesspieces[piece.x][piece.y] = pieces.Knight(piece.x, piece.y, piece.color)
                elif piece.x == 0 and piece.y > 3 and piece.color == pieces.Piece.BLACK:
                    if self.get_queen(piece.color) == 0:
                        self.chesspieces[piece.x][piece.y] = pieces.Queen(piece.x, piece.y, piece.color)
                    elif self.get_rook(piece.color) == 0:
                        self.chesspieces[piece.x][piece.y] = pieces.Rook(piece.x, piece.y, piece.color)
                    elif self.get_bishop(piece.color) == 0:
                        self.chesspieces[piece.x][piece.y] = pieces.Bishop(piece.x, piece.y, piece.color)
                    else:
                        self.chesspieces[piece.x][piece.y] = pieces.Knight(piece.x, piece.y, piece.color)

            if move.en_passant != "":
                self.chesspieces[int(move.en_passant[:1])][int(move.en_passant[1:])] = 0

            if move.castling_move:
                if move.yfrom > move.yto:
                    rook = self.chesspieces[0][move.yto - 1]
                    if rook != 0:
                        rook.y = move.yto + 1
                        self.chesspieces[0][move.yto + 1] = rook
                        self.chesspieces[0][move.yto - 1] = 0
                if move.xfrom < move.xto:
                    rook = self.chesspieces[move.xto + 1][Board.h - 1]
                    if rook != 0:
                        rook.x = move.xto + 1
                        self.chesspieces[move.xto - 1][Board.h - 1] = rook
                        self.chesspieces[move.xto + 1][Board.h - 1] = 0
                if move.yfrom < move.yto:
                    rook = self.chesspieces[Board.w - 1][move.yto + 1]
                    if rook != 0:
                        rook.y = move.yto - 1
                        self.chesspieces[Board.w - 1][move.yto - 1] = rook
                        self.chesspieces[Board.w - 1][move.yto + 1] = 0
                if move.xfrom > move.xto:
                    rook = self.chesspieces[move.xto - 1][0]
                    if rook != 0:
                        rook.x = move.xto - 1
                        self.chesspieces[move.xto + 1][0] = rook
                        self.chesspieces[move.xto - 1][0] = 0    

            if piece.piece_type == pieces.King.PIECE_TYPE:
                if piece.color == pieces.Piece.WHITE:
                    self.white_king_moved = True
                else:
                    self.black_king_moved = True


    # Returns if the given color is checked.
    def is_checked(self, color):
        king = self.get_king(color)
        if king == 0:
            return False
        if color == pieces.Piece.WHITE:
            moves = self.get_possible_moves(pieces.Piece.BLACK)
        else:
            moves = self.get_possible_moves(pieces.Piece.WHITE)
        for move in moves:
            if move.xto == king.x and move.yto == king.y:
                return True
        return False

    def get_king(self, color):
        for x in range(Board.w):
            for y in range(Board.h):
                piece = self.chesspieces[x][y]
                if piece != 0 and piece.piece_type == pieces.King.PIECE_TYPE and piece.color == color:
                    return piece
        return 0
    
    def get_queen(self, color):
        for x in range(Board.w):
            for y in range(Board.h):
                piece = self.chesspieces[x][y]
                if piece != 0 and piece.piece_type == pieces.Queen.PIECE_TYPE and piece.color == color:
                    return piece
        return 0

    def get_rook(self, color):
        count = 0
        for x in range(Board.w):
            for y in range(Board.h):
                piece = self.chesspieces[x][y]
                if piece != 0 and piece.piece_type == pieces.Rook.PIECE_TYPE and piece.color == color:
                    count += 1
                    if count == 2:
                        return piece
        return 0

    def get_bishop(self, color):
        count = 0
        for x in range(Board.w):
            for y in range(Board.h):
                piece = self.chesspieces[x][y]
                if piece != 0 and piece.piece_type == pieces.Bishop.PIECE_TYPE and piece.color == color:
                    count += 1
                    if count == 2:
                        return piece
        return 0

    def get_piece(self, x, y):
        if not self.in_bounds(x, y):
            return 0

        return self.chesspieces[x][y]

    def get_count_of_pieces(self):
        count = 0
        for x in range(Board.w):
            for y in range(Board.h):
                if self.chesspieces[x][y] != 0:
                    count += 1
        return count

    def is_capture(self, move):
        return self.get_piece(move.xto, move.yto) != 0

    def delete_checked_moves(self, moves, color):
        new_moves = np.array([])
        for move in moves:
            clone = self.clone(self)
            clone.perform_move(move)
            if not clone.is_checked(color):
                new_moves = np.append(new_moves, move)
        return new_moves

    def get_hash_board(self, maximazing_player, depth=0):
        count_pieces = self.get_count_of_pieces()
        pieces = 0
        key = list()
        if maximazing_player:
            key.append("1")
        else:
            key.append("0")
        for x in range(Board.w):
            for y in range(Board.h):
                piece = self.chesspieces[x][y]
                if piece != 0:
                    pieces += 1
                    key.append(str([piece.piece_type, piece.color, piece.x, piece.y]))
                    if pieces == count_pieces:
                        break
                else:
                    key.append("0")
        key.append(str(depth))
        key = "".join(key)
        return int(hashlib.sha256(key.encode('utf-8')).hexdigest(), 16) % 10**18
    
    def get_hash_board_to_drawn(self, maximazing_player):
        count_pieces = self.get_count_of_pieces()
        pieces = 0
        key = list()
        if maximazing_player:
            key.append("1")
        else:
            key.append("0")
        for x in range(Board.w):
            for y in range(Board.h):
                piece = self.chesspieces[x][y]
                if piece != 0:
                    pieces += 1
                    key.append(str([piece.piece_type, piece.color, piece.x, piece.y]))
                    if pieces == count_pieces:
                        break
                else:
                    key.append("0")
        key = "".join(key)
        key = int(hashlib.sha256(key.encode('utf-8')).hexdigest(), 16) % 10**16
        return str(key)

    def in_bounds(self, x, y):
        return 0 <= x < Board.w and 0 <= y < Board.h
        
    def piece_number(piece):
        if piece == "WP":
            return 0
        if piece == "WR":
            return 1
        if piece == "WN":
            return 2
        if piece == "WB":
            return 3
        if piece == "WQ":
            return 4
        if piece == "WK":
            return 5
        if piece == "BP":
            return 6
        if piece == "BR":
            return 7
        if piece == "BN":
            return 8
        if piece == "BB":
            return 9
        if piece == "BQ":
            return 10
        if piece == "BK":
            return 11
    
    def split_dims(self, chessboard, maximazing_player):
        board3d = np.zeros((17, 8, 8), dtype=np.float32)

        for i in range(8):
            for j in range(8):
                piece = chessboard.get_piece(i, j)
                if piece != 0:
                    piece_index = Board.piece_number(piece.to_string())
                    board3d[piece_index][i][j] = 1
    
        possible_moves = chessboard.get_possible_moves(pieces.Piece.WHITE)
        for move in possible_moves:
            i = int(move.to_string()[3])
            j = int(move.to_string()[2])
            board3d[12][i][j] = 1
   
        possible_moves = chessboard.get_possible_moves(pieces.Piece.BLACK)
        for move in possible_moves:
            i = int(move.to_string()[3])
            j = int(move.to_string()[2])
            board3d[13][i][j] = 1

        if self.last_move != None:
            i = int(self.last_move.yfrom)
            j = int(self.last_move.xfrom)
            
            board3d[14][i][j] = 1
            i = int(self.last_move.yto)
            j = int(self.last_move.xto)
            board3d[15][i][j] = 1
        else:
            board3d[14][0][0] = 0
            board3d[15][0][0] = 0

        if maximazing_player:
            board3d[16][0][0] = 1
        else:
            board3d[16][0][0] = 0

        return board3d