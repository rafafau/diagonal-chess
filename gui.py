import time
from functools import partial
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout, QLabel, QComboBox
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QMessageBox

import ai
import main


class PyChessUi(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Diagonal Chess AI")
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        self._createLabels()
        self._createBox()
        self._createResetButton()
        self._createBoard()
        self._createStats()
        self._createDisplayStats()
        self._createStats2()
        self._createDisplayStats2()

    def _createLabels(self):
        self.labels = {}
        labelsLayout = QGridLayout()
        labels = {"Białe": (0, 0), "Czarne": (0, 1)}
        for labelText, pos in labels.items():
            self.labels[labelText] = QLabel(labelText)
            self.labels[labelText].setAlignment(Qt.AlignCenter)
            labelsLayout.addWidget(self.labels[labelText], pos[0], pos[1])
        self.generalLayout.addLayout(labelsLayout)

    def _createBox(self):
        self.cb_white = QComboBox()
        self.cb_white.addItems(["Gracz", "AI"])
        self.cb_white.currentIndexChanged.connect(self.change_white_player)
        self.cb_black = QComboBox()
        self.cb_black.addItems(["Gracz 2", "AI 2"])
        self.cb_black.currentIndexChanged.connect(self.change_black_player)
        box_layout = QGridLayout()
        box_layout.addWidget(self.cb_white, 0, 0)
        box_layout.addWidget(self.cb_black, 0, 1)
        self.generalLayout.addLayout(box_layout)

    def change_white_player(self, i):
        if i == 0:
            main.white_player = "player"
        else:
            main.white_player = "ai"

    def change_black_player(self, i):
        if i == 0:
            main.black_player = "player"
        else:
            main.black_player = "ai"

    def _createResetButton(self):
        self.reset_button = QPushButton('Nowa Gra', self)
        self.reset_button.clicked.connect(self.new_game) 
        self.generalLayout.addWidget(self.reset_button)

    def new_game(self):
        main.new_game()
        self.clear_highlight()

    def show_endgame_message(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(message)
        msg.setWindowTitle("Koniec gry")
        msg.setStandardButtons(QMessageBox.Ok)
        retval = msg.exec_()
        

    def _createBoard(self):
        self.buttons = {}
        buttonsLayout = QGridLayout()
        buttons = {
            "A8": (0, 0), "B8": (0, 1), "C8": (0, 2), "D8": (0, 3), "E8": (0, 4), "F8": (0, 5), "G8": (0, 6),
            "H8": (0, 7),
            "A7": (1, 0), "B7": (1, 1), "C7": (1, 2), "D7": (1, 3), "E7": (1, 4), "F7": (1, 5), "G7": (1, 6),
            "H7": (1, 7),
            "A6": (2, 0), "B6": (2, 1), "C6": (2, 2), "D6": (2, 3), "E6": (2, 4), "F6": (2, 5), "G6": (2, 6),
            "H6": (2, 7),
            "A5": (3, 0), "B5": (3, 1), "C5": (3, 2), "D5": (3, 3), "E5": (3, 4), "F5": (3, 5), "G5": (3, 6),
            "H5": (3, 7),
            "A4": (4, 0), "B4": (4, 1), "C4": (4, 2), "D4": (4, 3), "E4": (4, 4), "F4": (4, 5), "G4": (4, 6),
            "H4": (4, 7),
            "A3": (5, 0), "B3": (5, 1), "C3": (5, 2), "D3": (5, 3), "E3": (5, 4), "F3": (5, 5), "G3": (5, 6),
            "H3": (5, 7),
            "A2": (6, 0), "B2": (6, 1), "C2": (6, 2), "D2": (6, 3), "E2": (6, 4), "F2": (6, 5), "G2": (6, 6),
            "H2": (6, 7),
            "A1": (7, 0), "B1": (7, 1), "C1": (7, 2), "D1": (7, 3), "E1": (7, 4), "F1": (7, 5), "G1": (7, 6),
            "H1": (7, 7),
        }

        i = 1
        j = 1
        for btnText, pos in buttons.items():
            self.buttons[btnText] = QPushButton(btnText)
            self.buttons[btnText].setFixedSize(60, 60)
            self.update_icon(btnText)
            if i / j == 8:
                j += 1
            i += 1

            buttonsLayout.addWidget(self.buttons[btnText], pos[0], pos[1])

        # czarne pionki
        self.update_icon("D8", "background-image:url(image/b_pawn.svg)")
        self.update_icon("E7", "background-image:url(image/b_pawn.svg)")
        self.update_icon("F6", "background-image:url(image/b_pawn.svg)")
        self.update_icon("G5", "background-image:url(image/b_pawn.svg)")
        self.update_icon("H4", "background-image:url(image/b_pawn.svg)")
        self.update_icon("F7", "background-image:url(image/b_pawn.svg)")
        self.update_icon("G6", "background-image:url(image/b_pawn.svg)")
        self.update_icon("E8", "background-image:url(image/b_rook.svg)")
        self.update_icon("H5", "background-image:url(image/b_rook.svg)")
        self.update_icon("G7", "background-image:url(image/b_queen.svg)")
        self.update_icon("H8", "background-image:url(image/b_king.svg)")
        self.update_icon("H6", "background-image:url(image/b_bishop.svg)")
        self.update_icon("G8", "background-image:url(image/b_bishop.svg)")
        self.update_icon("F8", "background-image:url(image/b_knight.svg)")
        self.update_icon("H7", "background-image:url(image/b_knight.svg)")

        # biale pionki
        self.update_icon("A5", "background-image:url(image/w_pawn.svg)")
        self.update_icon("B4", "background-image:url(image/w_pawn.svg)")
        self.update_icon("C3", "background-image:url(image/w_pawn.svg)")
        self.update_icon("D2", "background-image:url(image/w_pawn.svg)")
        self.update_icon("E1", "background-image:url(image/w_pawn.svg)")
        self.update_icon("C2", "background-image:url(image/w_pawn.svg)")
        self.update_icon("B3", "background-image:url(image/w_pawn.svg)")
        self.update_icon("A4", "background-image:url(image/w_rook.svg)")
        self.update_icon("D1", "background-image:url(image/w_rook.svg)")
        self.update_icon("B2", "background-image:url(image/w_queen.svg)")
        self.update_icon("A1", "background-image:url(image/w_king.svg)")
        self.update_icon("A3", "background-image:url(image/w_bishop.svg)")
        self.update_icon("B1", "background-image:url(image/w_bishop.svg)")
        self.update_icon("C1", "background-image:url(image/w_knight.svg)")
        self.update_icon("A2", "background-image:url(image/w_knight.svg)")

        self.generalLayout.addLayout(buttonsLayout)

    def update_board(self, ai_move=""):

        if ai_move == "":
            self.clear_highlight()
            self.update_icon(main.mv_from_to[:2], color="#2cd3db")

            dest = main.mv_from_to[2:4]
            chess_board = main.get_chess_board()

            i = main.letter2pos(dest[:1])
            j = int(dest[1:])

            piece = chess_board.get_piece(i, 8 - j)
            piece_icon = main.piece_icon(piece.to_string())

            self.update_icon(main.mv_from_to[2:4], piece_icon, color="#2cd3db")
        else:
            self.clear_highlight()
            origin = ai_move[:2]
            dest = ai_move[2:4]

            i = int(origin[:1])
            i_str = main.pos2letter(i)
            j = 8 - int(origin[1:])

            point = i_str + str(j)
            self.update_icon(point, color="#2cd3db")

            i = int(dest[:1])
            i_str = main.pos2letter(i)
            j = int(dest[1:])

            chess_board = main.get_chess_board()
            piece = chess_board.get_piece(i, j)
            piece_icon = main.piece_icon(piece.to_string())
            point = i_str + str(8 - j)
            self.update_icon(point, piece_icon, color="#2cd3db")

    def update_icon(self, point, icon="", color=""):
        i = main.letter2pos(point[:1])
        j = int(point[1:])

        if (i + j) % 2 == 0:
            if color == "":
                self.buttons[point].setStyleSheet("background-color: white;color:rgba(0,0,0,0.0);" + icon)
            else:
                self.buttons[point].setStyleSheet("background-color: " + color + ";color:rgba(0,0,0,0.0);" + icon)
        else:
            if color == "":
                self.buttons[point].setStyleSheet("background-color: #555;color:rgba(0,0,0,0.0);" + icon)
            else:
                self.buttons[point].setStyleSheet("background-color: " + color + ";color:rgba(0,0,0,0.0);" + icon)

    def highlight_pool(self, point):
        i = main.letter2pos(point[:1])
        j = int(point[1:])
        chess_board = main.get_chess_board()
        piece = chess_board.get_piece(i, 8 - j)
        if piece != 0:
            p_color = "black" if main.is_black_turn else "white"

            for l in ["A", "B", "C", "D", "E", "F", "G", "H"]:
                for k in range(1, 9):
                    if main.get_valid_move(chess_board, point + l + str(k), p_color) != 1:
                        dest_i = main.letter2pos(l)
                        dest_piece = chess_board.get_piece(dest_i, 8 - k)
                        if dest_piece != 0:
                            self.update_icon(l + str(k), main.piece_icon(dest_piece.to_string()), "red")
                        else:
                            self.update_icon(l + str(k), "", "#3FD97F")


    def clear_highlight(self):
        for l in ["A", "B", "C", "D", "E", "F", "G", "H"]:
            for k in range(1, 9):
                i = main.letter2pos(l)
                chess_board = main.get_chess_board()
                piece = chess_board.get_piece(i, 8 - k)
                if piece != 0:
                    piece_icon = main.piece_icon(piece.to_string())
                    self.update_icon(l + str(k), piece_icon)
                else:
                    self.update_icon(l + str(k))

    def _createStats(self):
        self.stats = {}
        statsLayout = QGridLayout()
        stats = {"Głębokość": (0, 0), "Czas": (0, 1)}
        for statsText, pos in stats.items():
            self.stats[statsText] = QLabel(statsText)
            self.stats[statsText].setAlignment(Qt.AlignCenter)
            statsLayout.addWidget(self.stats[statsText], pos[0], pos[1])
        self.generalLayout.addLayout(statsLayout)

    def _createDisplayStats(self):
        self.max_depth = QLineEdit()
        self.max_depth.setReadOnly(True)
        self.max_depth.setAlignment(Qt.AlignCenter)
        self.time = QLineEdit()
        self.time.setReadOnly(True)
        self.time.setAlignment(Qt.AlignCenter)
        box_stats_layout = QGridLayout()
        box_stats_layout.addWidget(self.max_depth, 0, 0)
        box_stats_layout.addWidget(self.time, 0, 1)
        self.generalLayout.addLayout(box_stats_layout)

    def setDisplayMaxDepth(self, text):
        self.max_depth.setText(text)

    def setDisplayTime(self, text):
        self.time.setText(text)

    def _createStats2(self):
        self.stats = {}
        statsLayout2 = QGridLayout()
        stats = {"Punkty": (0, 0), "Sprawdzonych stanów": (0, 1)}
        for statsText, pos in stats.items():
            self.stats[statsText] = QLabel(statsText)
            self.stats[statsText].setAlignment(Qt.AlignCenter)
            statsLayout2.addWidget(self.stats[statsText], pos[0], pos[1])
        self.generalLayout.addLayout(statsLayout2)

    def _createDisplayStats2(self):
        self.points = QLineEdit()
        self.points.setReadOnly(True)
        self.points.setAlignment(Qt.AlignCenter)
        self.moves = QLineEdit()
        self.moves.setReadOnly(True)
        self.moves.setAlignment(Qt.AlignCenter)
        box_stats_layout2 = QGridLayout()
        box_stats_layout2.addWidget(self.points, 0, 0)
        box_stats_layout2.addWidget(self.moves, 0, 1)
        self.generalLayout.addLayout(box_stats_layout2)

    def setDisplayPoints(self, text):
        self.points.setText(text)

    def setDisplayMoves(self, text):
        self.moves.setText(text)


class PyChessCtrl:

    def __init__(self, view):
        self._view = view
        self._connectSignals()

    def _calculateMove(self):
        chess_board = main.get_chess_board()
        if main.white_player == "player" and not main.is_black_turn:
            self.print_player_move(chess_board, "white")
            return

        if main.black_player == "player" and main.is_black_turn:
            self.print_player_move(chess_board, "black")
            return

        if main.white_player == "ai" and not main.is_black_turn:
            self.print_ai_move(chess_board, "white")
            return

        if main.black_player == "ai" and main.is_black_turn:
            self.print_ai_move(chess_board, "black")
            return

    def _buildMove(self, mv_text):
        if len(main.mv_from_to) == 4:
            main.mv_from_to = ""
            main.mv_from_to += mv_text
            self._view.highlight_pool(mv_text)
        elif main.mv_from_to == "":
            self._view.highlight_pool(mv_text)
        elif len(main.mv_from_to) == 2:
            self._view.clear_highlight()
            main.mv_from_to += mv_text

    def _connectSignals(self):
        for btnText, btn in self._view.buttons.items():
            btn.clicked.connect(partial(self._buildMove, btnText))
        self._view.max_depth.returnPressed.connect(self._calculateMove)

    def print_ai_move(self, chess_board, color):
        t1 = time.time()
        move_ai, score_ai, count_moves_ai, max_deep = ai.AI.get_ai_move(chess_board, color)
        if color == "white":
            main.hash_move_array.append(chess_board.get_hash_board_to_drawn(True))
        if color == "black":
            main.hash_move_array.append(chess_board.get_hash_board_to_drawn(False))
        t2 = time.time()
        self._view.setDisplayTime("Czas: " + str(round(t2 - t1, 2)) + "s")
        if move_ai == 0 and color == "white":
            self._view.show_endgame_message("Białe przegrały")
            return
        if move_ai == 0 and color == "black":
            self._view.show_endgame_message("Czarne przegrały")
            return
        if main.is_drawn():
            self._view.show_endgame_message("Remis")
            return
        elif main.is_won(color):
            if color == "white":
                self._view.show_endgame_message("Wygrywa biały")
            else:
                self._view.show_endgame_message("Wygrywa czarny")
            return
        else:
            self._view.setDisplayMoves(str(count_moves_ai))
            chess_board.perform_move(move_ai)
            self._view.update_board(move_ai.to_string())
            
            if color == "white":
                self._view.setDisplayPoints("Biały: " + str(score_ai))
                self._view.setDisplayMaxDepth(str((max_deep + 1)/2))
                main.is_black_turn = True
            else:
                self._view.setDisplayPoints("Czarny: " + str(score_ai))
                self._view.setDisplayMaxDepth(str((max_deep + 1)/2))
                main.is_black_turn = False
        main.game_depth = main.game_depth + 1
        return

    def print_player_move(self, chess_board, color):
        if main.is_drawn():
            self._view.show_endgame_message("Remis")
            return
        if main.is_won(color):
            if color == "white":
                self._view.show_endgame_message("Wygrywa biały")
            else:
                self._view.show_endgame_message("Wygrywa czarny")
            return
            
        move_player = main.get_valid_move(chess_board, main.mv_from_to, color)

        if move_player == 1:
            self._view.show_endgame_message("Błędny ruch")
            return
        elif move_player == 2 and color == "white":
            self._view.show_endgame_message("Białe przegrały")
            return
        elif move_player == 2 and color == "black":
            self._view.show_endgame_message("Czarne przegrały")
            return
        else:
            chess_board.perform_move(move_player)
            main.game_depth = main.game_depth + 1
            if color == "white":
                main.hash_move_array.append(chess_board.get_hash_board_to_drawn(True))
            else:
                main.hash_move_array.append(chess_board.get_hash_board_to_drawn(False))
            self._view.update_board()
            if color == "white":
                main.is_black_turn = True
                if main.black_player == "ai":
                    self.print_ai_move(chess_board, "black")
            else:
                main.is_black_turn = False
                if main.white_player == "ai":
                    self.print_ai_move(chess_board, "white")
        return

