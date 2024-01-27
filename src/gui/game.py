import time
import pygame
import pygame_menu as pgm

from .board import Board
from .drag_handler import Drag_Handler
from .constants import *
from ..algorithm.ai_agent import AI_Agent
from ..algorithm.state import State
from ..algorithm.check_winner import check_winner


class Game:
    def __init__(self, game_window):
        self.game_window = game_window
        self.game_mode = MODES[0]  # human vs human
        self.difficulty = DIFFICULTIES[0]
        self.reset()

    def reset(self):
        self.game_window.full_reset()
        self.game_window.clear()
        self.board = Board(self.game_window)
        self.state = State(self.board.abstract_board, self.board.stacks)
        self.drag_handler = Drag_Handler(self)
        self.current_player = "w"  # white starts by default
        self.intialize_labels()
        self.turn_label = self.game_window.get_widget("turn")
        self.winner = None
        self.end_of_game = False
        if self.game_mode == MODES[1]:
            self.ai_should_play = False
            if len(self.difficulty) == 2:
                self.agent = AI_Agent("b", str(self.difficulty[0]))
            else:
                self.agent = AI_Agent("b", self.difficulty)

        elif self.game_mode == MODES[2]:
            self.white_should_play = True
            self.black_should_play = False
            print(self.difficulty)
            self.w_agent = AI_Agent("w", self.difficulty[0])
            self.b_agent = AI_Agent("b", self.difficulty[1])

    def set_difficulty(self, selected, value):
        if self.game_mode == MODES[1]:
            self.difficulty = DIFFICULTIES[value][0]  # consider the first one only
        elif self.game_mode == MODES[2]:
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
        winner = check_winner(self.state)
        print("winner : ", winner)
        if winner:
            self.winner = winner
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
        if self.game_mode == MODES[0]:
            self.human_vs_human_mode(events)
        elif self.game_mode == MODES[1]:
            self.human_vs_ai_mode(events)
        else:
            self.ai_vs_ai_mode(events)

    def human_vs_human_mode(self, events):
        self.drag_handler.update(events, is_ai_player=False)

    def human_vs_ai_mode(self, events):
        if self.end_of_game:
            return
        is_ai_player = self.current_player == "b"
        if is_ai_player and self.ai_should_play:
            ai_move = self.agent.play_by_ai(self.state)
            if not ai_move :
                raise Exception("empty move") 
            self.drag_handler.update(events, is_ai_player, ai_move)
            self.ai_should_play = False
            self.state = State(self.board.abstract_board, self.board.stacks)
            Board.print_board(self.board.board)
            print("*************************************")
            Board.print_board(self.board.abstract_board)
            # pygame.time.delay(300)
        elif not is_ai_player and not self.ai_should_play:
            self.drag_handler.update(events, False, None)
            if self.drag_handler.human_played:
                self.ai_should_play = True
                self.drag_handler.human_played = False
                self.state = State(self.board.abstract_board, self.board.stacks)
                Board.print_board(self.board.board)
                print("*************************************")
                Board.print_board(self.board.abstract_board)

    def ai_vs_ai_mode(self, events):
        if self.end_of_game:
            return
        if self.current_player == "w" and self.white_should_play:
            ai_move = self.w_agent.play_by_ai(self.state)
            if not ai_move :
                raise Exception("empty move") 
            self.drag_handler.update(events, True, ai_move)
            self.white_should_play = False
            self.black_should_play = True
            self.state = State(self.board.abstract_board, self.board.stacks)
            if self.difficulty[0] == "easy":
                pygame.time.delay(300)
        elif self.current_player == "b" and self.black_should_play:
            ai_move = self.b_agent.play_by_ai(self.state)
            if not ai_move :
                raise Exception("empty move") 
            self.drag_handler.update(events, True, ai_move)
            self.white_should_play = True
            self.black_should_play = False
            self.state = State(self.board.abstract_board, self.board.stacks)
            if self.difficulty[1] == "easy":
                pygame.time.delay(300)

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
