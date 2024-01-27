import pygame
import pygame_menu as pgm

from .constants import *
from .piece import Piece


class Board:
    def __init__(self, menu=None):
        self.menu = menu
        self.board = self.construct_empty_board()
        self.abstract_board = self.construct_empty_board()
        self.stacks = {"w": [[], [], []], "b": [[], [], []]}  # white and black
        self.pieces = []
        if menu:
            self.create_borad()
        self.intialize_pieces()

    def construct_empty_board(self):
        board = []
        for i in range(4):
            board.append([])
            for _ in range(4):
                board[i].append([])
        return board

    def create_borad(self):
        menu_deco = self.menu.get_scrollarea().get_decorator()
        self.menu.add.vertical_margin(40)
        for row in range(BOARD_ROWS):
            y = BOARD_POS_Y + row * CELL_HEIGHT
            # self.board.append([])
            for col in range(BOARD_COLS):
                # self.board[row].append([])
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
                    piece = Piece(player, size, i, None, None)
                    if self.menu:
                        piece.intialize_widget(self.menu)
                        piece.place_aside(i)
                    self.pieces.append(piece)
                    self.stacks[player][i].append(piece.abstract_piece)

    def get_pieces(self):
        return self.pieces

    def get_stack(self, row, col):
        if self.board[row][col]:
            return self.board[row][col]
        return None

    def get_top_piece(self, row, col):
        stack = self.get_stack(row, col)
        if stack:
            return stack[-1]
        return None

    @staticmethod
    def print_board(board):
        for row in board:
            for cell in row:
                for p in cell:
                    print(p.player, end=" ")
                print(" | ", end=" ")
            print()
            print("--------------------------------------")
