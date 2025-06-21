import pygame
from menu_classes.menu_objects import (Objects, InteractiveObject, Text, MenuItem)
from menu_classes.menu_background import DynamicBackgroundManager
from menu_classes.menu_animations import FadeAnimation
from menu_classes.menu_music import (Music, Slider)
from secrets import setup_secrets
pygame.init()


# Setting the screen resolution
GAME_WIDTH, GAME_HEIGHT = 1920, 1080
info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
game_surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))


# Intro
animator = FadeAnimation(screen)
intro = pygame.image.load("assets(menu)/pictures/intro/intro.png").convert_alpha()
intro = pygame.transform.scale(intro, (600, 600))
animator.fade_in(intro, duration = 3)
pygame.time.delay(3000)
animator.fade_out(intro, duration = 3)


# Background
background_manager = DynamicBackgroundManager(
    screen,
    folder_path="assets(menu)/pictures/background",
    prefix="bg",
    start=0,
    end=38,
    change_interval=0.6
)
background_manager.start()


# Launch music
music = Music()
music.play_loop()


# Create Game Menu
title = Text(
    font_path = "assets(menu)/fonts/Boom/boom-boom-8-bit.colr_.ttf",
    font_size = 80,
    text = "THE FOG",
    color = (255, 255, 255),
    position = (GAME_WIDTH//2.85 - 25, 250),
    alpha = 255,
)
press_any_button = Text(
    font_path = "assets(menu)/fonts/GNF/GNF.ttf",
    font_size = 30,
    text = "press any button",
    color = (255, 255, 255),
    position = (GAME_WIDTH//2.8, 420),
    alpha = 255,
)

menu_items = [
    MenuItem(
        font_path = "assets(menu)/fonts/GNF/GNF.ttf",
        font_size = 45,
        text = "Start",
        position = (GAME_WIDTH//2.5 - 10, GAME_HEIGHT//5.2),
    ),
    MenuItem(
        font_path = "assets(menu)/fonts/GNF/GNF.ttf",
        font_size = 45,
        text = "Settings",
        position = (GAME_WIDTH//2.5 - 42, GAME_HEIGHT//3.9),
    ),
    MenuItem(
        font_path = "assets(menu)/fonts/GNF/GNF.ttf",
        font_size = 45,
        text = "Control",
        position = (GAME_WIDTH//2.5 - 33, GAME_HEIGHT//3.13),
    ),
    MenuItem(
        font_path = "assets(menu)/fonts/GNF/GNF.ttf",
        font_size = 45,
        text = "Exit",
        position = (GAME_WIDTH//2.5 + 5, GAME_HEIGHT//2.6),
    )
]
text_alpha = 0
text_target_alpha = 255
text_fade_speed = 2
fade_out_speed = 3
menu_alpha = 0
menu_fade_speed = 5
objects_manager = Objects()
setup_secrets(objects_manager, GAME_WIDTH, GAME_HEIGHT)
select_sound = pygame.mixer.Sound("assets(menu)/audio/navigation/switch.mp3")
activate_sound = pygame.mixer.Sound("assets(menu)/audio/navigation/select.mp3")


# Launch
pygame.display.set_caption("THE FOG")
running = True
clock = pygame.time.Clock()

show_text = True
menu_active = False
menu_visible = False
key_pressed = False
selected_index = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            music.stop()
            background_manager.stop()

        # Processing of pressing any key (except the mouse)
        if event.type == pygame.KEYDOWN and show_text:
            show_text = False
            menu_visible = True
            selected_index = 0

        # Handling menu navigation
        if event.type == pygame.KEYDOWN and menu_active:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                selected_index = (selected_index - 1) % len(menu_items)
                if select_sound: select_sound.play()
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                selected_index = (selected_index + 1) % len(menu_items)
                if select_sound: select_sound.play()
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                if activate_sound: activate_sound.play()
                if selected_index == 0:
                    print("Start button")
                elif selected_index == 1:
                    print("Settings button")
                elif selected_index == 2:
                    print("Control button")
                elif selected_index == 3:
                    running = False

        # Mouse Processing
        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION):
            mouse_x, mouse_y = pygame.mouse.get_pos()
            game_x = mouse_x * GAME_WIDTH / SCREEN_WIDTH
            game_y = mouse_y * GAME_HEIGHT / SCREEN_HEIGHT
            objects_manager.handle_event(event, (game_x, game_y))

            # Selecting a menu item with the mouse
            if menu_active:
                if event.type == pygame.MOUSEMOTION:
                    for i, item in enumerate(menu_items):
                        if item.bg_rect.collidepoint(game_x, game_y):
                            if i != selected_index and select_sound:
                                select_sound.play()
                            selected_index = i
                            break

                # Processing a mouse click to activate items
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for i, item in enumerate(menu_items):
                        if item.bg_rect.collidepoint(game_x, game_y):
                            if activate_sound: activate_sound.play()
                            if i == 0:  # Start
                                print("Starting game...")
                            elif i == 1:  # Settings
                                print("Opening settings...")
                            elif i == 2:  # Authors
                                print("Showing authors...")
                            elif i == 3:  # Exit
                                running = False
                            break

    # Drawing
    current_bg = background_manager.get_current_background()
    if current_bg:
        game_surface.blit(current_bg, (0, 0))

    # Control game menu
    if show_text:
        if text_alpha < text_target_alpha:
            text_alpha = min(text_alpha + text_fade_speed, text_target_alpha)
            title.set_alpha(text_alpha)
            press_any_button.set_alpha(text_alpha)
    else:
        if text_alpha > 0:
            text_alpha = max(0, text_alpha - text_fade_speed)
            title.set_alpha(text_alpha)
            press_any_button.set_alpha(text_alpha)


        elif menu_visible and menu_alpha < 255:
            menu_alpha = min(menu_alpha + menu_fade_speed, 255)
            if menu_alpha == 255:
                menu_active = True

    if text_alpha > 0:
        title.draw(game_surface)
        press_any_button.draw(game_surface)

    if menu_alpha > 0:
        for i, item in enumerate(menu_items):
            item.set_alpha(menu_alpha)
            item.set_active(i == selected_index)
            item.draw(game_surface)

    objects_manager.draw(game_surface)
    scaled_surface = pygame.transform.scale(game_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_surface, (0, 0))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
