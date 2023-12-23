import pygame 
import pygame_menu as pgm 
from constants import *

pygame.mixer.init()
move_sound = pygame.mixer.Sound("./assets/move.mp3")


class Drag_Handler:
    def __init__(self, game):
        self.active = None
        self.drag = False
        self.past_pos = None
        self.game = game

    def move_piece_with_mouse(self, pieces, event):
        piece = pieces[self.active]
        piece.set_pos(event.pos[0], event.pos[1])
        self.drag = True

    def get_active_piece(self, pieces, event):
        active = None
        current_player = self.game.get_current_player()
        for idx, piece in enumerate(pieces):
            if piece.collidepoint(event.pos):
                if piece.player != current_player :
                    continue 
                if not self.drag:
                    self.past_pos = piece.get_position()
                active = idx
        return active

    def release_piece_at_tile(self, board, pieces, event):
        if self.drag and self.active is not None:
            col, row = self.get_tile_under_mouse(event.pos)
            if col is not None and row is not None:
                self.check_rules(board,pieces,row , col, event)
            else:
                self.return_piece(pieces, event)
        self.active = None
        self.drag = False

    def get_tile_under_mouse(self, pos):
        x, y = pos
        if BOARD_POS_X <= x <= (BOARD_POS_X + BOARD_WIDTH) and BOARD_POS_Y <= y <= (
            BOARD_POS_Y + BOARD_HEIGHT
        ):
            return (x - BOARD_POS_X) // CELL_WIDTH, (y - BOARD_POS_Y) // CELL_HEIGHT
        else:
            return None, None

    def update(self,events):
        board  = self.game.get_board().board
        pieces = self.game.get_board().get_pieces()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.active = self.get_active_piece(pieces, event)
            if event.type == pygame.MOUSEBUTTONUP:
                self.release_piece_at_tile(board, pieces, event)
            if (self.active is not None) and (event.type == pygame.MOUSEMOTION):
                self.move_piece_with_mouse(pieces, event)

    def interpolate_path(self, point1, point2, num=100):
        slope = (point1[1] - point2[1]) / (point1[0] - point2[0])
        points = [point1]
        dx = (point1[0] - point2[0]) // num
        for i in range(1, num):
            pt_x = point1[0] + i * dx
            pt_y = slope * pt_x + point1[1] - (slope * point1[0])
            points.append((int(pt_x), int(pt_y)))
        points.append(point2)
        return points

    def move_automatically(self, points, piece):
        for pt in points:
            piece.set_pos(int(pt[0]), int(pt[1]))

    def yank_move(self, board, pieces,row , col):
        current_row, current_col = pieces[self.active].row , pieces[self.active].col
        # dont count move if it is the same place 
        if current_col == col and current_row == row :
            return 
        if current_col != None and current_row != None :
            board[current_row][current_col].pop()
        board[row][col].append(pieces[self.active])
        pieces[self.active].set_pos_by_row_and_col(row, col)
        self.game.switch_turns()
        move_sound.play() 

    def return_piece(self, pieces, event):
        points = self.interpolate_path(event.pos, self.past_pos)
        self.move_automatically(points, pieces[self.active])

    def check_rules(self, board, pieces,row , col,event):
        if board[row][col]: 
            # check gobbling rule 
            if SIZE[board[row][col][-1].size][-1] < SIZE[pieces[self.active].size][-1]:
                self.yank_move(board, pieces,row , col)
            else:
                # invalid move, return piece as it was  
                self.return_piece(pieces, event)
        else:
            # the cell is empty 
            self.yank_move(board, pieces,row , col)

