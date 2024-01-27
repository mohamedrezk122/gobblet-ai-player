import pygame
import pygame_menu as pgm
import os
import sys

from src.gui.board import Board 
from src.algorithm.state import State 
from src.algorithm.ai_agent import AI_Agent
from src.algorithm.check_winner import check_winner


cli =  0
if not cli :
    from src.gui.menu import * 
    from src.gui.constants import * 
    from src.gui.game import Game 

    game = Game(game_window)


    mode_selector.set_onchange(game.set_game_mode)
    difficulty_selector.set_onchange(game.set_difficulty)


    def game_loop():
        start_ticks=pygame.time.get_ticks()
        while True:
            DISPLAY.fill("#252525")
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()
            if main_menu.is_enabled():
                main_menu.update(events)
                main_menu.draw(DISPLAY)

            if game_window.is_enabled():
                seconds=(pygame.time.get_ticks()-start_ticks)/1000 
                if seconds > 2 :
                    game.play(events)

            pygame.display.flip()
    game_loop()

#cli 
else :
    board = Board()
    state = State(board.abstract_board, board.stacks)

    w_agent  = AI_Agent("w", "easy")
    b_agent  = AI_Agent("b", "hard")
    player = "w"
    winner = False
    while not winner:
        if player == "w": 
            ai_move = w_agent.play_by_ai(state)
        else:
            ai_move = b_agent.play_by_ai(state)
        print(player, ai_move, ai_move.piece.aside_stack)
        print("-"*30)
        state = state.apply_move(ai_move,ai_move.piece.player)
        winner = check_winner(state)
        if winner :
            break
        print(state.board)
        print("-"*30)
        print(state.stacks[player])
        player = "w" if player == "b" else "b"
        print("*"*30)
    print(check_winner(state))


# ai_move = w_agent.play_by_ai(state)

# new_state = state.apply_move(ai_move, "w")
# print(ai_move)
# print(state.stacks)
# print("-------------------------------")
# print(new_state.stacks)
# print("-------------------------------")
# print(state.board)
# print("-------------------------------")
# print(new_state.board)