import itertools
import pygame
import pygame_menu as pgm
from dataclasses import dataclass

from .constants import *

def dummy():
    print("pressed")


@dataclass
class Abstract_Piece:
    piece_id: int
    player: str
    size: int
    aside_stack: int
    row: int
    col: int

    def __repr__(self):
        return f"({self.piece_id} {self.player} {self.size})"

    def __deepcopy__(self, memo):
        # Create a new instance of the data class
        new_instance = self.__class__.__new__(self.__class__)
        new_instance.piece_id = self.piece_id
        new_instance.player = self.player
        new_instance.size = self.size
        new_instance.aside_stack = self.aside_stack
        new_instance.row = self.row
        new_instance.col = self.col
        return new_instance

    def is_outside(self):
        return self.row == None and self.col == None

class Piece:
    obj_id = itertools.count()

    def __init__(self, player, size, aside_stack, row=None, col=None):
        self.player = player
        self.size = size
        self.row = row
        self.col = col
        self.x = 0
        self.y = 0
        self.id = next(Piece.obj_id)
        self.button = None
        self.aside_stack = aside_stack
        self.abstract_piece = Abstract_Piece(
            self.id, self.player, SIZE[self.size][-1] + 1, self.aside_stack, None, None
        )
        self.image = pgm.BaseImage(
            PLAYER[self.player][-1], drawing_mode=pgm.baseimage.IMAGE_MODE_CENTER
        )
        self.image.resize(width=SIZE[self.size][1], height=SIZE[self.size][1])

    def __str__(self):
        return f"Piece@ player {PLAYER[self.player][0]} size {SIZE[self.size][-1]}"

    def __repr__(self):
        return f"{PLAYER[self.player][0]} size {SIZE[self.size][-1]}"

    def place_aside(self, idx):
        self.dx, self.dy = self.position_correction()
        offset = BOARD_POS_X / 2
        if self.player == "b":
            offset = BOARD_WIDTH + 1.5 * BOARD_POS_X
        self.x = offset + self.dx
        self.y = (
            BOARD_POS_Y + (idx * BOARD_HEIGHT / 3) + 0.5 * BOARD_HEIGHT / 3
        ) + self.dy

        self.button.translate(self.x, self.y)
        self.rerender_button()

    def set_pos_by_row_and_col(self, row, col):
        self.x = BOARD_POS_X + (col + 0.5) * (CELL_WIDTH) + self.dx
        self.y = BOARD_POS_Y + (row + 0.5) * (CELL_HEIGHT) + self.dy
        self.button.translate(self.x, self.y)
        self.rerender_button()
        self.row = row
        self.col = col
        self.abstract_piece.row = row
        self.abstract_piece.col = col

    def get_position(self):
        return self.x, self.y

    def set_pos(self, x, y):
        self.x = x + self.dx
        self.y = y + self.dy
        self.button.translate(x, y)
        self.rerender_button()

    def collidepoint(self, *args, **kwargs):
        return self.button.get_rect().collidepoint(*args, **kwargs)

    def get_piece_info():
        return self.player, self.size

    def intialize_widget(self, menu):
        button = menu.add.button(
            str(SIZE[self.size][-1] + 1),
            dummy,
            font_size=50,
            font_color=PLAYER[self.player][1],
        )
        button.set_cursor(pgm.locals.CURSOR_HAND)
        button.set_float(origin_position=True)
        button.get_decorator().add_baseimage(0, 0, self.image, centered=True)
        button.set_attribute("piece", self)
        button_selection = pgm.widgets.LeftArrowSelection(
            arrow_size=(20, 30), blink_ms=1000
        )
        button.set_selection_effect(button_selection.set_color("#ff00ff"))
        self.button = button

    def rerender_button(self):
        self.button.render()
        self.button.force_menu_surface_cache_update()

    def position_correction(self):
        return -self.button.get_width() // 2, -self.button.get_height() // 2

    def get_size(self):
        return SIZE[self.size][-1] + 1

    def is_outside(self):
        return self.row == None and self.col == None
