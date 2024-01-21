import pygame
import pygame_menu as pgm

from gui.menu import * 
from gui.constants import * 
from gui.game import Game 
from gui.ai_agent import Logic 

game = Game(game_window)


mode_selector.set_onchange(game.set_game_mode)
difficulty_selector.set_onchange(game.set_difficulty)


def game_loop():
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
            game.play(events)

        pygame.display.flip()


game_loop()
