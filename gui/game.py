import time
import pygame
import pygame_menu as pgm

from .board import Board
from .drag_handler import Drag_Handler
from .constants import *
from .ai_agent import Logic


class Game:
    def __init__(self, game_window):
        self.game_window = game_window

        self.game_mode = MODES[0]  # human vs human
        self.difficulty = "easy"
        self.ai_should_play = True
        self.reset()


    def reset(self):
        self.game_window.full_reset()
        self.game_window.clear()
        self.board = Board(self.game_window)
        self.drag_handler = Drag_Handler(self)
        self.current_player = "w"  # white starts by default
        self.intialize_labels()
        self.turn_label = self.game_window.get_widget("turn")
        self.agent = Logic()
        self.agent.current = self.current_player
        self.winner = None
        self.end_of_game = False

    def set_difficulty(self, selected, value):
        if self.game_mode == ["human", "ai"]:
            self.difficulty = DIFFICULTIES[value][0]  # consider the first one only
        elif self.game_mode == ["ai", "ai"]:
            self.difficulty = DIFFICULTIES[value]
        print("Difficulty: ", self.difficulty)
        self.reset()

    def set_game_mode(self, selected, value):
        self.game_mode = MODES[value]
        print("Game Mode:", self.game_mode)
        self.reset()

    def switch_turns(self):
        self.current_player = "b" if self.current_player == "w" else "w"
        self.turn_label.set_title(PLAYER[self.current_player][0])
        self.turn_label.update_font({"color": PLAYER[self.current_player][2]})
        self.check_game_state()

    def check_game_state(self):
        self.check_row_win()
        self.check_col_win()
        self.check_diagonal_win()
        self.check_diagonal_win(right=True)

        if self.winner:
            self.raise_end_of_game_flag()

    def raise_end_of_game_flag(self):
        self.end_of_game = True

        # remove whose turn
        self.turn_label.set_title("-")
        self.turn_label.update_font({"color": "#ff0000"})

        # declare winner
        winner = PLAYER[self.winner][0]
        label = self.game_window.add.label(
            f"{winner} WON!", font_size=80, font_color="#ff0000"
        )
        label.set_float(origin_position=True)
        label.translate(
            WIDTH // 2 - label.get_width() // 2, HEIGHT - label.get_height() - 60
        )

        # self.reset()

    def check_draw_state(self):
        pass

    def play(self, events):
        # if self.game_mode == ["human", "human"] :
            # self.human_vs_human_mode(events)
        # elif self.game_mode == ["human", "ai"]:
        self.human_vs_ai_mode(events)
        # else:
        #     self.ai_vs_ai_mode()

    def human_vs_human_mode(self, events):
        self.drag_handler.update(events, is_ai_player=False)
        aug_move = self.drag_handler.augmented_move
        if aug_move:
            self.agent.play_by_human(self.agent.current, aug_move[:4], aug_move[4:])
            self.drag_handler.augmented_move = None
            self.agent.set_winner()
            if self.agent.winner:
                print("Winner from logic: ", self.agent.winner)
            self.agent.switch_turns()

    def human_vs_ai_mode(self, events):
        is_ai_player = (self.current_player == "w")
        if is_ai_player and self.ai_should_play:
            ai_move = self.agent.play_by_ai("easy")
            self.drag_handler.update(events, is_ai_player, ai_move)
            self.ai_should_play = False
            self.agent.switch_turns()
            self.board.print_board()
        elif not is_ai_player and not self.ai_should_play:
            self.drag_handler.update(events)
            aug_move = self.drag_handler.augmented_move
            if aug_move is not None:
                self.agent.play_by_ai("easy", aug_move[:4], aug_move[4:])
                self.drag_handler.augmented_move = None
                self.ai_should_play = True
                self.agent.switch_turns()
        self.agent.set_winner()
        if self.agent.winner:
            pass
            # print("winner from logic :", self.agent.winner)
            # quit()
    def ai_vs_ai_mode(self):
        pass
    def get_board(self):
        return self.board

    def get_current_player(self):
        return self.current_player

    def intialize_labels(self):
        label = self.game_window.add.label("Turn", font_size=50, font_color="#f0ff00")
        label.set_float(origin_position=True)
        label.translate(WIDTH // 2, 30)

        turn_label = self.game_window.add.label(
            "White", label_id="turn", font_size=50, font_color="#ffffff"
        )
        turn_label.set_float(origin_position=True)
        turn_label.translate(WIDTH // 2 - 130, 30)

    def check_row_win(self):
        for row in range(BOARD_ROWS):
            top_colors_row = []
            for column in range(BOARD_COLS):
                top = self.board.get_top_piece(row, column)
                if not top:
                    break
                top_colors_row.append(top.player)

            if not top_colors_row:
                continue
            if self.count_colors(top_colors_row, "Row Win: "):
                return

    def check_col_win(self):
        for column in range(BOARD_COLS):
            top_colors_col = []
            for row in range(BOARD_ROWS):
                top = self.board.get_top_piece(row, column)
                if not top:
                    break
                top_colors_col.append(top.player)

            if not top_colors_col:
                continue

            if self.count_colors(top_colors_col, "Col Win: "):
                return

    def check_diagonal_win(self, right=False):
        # default is left diagonal checking
        top_colors_diagonal = []
        for i in range(BOARD_COLS):
            y = 3 - i if right else i
            top = self.board.get_top_piece(i, y)
            if not top:
                break
            top_colors_diagonal.append(top.player)

            msg = f"{'Right' if right else 'Left'} Diagonal Win: "
            if self.count_colors(top_colors_diagonal, msg):
                return

    def count_colors(self, colors, msg=""):
        # print(colors)
        if colors.count(colors[0]) == 4:
            self.winner = colors[0]
            if msg:
                print(msg + self.winner)
            return True  # there is a winner
        return False  # game continues
