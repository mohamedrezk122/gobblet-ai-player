import pygame
import pygame_menu as pgm

from .constants import *
from .piece import Piece

class Board:
    def __init__(self, menu):
        self.menu = menu
        self.board = []
        self.pieces = []
        self.create_borad()
        self.intialize_pieces()

    def create_borad(self):
        menu_deco = self.menu.get_scrollarea().get_decorator()
        self.menu.add.vertical_margin(40)
        for row in range(BOARD_ROWS):
            y = BOARD_POS_Y + row * CELL_HEIGHT
            self.board.append([])
            for col in range(BOARD_COLS):
                self.board[row].append([])
                x = BOARD_POS_X + col * CELL_WIDTH
                cell = menu_deco.add_rectangle(
                    x,
                    y,
                    CELL_WIDTH,
                    CELL_HEIGHT,
                    CELL_COLOR,
                    use_center_positioning=False,
                )
                menu_deco.add_rectangle(
                    x,
                    y,
                    CELL_WIDTH + 3,
                    CELL_HEIGHT + 3,
                    CELL_BORDER,
                    3,
                    use_center_positioning=False,
                )


    def intialize_pieces(self):
        for i in range(PIECES_BY_PLAYER // PIECES_SIZES):
            for size in SIZE.keys():
                for player in PLAYER.keys():
                    piece = Piece(player, size, None, None)
                    piece.intialize_widget(self.menu)
                    piece.place_aside(i)
                    self.pieces.append(piece)

    def get_pieces(self):
        return self.pieces

