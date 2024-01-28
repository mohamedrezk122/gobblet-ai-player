from dataclasses import dataclass
from collections import defaultdict
import random

from .heuristics import *
from .state import State


class AI_Agent:
    def __init__(self, player, difficulty="easy"):
        self.max_player = player
        self.min_player = "w" if self.max_player == "b" else "b"
        self.difficulty_to_depth = {
            "hard": 3,
            "easy": 2,
        }
        self.max_depth = self.difficulty_to_depth[difficulty]
        self.difficulty = difficulty
        self.is_first_move  = True
        print("agent difficulty: ", self.max_player, self.difficulty)

    def execute_min_max(self, state, player, depth, alpha, beta):
        if depth == 0 :
            p = self.max_player if self.max_depth % 2 == 0 else self.min_player
            return evaluate_state(state, p)

        if player == self.max_player:
            score = float("-inf")
            moves, has_winning = state.get_valid_moves(self.max_player, include_winning_moves=False)
            for move in moves:
                state.apply_move(move, self.max_player)
                score = self.execute_min_max(
                    state, self.min_player, depth - 1, alpha, beta
                )
                state.undo_move(move, self.max_player)
                if score >= beta:
                    return score
                alpha = max(alpha, score)
            return score
        else:  # min_player
            score = float("inf")
            moves,_ = state.get_valid_moves(self.min_player, include_winning_moves= False)
            for move in moves:
                state.apply_move(move, self.min_player)
                score = self.execute_min_max(
                    state, self.max_player, depth - 1, alpha, beta
                )
                state.undo_move(move, self.min_player)
                if alpha >= score:
                    return score
                beta = min(score, beta)
            return score

    def play_by_ai(self, state):
        self.best_moves = defaultdict(list)
        best_move  = None
        alpha = float("-inf")
        beta = float("inf")
        max_score = float("-inf")
        moves, has_winning = state.get_valid_moves(self.max_player, self.difficulty=="hard")
        if self.is_first_move:
            print("first here")
            self.is_first_move = False
            return random.choice(moves)

        if has_winning and self.difficulty=="hard":
            return random.choice(moves)
        for move in moves:
            state.apply_move(move, self.max_player)
            score = self.execute_min_max(
                state, self.min_player, self.max_depth-1, alpha, beta
            )
            state.undo_move(move, self.max_player)
            if score > max_score:
                max_score = score
                self.best_moves[score].append(move)
                best_move = move
        best_move = random.choice(self.best_moves[max(self.best_moves)])
        print("score:", max_score, "player: ", self.max_player, "move:", best_move)
        return best_move

