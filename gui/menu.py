import pygame
import pygame_menu as pgm

from .board import Board
from .game import Game
from .constants import *
from .themes import *

pygame.init()

DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))

game_window = pgm.Menu(
    title="",
    width=WIDTH,
    height=HEIGHT,
    theme=game_theme,
    enabled=False,
    mouse_motion_selection=True,
    center_content=False,
    overflow=False,
    position=(0, 0),
)


main_menu = pgm.Menu(
    title="Gobblet Game",
    width=WIDTH,
    height=HEIGHT,
    theme=main_menu_theme,
    mouse_motion_selection=True,
    onclose=pgm.events.EXIT,
    position=(0, 0, False),
    verbose=False,
)


play_button = main_menu.add.button("Play", game_window)

mode_selector = main_menu.add.selector(
    "Mode: ",
    [("Human vs Human", 0), ("Human vs AI", 1), ("AI vs AI", 2)],
    onchange=None,
)

difficulty_selector = main_menu.add.selector(
    "Difficulty: ",
    [("Easy-Easy", 0), ("Hard-Easy", 1), ("Easy-Hard", 2), ("Hard-Hard", 3)],
    onchange=None,
)
quit_button = main_menu.add.button("Quit", pgm.events.EXIT)
