import pygame 
import pygame_menu as pgm 

from .board import Board
from .drag_handler import Drag_Handler
from .constants import * 

class Game:

    def __init__(self, game_window):
        self.game_window = game_window
        self.board = Board(game_window)
        self.drag_handler = Drag_Handler(self)

        self.current_player = "w"
        self.game_mode = None 
        self.difficulty = None 
        self.intialize_labels()
        self.turn_label = self.game_window.get_widget('turn')

    def reset(self):
        self.game_window.full_reset()
        self.game_window.clear()
        self.board = Board(self.game_window)
        self.current_player = 'w'
        self.intialize_labels()

    def set_difficulty(self,selected, value):
        print(selected ," ", value)
        self.reset()

    def set_game_mode(self,selected, value):
        print(selected ," ", value)
        self.reset()

    def switch_turns(self):
        self.current_player = "b" if self.current_player == "w" else "w"
        self.turn_label.set_title(PLAYER[self.current_player][0])
        self.turn_label.update_font({"color" : PLAYER[self.current_player][2]})

    def check_game_state(self):
        pass  

    def move_piece_by_human(self):
        pass

    def move_piece_by_AI(self):
        pass

    def check_collision(self,events):
        self.drag_handler.update(events)

    def get_board(self):
        return self.board

    def get_current_player(self):
        return self.current_player 

    def intialize_labels(self):
        label = self.game_window.add.label("Turn",font_size=50, font_color="#f0ff00")
        label.set_float(origin_position=True)
        label.translate(WIDTH//2, 30)

        turn_label = self.game_window.add.label("White", label_id = "turn",font_size=50, font_color="#ffffff")
        turn_label.set_float(origin_position=True)
        turn_label.translate(WIDTH//2 - 130 , 30)