import board
import numpy as np
import pieces
import main

import sqlite3
from tensorflow.keras import models

class Heuristics:

    WPAWN_TABLE = np.array([
        [0, 0, 1, 2, 0, 0, 0, 0],
        [0, 0, 0, 1, 2, 2, 2, 0],
        [0, 0, 0, 0, 1, 1, 2, 0],
        [0, 0, 0, 0, 0, 1, 2, 0],
        [0, 0, 0, 0, 0, 0, 1, 2],
        [0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ])

    BPAWN_TABLE = np.array([
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0],
        [2, 1, 0, 0, 0, 0, 0, 0],
        [0, 2, 1, 0, 0, 0, 0, 0],
        [0, 2, 1, 1, 0, 0, 0, 0],
        [0, 2, 2, 2, 1, 0, 0, 0],
        [0, 0, 0, 0, 2, 1, 0, 0],
    ])

    @staticmethod
    def evaluate(board):
        material = Heuristics.get_material_score(board)

        w_pawns = Heuristics.get_piece_position_score(board, pieces.Pawn.PIECE_TYPE, Heuristics.WPAWN_TABLE, pieces.Piece.WHITE)
        b_pawns = Heuristics.get_piece_position_score(board, pieces.Pawn.PIECE_TYPE, Heuristics.BPAWN_TABLE, pieces.Piece.BLACK)

        if board.is_checked(pieces.Piece.WHITE):
            return material - 5 + w_pawns + b_pawns
        if board.is_checked(pieces.Piece.BLACK):
            return material + 5 + w_pawns + b_pawns

        return material + w_pawns + b_pawns

    @staticmethod
    def get_piece_position_score(board, piece_type, table, color=pieces.Piece.WHITE):
        score = 0
        for x in range(8):
            for y in range(8):
                piece = board.chesspieces[x][y]
                if piece != 0:
                    if piece.piece_type == piece_type and color == pieces.Piece.WHITE:
                        score += table[x][y]
                    elif piece.piece_type == piece_type and color == pieces.Piece.BLACK:
                        score -= table[x][y]
        return score

    @staticmethod
    def get_material_score(board):
        white = 0
        black = 0
        for x in range(8):
            for y in range(8):
                piece = board.chesspieces[x][y]
                if piece != 0:
                    if piece.color == pieces.Piece.WHITE:
                        white += piece.value
                    else:
                        black += piece.value

        return white - black        
        

count_moves = 0
deep = 3
game_deep = 0
max_deep = 0
model = models.load_model('model.h5')

# Create a SQLite database connection
conn = sqlite3.connect('chessboard.db')
cursor = conn.cursor()

# Create a table to store chessboard positions and their scores
cursor.execute('''
    CREATE TABLE IF NOT EXISTS chessboard_positions (
        position_hash TEXT PRIMARY KEY,
        score INTEGER
    )
''')
conn.commit()

def store_position_hash(hash_board, score):
    if score >= 100000 or score <= -100000:
        return
    else:
        score = int(score)
        cursor.execute('INSERT OR REPLACE INTO chessboard_positions (position_hash, score) VALUES (?, ?)', (hash_board, score))
        conn.commit()

def get_position_score(hash_board):
    cursor.execute('SELECT score FROM chessboard_positions WHERE position_hash = ?', (hash_board,))
    result = cursor.fetchone()
    if result:
        return int(result[0])
    return None

class AI:

    @staticmethod
    def get_ai_move(chessboard, color):
        global count_moves, deep, game_deep, max_deep
        count_moves = 0
        best_move = 0
        max_deep = deep

        if color == "white":
            pieces_color = pieces.Piece.WHITE
            best_score = -np.Inf
            possible_moves = chessboard.get_possible_moves(pieces_color)
            if chessboard.is_checked(pieces_color):
                possible_moves = chessboard.delete_checked_moves(possible_moves, pieces_color)
                if len(possible_moves) == 0:
                    return 0, 0, 0, 0
            possible_moves = AI.sort_moves_ai(possible_moves, chessboard, maximizing=True)
            for move in possible_moves:
                count_moves += 1
                copy = board.Board.clone(chessboard)
                copy.perform_move(move)
                hash_board = copy.get_hash_board(maximazing_player=True, depth=game_deep)
                cached_score = get_position_score(hash_board)
                if cached_score is not None:
                    if cached_score > best_score:
                        best_score = cached_score
                        best_move = move
                else:
                    score = AI.alphabeta(copy, deep - 1, -np.inf, np.inf, False)
                    if score > best_score:
                        store_position_hash(hash_board, score)    #dodatkowy
                        best_score = score
                        best_move = move
        else:
            best_score = np.Inf
            pieces_color = pieces.Piece.BLACK
            possible_moves = chessboard.get_possible_moves(pieces_color)
            if chessboard.is_checked(pieces_color):
                possible_moves = chessboard.delete_checked_moves(possible_moves, pieces_color)
                if len(possible_moves) == 0:
                    return 0, 0, 0, 0
            possible_moves = AI.sort_moves_ai(possible_moves, chessboard, maximizing=False)
            for move in possible_moves:
                count_moves += 1
                copy = board.Board.clone(chessboard)
                copy.perform_move(move)
                hash_board = copy.get_hash_board(maximazing_player=False, depth=game_deep)
                cached_score = get_position_score(hash_board)
                if cached_score is not None:
                    if cached_score < best_score:
                        best_score = cached_score
                        best_move = move
                else:
                    score = AI.alphabeta(copy, deep - 1, -np.inf, np.inf, True)
                    if score < best_score:
                        store_position_hash(hash_board, score)   #dodatkowy
                        best_score = score
                        best_move = move

        copy = board.Board.clone(chessboard)
        copy.perform_move(best_move)
        game_deep += 2
        return best_move, int(best_score), count_moves, max_deep

    @staticmethod
    def alphabeta(chessboard, depth, a, b, maximizing):
        global count_moves, deep, game_deep

        count_moves += 1
        if count_moves % 1000 == 0:
            print(count_moves)

        if depth == 0:
            return AI.quiesce(chessboard, a, b, maximizing)

        if maximizing:
            best_score = -np.inf
            possible_moves = chessboard.get_possible_moves(pieces.Piece.WHITE)
            if chessboard.is_checked(pieces.Piece.WHITE):
                possible_moves = chessboard.delete_checked_moves(possible_moves, pieces.Piece.WHITE)
                if len(possible_moves) == 0:
                    return 0
            possible_moves = AI.sort_moves(possible_moves, chessboard, maximizing=True)
            for move in possible_moves:
                copy = board.Board.clone(chessboard)
                copy.perform_move(move)
                hash_board = copy.get_hash_board(maximazing_player=True, depth=deep - depth + game_deep)
                cached_score = get_position_score(hash_board)
                if cached_score is not None:
                    best_score = max(best_score, cached_score)
                    a = max(a, best_score)
                    if b <= a:
                        break
                else:
                    score = AI.alphabeta(copy, depth - 1, a, b, False)
                    best_score = max(best_score, score)
                    a = max(a, best_score)
                    if b <= a:
                        break
                    else:
                        curr_depth = deep - depth + game_deep
                        store_position_hash(hash_board, score)
        else:
            best_score = np.inf
            possible_moves = chessboard.get_possible_moves(pieces.Piece.BLACK)
            if chessboard.is_checked(pieces.Piece.BLACK):
                possible_moves = chessboard.delete_checked_moves(possible_moves, pieces.Piece.BLACK)
                if len(possible_moves) == 0:
                    return 0
            possible_moves = AI.sort_moves(possible_moves, chessboard, maximizing=False)
            for move in possible_moves:
                copy = board.Board.clone(chessboard)
                copy.perform_move(move)

                hash_board = copy.get_hash_board(maximazing_player=False, depth=deep - depth + game_deep)
                cached_score = get_position_score(hash_board)
                if cached_score is not None:
                    best_score = min(best_score, cached_score)
                    b = min(b, best_score)
                    if b <= a:
                        break
                else:
                    score = AI.alphabeta(copy, depth - 1, a, b, True)
                    best_score = min(best_score, score)
                    b = min(b, best_score)
                    if b <= a:
                        break
                    else:
                        curr_depth = deep - depth + game_deep
                        store_position_hash(hash_board, score)
        return best_score

    @staticmethod
    def quiesce(chessboard, alpha, beta, maximizing, depth=0):
        global count_moves, deep, game_deep, max_deep

        count_moves += 1
        if count_moves % 1000 == 0:
            print(count_moves)
        stand_pat = Heuristics.evaluate(chessboard)
        if maximizing:
            if stand_pat >= beta:
                return beta
            if alpha < stand_pat:
                alpha = stand_pat
            possible_moves = chessboard.get_possible_moves(pieces.Piece.WHITE)
            if chessboard.is_checked(pieces.Piece.WHITE):
                possible_moves = chessboard.delete_checked_moves(possible_moves, pieces.Piece.WHITE)
                if len(possible_moves) == 0:
                    return 0
            possible_moves = AI.sort_moves_quiesce(possible_moves, chessboard)
            for move in possible_moves:
                copy = board.Board.clone(chessboard)
                copy.perform_move(move)
                max_deep = max(max_deep, deep + depth)
                hash_board = copy.get_hash_board(maximazing_player=True, depth=deep + depth + game_deep)
                cached_score = get_position_score(hash_board)
                if cached_score is not None:
                    alpha = max(alpha, cached_score)
                    if alpha >= beta:
                        break
                else:
                    score = AI.quiesce(copy, alpha, beta, False, depth + 1)
                    alpha = max(alpha, score)
                    if alpha >= beta:
                        break
                    else:
                        curr_depth = deep + depth + game_deep
                        store_position_hash(hash_board, score)
            return alpha
        else:
            if stand_pat <= alpha:
                return alpha
            if beta > stand_pat:
                beta = stand_pat
            possible_moves = chessboard.get_possible_moves(pieces.Piece.BLACK)
            if chessboard.is_checked(pieces.Piece.BLACK):
                possible_moves = chessboard.delete_checked_moves(possible_moves, pieces.Piece.BLACK)
                if len(possible_moves) == 0:
                    return 0
            possible_moves = AI.sort_moves_quiesce(possible_moves, chessboard)
            for move in possible_moves:
                copy = board.Board.clone(chessboard)
                copy.perform_move(move)
                max_deep = max(max_deep, deep + depth)
                hash_board = copy.get_hash_board(maximazing_player=False, depth=deep + depth + game_deep)
                cached_score = get_position_score(hash_board)
                if cached_score is not None:
                    beta = min(beta, cached_score)
                    if beta <= alpha:
                        break
                else:
                    score = AI.quiesce(copy, alpha, beta, True, depth + 1)
                    beta = min(beta, score)
                    if score <= alpha:
                        break
                    else:
                        curr_depth = deep + depth + game_deep
                        store_position_hash(hash_board, score)
            return beta

    @staticmethod
    def sort_moves_ai(moves, chessboard, maximizing):
        for move in moves:
            copy = board.Board.clone(chessboard)
            copy.perform_move(move)
            move.score = np.array(AI.minimax_eval(copy, maximizing), dtype=np.float32)
        if maximizing:
            moves = sorted(moves, key=lambda move: move.score, reverse=True)
        else:
            moves = sorted(moves, key=lambda move: move.score)
        return moves
    
    @staticmethod
    def sort_moves(moves, chessboard, maximizing):
        for move in moves:
            copy = board.Board.clone(chessboard)
            copy.perform_move(move)
            if not chessboard.is_capture(move):
                move.score = 0
            else:
                move.score = Heuristics.get_material_score(copy)
        if maximizing:
            moves = sorted(moves, key=lambda move: move.score, reverse=True)
        else:
            moves = sorted(moves, key=lambda move: move.score)
        return moves
    
    @staticmethod
    def sort_moves_quiesce(moves, chessboard):
        for move in moves:
            copy = board.Board.clone(chessboard)
            copy.perform_move(move)
            if not chessboard.is_capture(move):
                moves = np.delete(moves, np.where(moves == move))
            else:
                piece_from = chessboard.get_piece(move.xfrom, move.yfrom)
                piece_to = chessboard.get_piece(move.xto, move.yto)
                if piece_from != 0 and piece_to != 0:
                    move.score =  piece_from.value - piece_to.value
                else:
                    move.score = 0
        moves = sorted(moves, key=lambda move: move.score)
        return moves

    @staticmethod
    def minimax_eval(chessboard, maximizing=True):
        global model
        board3d = chessboard.split_dims(chessboard, maximizing)
        board3d = np.expand_dims(board3d, 0)
        return model(board3d)[0][0]

class Move:

    def __init__(self, xfrom, yfrom, xto, yto, castling_move=False, en_passant=""):
        self.xfrom = xfrom
        self.yfrom = yfrom
        self.xto = xto
        self.yto = yto
        self.castling_move = castling_move
        self.score = None
        self.en_passant = en_passant

    def equals(self, other_move):
        return self.xfrom == other_move.xfrom and self.yfrom == other_move.yfrom and \
               self.xto == other_move.xto and self.yto == other_move.yto

    def to_string(self):
        return str(self.xfrom) + str(self.yfrom) + str(self.xto) + str(self.yto)
