from dataclasses import dataclass
from copy import deepcopy

from random import shuffle

from ..gui.piece import Abstract_Piece
from ..gui.board import Board
from .check_winner import check_winner
from .check_winner import count_pieces_in_line


@dataclass
class Piece_Move:
    piece: Abstract_Piece
    row_to: int
    col_to: int
    from_outside: bool


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

    def get_valid_piece_moves(self, piece, from_outside, include_winning_moves= False):
        if include_winning_moves :
            winning_moves = self.has_a_win_move(piece)
            if winning_moves:
                # print(winning_moves)
                return winning_moves, True
        valid_piece_moves = []
        for row in range(4):
            for col in range(4):
                move = Piece_Move(piece, row, col, from_outside)
                if self.is_valid_piece_move(move):
                    valid_piece_moves.append(move)
        return valid_piece_moves, False

    def has_a_win_move(self, target_piece):
        winning_moves = []

        def helper(count, x, y, open_place):
            nonlocal winning_moves
            # open_place = None
            piece = self.get_top_piece(x, y)
            if not piece:
                open_place = (x, y)
            elif piece.player != target_piece.player and piece.size < target_piece.size:
                open_place = (x, y)
            elif piece.player == target_piece.player:
                count += 1
            # if count == 3 and open_place:
            #     is_outside = target_piece.row == None and target_piece.col == None
            #     winning_moves.append(Piece_Move(target_piece, open_place[0], open_place[1], is_outside))
            #     count = 0 
            #     open_place = None
            return count, open_place

        l_diag_count, open_l_diag = 0, None
        r_diag_count, open_r_diag = 0, None
        for row in range(4):
            row_count, open_row = 0, None
            col_count, open_col = 0, None
            for col in range(4):
                # print(col, row)
                row_count, open_row = helper(row_count, row, col, open_row)
                if row_count == 3 and open_row:
                    is_outside = target_piece.row == None and target_piece.col == None
                    winning_moves.append(Piece_Move(target_piece, open_row[0], open_row[1], is_outside))
                    row_count = 0 
                    open_row = None

                col_count, open_col = helper(col_count, col, row, open_col)
                if col_count == 3 and open_col:
                    is_outside = target_piece.row == None and target_piece.col == None
                    winning_moves.append(Piece_Move(target_piece, open_col[0], open_col[1], is_outside))
                    col_count = 0 
                    open_col = None

            l_diag_count, open_l_diag = helper(l_diag_count, row, row, open_l_diag)
            if l_diag_count == 3 and open_l_diag:
                is_outside = target_piece.row == None and target_piece.col == None
                winning_moves.append(Piece_Move(target_piece, open_l_diag[0], open_l_diag[1], is_outside))
                l_diag_count = 0 
                open_l_diag = None

            r_diag_count, open_r_diag = helper(r_diag_count, row, 3 - row, open_r_diag)
            if r_diag_count == 3 and open_r_diag:
                is_outside = target_piece.row == None and target_piece.col == None
                winning_moves.append(Piece_Move(target_piece, open_r_diag[0], open_r_diag[1], is_outside))
                r_diag_count = 0 
                open_r_diag = None

        # print("*"*30)
        return winning_moves

    def get_valid_moves(self, player, include_winning_moves):
        valid_moves = []
        movable_pieces = self.get_movable_pieces(player)
        has_winning = False
        for piece in movable_pieces:
            is_outside = piece.row == None and piece.col == None
            moves, has_winning = self.get_valid_piece_moves(piece, is_outside,include_winning_moves)
            valid_moves.extend(moves)
        shuffle(valid_moves)
        return valid_moves, has_winning

    def is_valid_piece_move(self, move):
        top_piece = self.get_top_piece(move.row_to, move.col_to)
        if top_piece is None:  # cell is empty
            return True
        elif top_piece.size >= move.piece.size:
            return False
        return True

    def get_top_piece(self, row, col):
        if self.board[row][col]:
            return self.board[row][col][-1]
        return None

    def apply_move(self, move, player):

        if player != move.piece.player :
            raise Exception("different players")
        new_stacks = deepcopy(self.stacks)
        new_board = deepcopy(self.board)
        # new_board = jsonpickle.decode(jsonpickle.encode(self.board))
        # new_stacks = jsonpickle.decode(jsonpickle.encode(self.stacks))
        if move.from_outside:
            new_stacks[player][move.piece.aside_stack].pop()
        else:
            new_board[move.piece.row][move.piece.col].pop()
        new_piece = Abstract_Piece(
            move.piece.piece_id,
            move.piece.player,
            move.piece.size,
            move.piece.aside_stack,
            move.row_to,
            move.col_to,
        )
        new_board[move.row_to][move.col_to].append(new_piece)
        return State(new_board, new_stacks)
