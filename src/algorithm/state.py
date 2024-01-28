from dataclasses import dataclass
from copy import deepcopy

from random import shuffle

from ..gui.piece import Abstract_Piece
from ..gui.board import Board
from .check_winner import check_winner
from .check_winner import count_pieces_in_line

MY_GOBBLING_WEIGHT = 1
OTHER_GOBBLING_WEIGHT = 3
EMPTY_CELL_WEIGHT = 2

def is_piece_in_the_same_line(piece,row,col,check):

    if piece.is_outside():
        return True
    if check == "row" :
        return piece.row == row
    elif check == "col" :
        return piece.col == col
    elif check == "left":
        return piece.col == piece.row
    else:
        return piece.col == (3 - piece.row) 

@dataclass
class Piece_Move:
    piece: Abstract_Piece
    row_to: int
    col_to: int
    from_outside: bool
    row_from: int
    col_from: int
    weight: int


class State:
    def __init__(self, board, stacks):
        self.board = board
        self.stacks = stacks

    def is_game_over(self):
        is_winner = check_winner(self)
        return True if is_winner else False

    def get_movable_pieces(self, player):
        movable_pieces = []
        # movable pieces from the board cells
        for row in range(4):
            for col in range(4):
                piece = self.get_top_piece(row, col)
                if not piece:
                    continue
                if piece.player == player:
                    movable_pieces.append(piece)

        # get piece from the top of the outside stack
        player_stacks = self.stacks[player]
        for stack in player_stacks:
            if stack:
                movable_pieces.append(stack[-1])
        return movable_pieces

    def get_valid_piece_moves(self, piece, from_outside, include_winning_moves=False):
        if include_winning_moves:
            winning_moves = self.has_a_win_move(piece)
            if winning_moves:
                # print("winning:", winning_moves)
                return winning_moves, True
        valid_piece_moves = []
        for row in range(4):
            for col in range(4):
                move = Piece_Move(piece, row, col, from_outside, piece.row, piece.col,0)
                if self.is_valid_piece_move(move):
                    valid_piece_moves.append(move)
        return valid_piece_moves, False

    def has_a_win_move(self, target_piece):
        winning_moves = []
        def helper(count, x, y, open_place, check):
            nonlocal winning_moves
            piece = self.get_top_piece(x, y)
            if not piece:
                # exclude pieces in that line
                if not is_piece_in_the_same_line(target_piece,x,y, check):
                    open_place = (x, y)
            elif piece.player != target_piece.player and piece.size < target_piece.size:
                open_place = (x, y)
            elif piece.player == target_piece.player:
                count += 1
            if count == 3 and open_place:
                is_outside = target_piece.is_outside()
                winning_moves.append(
                    Piece_Move(
                        target_piece,
                        open_place[0],
                        open_place[1],
                        is_outside,
                        target_piece.row,
                        target_piece.col,
                        100
                    )
                )
                count = 0
                open_place = None
            return count, open_place

        l_diag_count, open_l_diag = 0, None
        r_diag_count, open_r_diag = 0, None
        for row in range(4):
            row_count, open_row = 0, None
            col_count, open_col = 0, None
            for col in range(4):
                row_count, open_row = helper(row_count, row, col, open_row, "row")
                col_count, open_col = helper(col_count, col, row, open_col, "col")
            if winning_moves:
                return winning_moves
            l_diag_count, open_l_diag = helper(l_diag_count, row, row, open_l_diag, "left")
            if winning_moves:
                return winning_moves
            r_diag_count, open_r_diag = helper(r_diag_count, row, 3 - row, open_r_diag, "right")
            if winning_moves:
                return winning_moves
        return winning_moves

    def get_valid_moves(self, player, include_winning_moves):
        valid_moves = []
        movable_pieces = self.get_movable_pieces(player)
        has_winning = False
        for piece in movable_pieces:
            moves, has_winning = self.get_valid_piece_moves(
                piece, piece.is_outside(), include_winning_moves
            )
            valid_moves.extend(moves)
        shuffle(valid_moves)
        return valid_moves, has_winning

    def is_valid_piece_move(self, move):
        top_piece = self.get_top_piece(move.row_to, move.col_to)
        if top_piece is None:  # cell is empty
            move.weight = EMPTY_CELL_WEIGHT
            return True
        elif top_piece.size < move.piece.size:  # can gobble
            if top_piece.player == move.piece.player:
                move.weight = MY_GOBBLING_WEIGHT
            else:
                move.weight = OTHER_GOBBLING_WEIGHT
            return True
        return False

    def get_top_piece(self, row, col):
        if self.board[row][col]:
            return self.board[row][col][-1]
        return None

    def undo_move(self, move, player):
        if self.board[move.row_to][move.col_to][-1].piece_id != move.piece.piece_id:
            raise Exception("Not the same piece")

        if player != move.piece.player:
            raise Exception("Different players")

        self.board[move.row_to][move.col_to].pop()
        move.piece.row = move.row_from
        move.piece.col = move.col_from
        if move.from_outside:
            self.stacks[player][move.piece.aside_stack].append(move.piece)
        else:
            self.board[move.row_from][move.col_from].append(move.piece)

    def apply_move(self, move, player):
        if player != move.piece.player:
            raise Exception("Different players")
        if move.from_outside:
            self.stacks[player][move.piece.aside_stack].pop()
        else:
            self.board[move.piece.row][move.piece.col].pop()
        move.piece.row = move.row_to
        move.piece.col = move.col_to
        self.board[move.row_to][move.col_to].append(move.piece)
