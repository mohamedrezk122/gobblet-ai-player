import sys

from .check_winner import check_winner
from .check_winner import count_pieces_in_line

EMPTY_CELL_SCORE = 1

def is_corner(row, col):
    return abs(row - col) == 3

def compute_weight(piece_size):
    size_to_weight = {
        1: 50,
        2: 100,
        3: 130,
        4: 200,
    }
    return size_to_weight[piece_size]


# player - opponent
def surface_heuristic(state, player):
    winner = check_winner(state)
    if winner:
        if winner == player:
            return sys.maxsize
        else:
            return -sys.maxsize
    player_score = 0
    for row in range(4):
        for col in range(4):
            piece = state.get_top_piece(row, col)
            factor = 2 if is_corner(row,col) else 1
            if not piece:
                continue
            elif piece.player == player:
                player_score += factor * compute_weight(piece.size) * piece.size
            else:
                player_score -= factor * compute_weight(piece.size) * piece.size 
    return player_score


def custom_heuristic(state, player):
    w_count, b_count = 0, 0
    w_close_to_win, b_close_to_win = 0, 0
    w_won, b_won = 0, 0

    def increment_scores(w, b):
        nonlocal w_won, b_won, w_close_to_win, b_close_to_win, w_count, b_count
        if w == 3 :
            w_close_to_win += 10000
        if b == 3 :
            b_close_to_win += 10000 
        if w == 4:
            w_won = sys.maxsize
        if b == 4:
            b_won = sys.maxsize

    for i in range(4):
        w, b = count_pieces_in_line(state, [(i, j) for j in range(4)])  # rows
        increment_scores(w, b)
        w, b = count_pieces_in_line(state, [(j, i) for j in range(4)])  # cols
        increment_scores(w, b)

    w, b = count_pieces_in_line(state, [(i, i) for i in range(4)])  # left diag
    increment_scores(w, b)
    w, b = count_pieces_in_line(state, [(i, 3 - i) for i in range(4)])  # right_diag
    increment_scores(w, b)

    if player == "b":
        b_won = -b_won
        b_close_to_win = -b_close_to_win
        b_count = -b_count
    else:
        w_won = -w_won
        w_close_to_win = -w_close_to_win
        w_count = -w_count

    score = (
        (b_close_to_win + w_close_to_win)
        + (b_won + w_won)
        # + 10 * (w_count + b_count)
    )
    another = not b_close_to_win and not w_close_to_win and not b_won and not w_won
    return score, another


# container to different heuristic
def evaluate_state(state, player):
    score_1, another = custom_heuristic(state, player)
    if another:
        return surface_heuristic(state, player)
    return score_1


