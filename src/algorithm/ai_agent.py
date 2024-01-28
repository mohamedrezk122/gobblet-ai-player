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
        # self.MUTATION = 0.3 if difficulty == "easy" else 0
        self.best_move = None
        self.best_moves = defaultdict(list)
        print("agent difficulty: ", self.max_player, self.difficulty)

    def execute_min_max(self, state, player, depth, alpha, beta):
        if depth == 0 :
            return evaluate_state(state, self.max_player, self.difficulty)

        if player == self.max_player:
            max_score = float("-inf")
            moves, has_winning = state.get_valid_moves(self.max_player, include_winning_moves=(self.difficulty == "hard"))
            if has_winning  and depth == self.max_depth and self.difficulty == "hard":
                self.best_moves = {1:[random.choice(moves)]}
                print("at root")
                return 10000
            for move in moves:
                new_state = state.apply_move(move, self.max_player)
                score = self.execute_min_max(
                    new_state, self.min_player, depth - 1, alpha, beta
                )
                alpha = max(alpha, score)
                # mutation_probabilty = random.random()
                # if depth == self.max_depth and max_score == score and mutation_probabilty >= self.MUTATION:
                #     self.best_move = move
                #     print("max_score", max_score)
                if depth == self.max_depth and score >= max_score :
                    self.best_moves[score].append(move)
                max_score = max(score, max_score)
                if alpha >= beta:
                    break
            return alpha
        else:  # min_player
            min_score = float("inf")
            moves,_ = state.get_valid_moves(self.min_player, include_winning_moves= False)
            for move in moves:
                new_state = state.apply_move(move, self.min_player)
                score = self.execute_min_max(
                    new_state, self.max_player, depth - 1, alpha, beta
                )
                beta = min(score, beta)
                # mutation_probabilty = random.random()
                # if depth == self.max_depth and min_score == score and mutation_probabilty >= self.MUTATION:
                #     self.best_move = move
                # min_score = min(min_score , score)
                if alpha >= beta:
                    break
            return beta

    def play_by_ai(self, state):
        self.best_move = None
        self.best_moves = defaultdict(list)
        alpha = float("-inf")
        beta = float("inf")
        score = self.execute_min_max(
            state, self.max_player, self.max_depth, alpha, beta
        )
        print("len ", len(self.best_moves))
        move = random.choice(self.best_moves[max(self.best_moves)])
        print("score:", score, "player: ", self.max_player)
        return move

