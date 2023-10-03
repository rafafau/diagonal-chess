from PyQt5.QtWidgets import QApplication

import ai

import board
import gui
import pieces
import sys


def get_user_move(move):
    if move == "" or len(move) != 4:
        return 1
    else:
        xfrom = letter2pos(move[0:1])
        yfrom = 8 - int(move[1:2])
        xto = letter2pos(move[2:3])
        yto = 8 - int(move[3:4])
        return ai.Move(xfrom, yfrom, xto, yto)

def get_valid_move(board, move_str, color):
    global mv_from_to
    mov = get_user_move(move_str)
    valid = False
    if color == "white":
        possible_moves = board.get_possible_moves(pieces.Piece.WHITE)
        if board.is_checked(pieces.Piece.WHITE):
            possible_moves = board.delete_checked_moves(possible_moves, pieces.Piece.WHITE)
            if possible_moves == []:
                return 2
    elif color == "black":
        possible_moves = board.get_possible_moves(pieces.Piece.BLACK)
        if board.is_checked(pieces.Piece.BLACK):
            possible_moves = board.delete_checked_moves(possible_moves, pieces.Piece.BLACK)
            if possible_moves == []:
                return 2
    else:
        return 1
    if mov == 1:
        return 1


    for possible_move in possible_moves:
        if mov.equals(possible_move):
            mov.castling_move = possible_move.castling_move
            mov.en_passant = possible_move.en_passant
            valid = True

    if not valid:
        return 1

    return mov


def is_won(color: str) -> bool:

    if color == "black":
        if chess_board.is_checked(pieces.Piece.WHITE):
            return True
    if color == "white":
        if chess_board.is_checked(pieces.Piece.BLACK):
            return True

    return False


def letter2pos(letter):
    try:
        return {
            'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7,
        }[letter]
    except TypeError:
        TypeError("Niepoprawna zmienna, powinien być string")
    except KeyError:
        KeyError("Niepoprawna litera")


def pos2letter(number):
    try:
        return {
            0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H',
        }[number]
    except TypeError:
        TypeError("Niepoprawna zmienna, powinien być string")
    except KeyError:
        KeyError("Niepoprawna litera")


def piece_icon(piece):
    if piece == "WP":
        return "background-image:url(image/w_pawn.svg)"
    if piece == "WR":
        return "background-image:url(image/w_rook.svg)"
    if piece == "WN":
        return "background-image:url(image/w_knight.svg)"
    if piece == "WB":
        return "background-image:url(image/w_bishop.svg)"
    if piece == "WQ":
        return "background-image:url(image/w_queen.svg)"
    if piece == "WK":
        return "background-image:url(image/w_king.svg)"

    if piece == "BP":
        return "background-image:url(image/b_pawn.svg)"
    if piece == "BR":
        return "background-image:url(image/b_rook.svg)"
    if piece == "BN":
        return "background-image:url(image/b_knight.svg)"
    if piece == "BB":
        return "background-image:url(image/b_bishop.svg)"
    if piece == "BQ":
        return "background-image:url(image/b_queen.svg)"
    if piece == "BK":
        return "background-image:url(image/b_king.svg)"


def get_chess_board():
    return chess_board


chess_board = board.Board.new()
is_black_turn = False
white_player = "player"
black_player = "player"
mv_from_to = "C3C5"
count_pieces = chess_board.get_count_of_pieces()
last_count = count_pieces
repeat_count = 0
hash_move_array = []
game_depth = 0

def new_game():
    global chess_board, is_black_turn, end_game, count_pieces, last_count, repeat_count, hash_move_array, game_depth
    chess_board = board.Board.new()
    is_black_turn = False
    end_game = False
    count_pieces = chess_board.get_count_of_pieces()
    last_count = count_pieces
    repeat_count = 0
    game_depth = 0
    hash_move_array = []

def is_3_move_repetition():
    global hash_move_array, chess_board, is_black_turn
    last_hash = chess_board.get_hash_board_to_drawn(is_black_turn)
    count = 0
    for hash in hash_move_array:
        if hash == last_hash:
            count += 1
    if count == 3:
        return True
    return False

def check_if_drawn(last_hash):
    global hash_move_array
    count = 0
    for hash in hash_move_array:
        if hash == last_hash:
            count += 1
    if count == 3:
        return True
    return False

def is_50_move_rule():
    global chess_board, count_pieces, last_count, repeat_count
    count_pieces = chess_board.get_count_of_pieces()
    if count_pieces == 2:
        return True
    if count_pieces == last_count:
        repeat_count += 1
        if repeat_count == 50:
            return True
    else:
        repeat_count = 0
        last_count = count_pieces

def is_drawn():
    if is_3_move_repetition():
        return True
    if is_50_move_rule():
        return True
    return False

def main():
    pychess = QApplication(sys.argv)
    view = gui.PyChessUi()
    view.show()
    gui.PyChessCtrl(view=view)
    sys.exit(pychess.exec_())


if __name__ == '__main__':
    main()
