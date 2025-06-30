import pygame
from menu_classes.menu_background import DynamicBackgroundManager
from menu_classes.menu_animations import FadeAnimation
from menu_classes.menu_objects import Text, MenuItem
from menu_classes.menu_music import Slider


def create_intro(screen):
    animator = FadeAnimation(screen)
    try:
        intro = pygame.image.load("assets(menu)/pictures/intro/intro.png").convert_alpha()
        intro = pygame.transform.scale(intro, (600, 600))
    except pygame.error:
        print("Error loading intro image")
        intro = pygame.Surface((600, 600))
        intro.fill((0, 0, 0))

    animator.fade_in(intro, duration = 0)
    pygame.time.delay(0)
    animator.fade_out(intro, duration = 0)
    return animator


def create_background_manager(screen):
    return DynamicBackgroundManager(
        screen,
        folder_path = "assets(menu)/pictures/background",
        prefix = "bg",
        start = 0,
        end = 78,
        change_interval = 0.6
    )


def create_main_menu_elements(game_width, game_height):
    title = Text(
        text = "THE FOG",
        position = (game_width // 2.85 - 25, 250),
        font_path = "assets(menu)/fonts/Boom/boom-boom-8-bit.colr_.ttf",
        font_size = 80,
        color = (255, 255, 255),
        alpha = 255,
    )

    press_any_button = Text(
        text = "press any button",
        position = (game_width // 2.8, 420),
        font_path = "assets(menu)/fonts/GNF/GNF.ttf",
        font_size = 30,
        color = (255, 255, 255),
        alpha = 255,
    )

    menu_items = [
        MenuItem(
            text = "Start",
            position = (game_width // 2.5 - 10, game_height // 5.2),
            font_path = "assets(menu)/fonts/GNF/GNF.ttf",
            font_size = 45
        ),
        MenuItem(
            text = "Settings",
            position = (game_width // 2.5 - 42, game_height // 3.9),
            font_path = "assets(menu)/fonts/GNF/GNF.ttf",
            font_size = 45
        ),
        MenuItem(
            text = "Authors",
            position = (game_width // 2.5 - 40, game_height // 3.13),
            font_path = "assets(menu)/fonts/GNF/GNF.ttf",
            font_size = 45
        ),
        MenuItem(
            text = "Exit",
            position = (game_width // 2.5 + 5, game_height // 2.6),
            font_path = "assets(menu)/fonts/GNF/GNF.ttf",
            font_size = 45
        )
    ]

    return title, press_any_button, menu_items


def create_settings_elements(game_width, game_height, music):
    settings_title = Text(
        text = "SETTINGS",
        position = (game_width // 1.7 - 10, game_height // 15),
        font_path = "assets(menu)/fonts/Boom/boom-boom-8-bit.colr_.ttf",
        font_size = 50
    )

    music_slider = Slider(
        x = game_width // 1.7 + 15,
        y = game_height // 6,
        width = 200,
        height = 10,
        min_val = 0.0,
        max_val = 1.0,
        initial_val = music.volume,
        label = "Music",
        font_path = "assets(menu)/fonts/GNF/GNF.ttf",
        font_size = 25
    )

    sound_slider = Slider(
        x = game_width // 1.7 + 15,
        y = game_height // 4,
        width = 200,
        height = 10,
        min_val = 0.0,
        max_val = 1.0,
        initial_val = 0.5,
        label = "Sound",
        font_path = "assets(menu)/fonts/GNF/GNF.ttf",
        font_size = 25
    )

    back_button = MenuItem(
        text = "Back",
        position = (game_width // 1.5, game_height // 2.7),
        font_path = "assets(menu)/fonts/GNF/GNF.ttf",
        font_size = 35,
        text_color = (255, 255, 255),
        bg_color = (50, 50, 150, 180),
        bg_padding = 10
    )

    return settings_title, music_slider, sound_slider, back_button


def create_authors_elements(game_width, game_height):
    authors_title = Text(
        text = "AUTHORS",
        position = (game_width // 1.7 + 4, game_height // 15),
        font_path = "assets(menu)/fonts/Boom/boom-boom-8-bit.colr_.ttf",
        font_size = 50
    )

    authors_lines = [
        Text(
            text = "Game developed by",
            position = (game_width // 1.7 - 25, game_height // 8),
            font_path = "assets(menu)/fonts/GNF/GNF.ttf",
            font_size = 30,
            color = (255, 255, 255)
        ),
        Text(
            text = "Svetozar Kravchuk",
            position = (game_width // 1.7 - 3, game_height // 7 + 40),
            font_path = "assets(menu)/fonts/GNF/GNF.ttf",
            font_size = 25,
            color = (255, 255, 255)
        ),
        Text(
            text = "Mark Solovyevsky",
            position = (game_width // 1.7 + 5, game_height // 7 + 80),
            font_path = "assets(menu)/fonts/GNF/GNF.ttf",
            font_size = 25,
            color = (255, 255, 255)
        ),
        Text(
            text = "Special thanks to",
            position = (game_width // 1.7 - 15, game_height // 4 + 15),
            font_path = "assets(menu)/fonts/GNF/GNF.ttf",
            font_size = 30,
            color = (255, 255, 255)
        ),
        Text(
            text = "Dmitry Rozhkov",
            position = (game_width // 1.7 + 25, game_height // 3.2 - 10),
            font_path = "assets(menu)/fonts/GNF/GNF.ttf",
            font_size = 25,
            color = (255, 255, 255)
        ),
        Text(
            text = "Artemy Skvortsov",
            position = (game_width // 1.7 + 10, game_height // 3 - 8),
            font_path = "assets(menu)/fonts/GNF/GNF.ttf",
            font_size = 25,
            color = (255, 255, 255)
        ),
        Text(
            text = "Alexander Sobolevsky",
            position = (game_width // 1.7 - 20, game_height // 2.9 + 7),
            font_path = "assets(menu)/fonts/GNF/GNF.ttf",
            font_size = 25,
            color = (255, 255, 255)
        ),
        Text(
            text="...",
            position=(game_width // 1.7, game_height // 2.7),
            font_path="assets(menu)/fonts/GNF/GNF.ttf",
            font_size=25,
            color=(255, 255, 255)
        )
    ]

    authors_back_button = MenuItem(
        text = "Back",
        position = (game_width // 1.5, game_height // 2.4),
        font_path = "assets(menu)/fonts/GNF/GNF.ttf",
        font_size = 35,
        text_color = (255, 255, 255),
        bg_color = (50, 50, 150, 180),
        bg_padding = 10
    )

    return authors_title, authors_lines, authors_back_button


def create_game_start_elements(game_width, game_height):
    next_button = MenuItem(
        text = "NEXT",
        position = (game_width // 1.1, game_height // 1.1),
        font_path = "assets(menu)/fonts/GNF/GNF.ttf",
        font_size = 35,
        text_color = (255, 255, 255),
        bg_color = (50, 50, 150, 180),
        bg_padding = 10
    )
    return next_button

def create_game_intro_text(game_width, game_height):
    font = pygame.font.Font("assets(menu)/fonts/Epilepsy Sans/EpilepsySans.ttf", 35)
    intro_text = font.render("Жизнь — это испытание, это подготовка и анализ, но большинство просто приспосабливается и тонет в рутине", True, (255, 255, 255))
    intro_text.set_alpha(0)
    text_rect = intro_text.get_rect(center=(game_width // 2, game_height // 2))

    return intro_text, text_rect

def adjust_comic_position(game_width, game_height):
    positions = [
        (game_width * 0.1, game_height * 0.03),
        (game_width * 0.1, game_height * 0.08)
    ]

    return positions
