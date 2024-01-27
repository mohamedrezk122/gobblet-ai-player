import pygame
import pygame_menu as pgm

from .constants import *

pygame.mixer.init()
move_sound = pygame.mixer.Sound("./src/gui/assets/move.mp3")


def convert_from_row_col_to_abs_pos(row, col, piece_width, piece_height):
    dx, dy = -piece_width // 2, -piece_height // 2
    x = BOARD_POS_X + (col + 0.5) * (CELL_WIDTH) + dx
    y = BOARD_POS_Y + (row + 0.5) * (CELL_HEIGHT) + dy
    return x, y


class Drag_Handler:
    def __init__(self, game):
        self.active = None
        self.drag = False
        self.past_pos = None
        self.game = game

        # a list constaining the info of the move from which cell to which, etc.
        self.augmented_move = None
        self.human_played = False

    def move_piece_with_mouse(self, pieces, event):
        piece = pieces[self.active]
        piece.set_pos(event.pos[0], event.pos[1])
        self.drag = True

    def get_active_piece(self, pieces, event):
        active = None
        current_player = self.game.get_current_player()
        active_pieces = []
        for idx, piece in enumerate(pieces):
            if piece.collidepoint(event.pos):
                if piece.player != current_player:
                    continue
                active_pieces.append(idx)

        max_so_far = -1
        # choose the one on top
        for piece_idx in active_pieces:
            piece = pieces[piece_idx]
            if max_so_far < SIZE[piece.size][-1]:
                max_so_far = SIZE[piece.size][-1]
                active = piece_idx
        if not self.drag and active is not None:
            self.past_pos = pieces[active].get_position()
        return active

    def release_piece_at_tile(self, board, abstract_board, stacks, pieces, event):
        if self.drag and self.active is not None:
            col, row = self.get_tile_under_mouse(event.pos)
            if col is not None and row is not None:
                self.check_rules(board, abstract_board, stacks, pieces, row, col, event)
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

    def update(self, events, is_ai_player=False, move=None):
        board = self.game.get_board().board
        abstract_board = self.game.get_board().abstract_board
        pieces = self.game.get_board().get_pieces()
        stacks = self.game.get_board().stacks

        if is_ai_player:
            self.move_piece_by_ai(board, abstract_board, stacks, pieces, move)

        if self.game.end_of_game:
            return
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.active = self.get_active_piece(pieces, event)
            if event.type == pygame.MOUSEBUTTONUP:
                self.release_piece_at_tile(board, abstract_board, stacks, pieces, event)
            if (self.active is not None) and (event.type == pygame.MOUSEMOTION):
                self.move_piece_with_mouse(pieces, event)

    def interpolate_path(self, point1, point2, num=100):
        if (point1[0] - point2[0]) == 0:
            dy = (point2[1] - point1[1]) / num
            return [[point1[0], point1[1] + i * dy] for i in range(num)] + list(point2)
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
            try:
                piece.set_pos(int(pt[0]), int(pt[1]))
            except:
                pass

    def move_piece_by_ai(self, board, abstract_board, stacks, pieces, move):
        print("-" * 20)
        print(move)
        print("-" * 20)

        piece = None
        if not move.from_outside:
            piece = board[move.piece.row][move.piece.col][-1]
        else:
            for pc in pieces:
                if pc.id == move.piece.piece_id:
                    piece = pc
                    break
        self.yank_move(
            board, abstract_board, stacks, piece, move.row_to, move.col_to, False
        )

        point1 = [piece.x, piece.y]
        point2 = convert_from_row_col_to_abs_pos(
            move.row_to,
            move.col_to,
            piece.button.get_width(),
            piece.button.get_height(),
        )
        points = self.interpolate_path(point1, point2, 400)
        self.move_automatically(points, piece)
        piece.set_pos_by_row_and_col(move.row_to, move.col_to)
        move_sound.play()
        self.game.switch_turns()

    def yank_move(
        self, board, abstract_board, stacks, piece, row, col, switch_turns=True
    ):
        current_row, current_col = piece.row, piece.col
        # dont count move if it is the same place
        if current_col == col and current_row == row:
            return None
        if current_col != None and current_row != None:
            stack = board[current_row][current_col]
            abstract_board[current_row][current_col].pop()
            stack.pop()
            if stack:
                stack[-1].button.show()
        # from outside
        else:
            stacks[piece.player][piece.aside_stack].pop()
            print(stacks[piece.player])

        piece.set_pos_by_row_and_col(row, col)
        board[row][col].append(piece)
        piece.abstract_piece.col = col
        piece.abstract_piece.row = row
        abstract_board[row][col].append(piece.abstract_piece)
        stack = board[row][col]
        if len(stack) > 1:
            for i in range(len(stack) - 1):
                stack[i].button.hide()

        if switch_turns:
            self.game.switch_turns()
            move_sound.play()

    def return_piece(self, pieces, event):
        points = self.interpolate_path(event.pos, self.past_pos)
        self.move_automatically(points, pieces[self.active])

    def check_rules(self, board, abstract_board, stacks, pieces, row, col, event):
        if board[row][col]:
            # check gobbling rule
            if SIZE[board[row][col][-1].size][-1] < SIZE[pieces[self.active].size][-1]:
                self.yank_move(
                    board, abstract_board, stacks, pieces[self.active], row, col
                )
                self.human_played = True
            else:
                # invalid move, return piece as it was
                self.return_piece(pieces, event)
                self.human_played = False
        else:
            # the cell is empty
            self.yank_move(board, abstract_board, stacks, pieces[self.active], row, col)
            self.human_played = True
