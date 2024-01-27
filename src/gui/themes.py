import pygame
import pygame_menu as pgm

background_image = pgm.baseimage.BaseImage(
    image_path="./src/gui/assets/menu_image.png",
    drawing_mode=pgm.baseimage.IMAGE_MODE_CENTER,
    drawing_offset=(10, 230),
).scale(0.8, 0.8, smooth=True)


main_menu_theme_attributes = {
    "background_color": background_image,
    "title_font": pgm.font.FONT_8BIT,
    "title_bar_style": pgm.widgets.MENUBAR_STYLE_SIMPLE,
    "title_font_color": "#ffffff",
    "title_background_color": "#10000000",
    "title_close_button": True,
    "title_offset": (190, 30),
    "widget_font_size": 54,
    "widget_font": pgm.font.FONT_MUNRO,
    "widget_font_color": "#595757",
    "widget_offset": (0, 100),
    "widget_padding": (20, 90),
}

game_theme_attributes = {
    "background_color": "#252525",
    "title_floating": True,
    "title_close_button": True,
    "title_font": pgm.font.FONT_8BIT,
    "title_font_size": 50,
    "title_bar_style": pgm.widgets.MENUBAR_STYLE_SIMPLE,
    "title_font_color": "#ffffff",
    "title_background_color": "#10000000",
    "title_close_button": True,
    "title_offset": (0, 0),
    "widget_font_size": 10,
    "widget_font": pgm.font.FONT_MUNRO,
    "widget_font_color": "#595757",
    "widget_offset": (0, 0),
    "widget_padding": (0, 0),
}


main_menu_theme = pgm.Theme(**main_menu_theme_attributes)
game_theme = pgm.Theme(**game_theme_attributes)
