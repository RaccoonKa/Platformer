import pygame
from menu_classes import (FadeAnimation, Music,
                          Background, InteractiveObject, Objects, Text,
                          MenuItem)

pygame.init()

# Setting the screen resolution
GAME_WIDTH, GAME_HEIGHT = 1920, 1080
info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
game_surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))

custom_background_order = [
    "assets(menu)/pictures/background/bg0.png",
    "assets(menu)/pictures/background/bg1.png",
    "assets(menu)/pictures/background/bg2.png",
    "assets(menu)/pictures/background/bg3.png",
    "assets(menu)/pictures/background/bg4.png",
    "assets(menu)/pictures/background/bg5.png",
    "assets(menu)/pictures/background/bg6.png",
    "assets(menu)/pictures/background/bg7.png",
    "assets(menu)/pictures/background/bg8.png",
    "assets(menu)/pictures/background/bg9.png",
    "assets(menu)/pictures/background/bg10.png",
]

# Launch classes
animator = FadeAnimation(screen)
music = Music()
background_manager = Background(screen, image_paths = custom_background_order, change_interval = 0.6)
background_manager.start()
objects_manager = Objects()

# Intro
intro = pygame.image.load("assets(menu)/pictures/intro/intro.png").convert_alpha()
intro = pygame.transform.scale(intro, (600, 600))
animator.fade_in(intro, duration = 3)
pygame.time.delay(3000)
animator.fade_out(intro, duration = 3)

# Background
background = pygame.image.load("assets(menu)/pictures/background/bg0.png").convert()
background = pygame.transform.scale(background, (GAME_WIDTH, GAME_HEIGHT))

# Launch music
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

# Create SECRET objects

coon = InteractiveObject(
    x = GAME_WIDTH // 1.2 + 10,
    y = GAME_HEIGHT // 2.5,
    shape = "rect",
    width = 250,
    height = 400,
    sound_path="assets(menu)/audio/secrets/coon.mp3"
)
objects_manager.add(coon)

keyboard = InteractiveObject(
    x = GAME_WIDTH // 2.17,
    y = GAME_HEIGHT // 1.22,
    shape = "rect",
    width = 515,
    height = 120,
    angle = 9,
    sound_path="assets(menu)/audio/secrets/keyboard.mp3"
)
objects_manager.add(keyboard)

mouse = InteractiveObject(
    x = GAME_WIDTH // 1.618,
    y = GAME_HEIGHT // 1.38,
    shape = "rect",
    width = 100,
    height = 50,
    angle = 312,
    sound_path="assets(menu)/audio/secrets/mouse.wav"
)
objects_manager.add(mouse)

floppy_disk = InteractiveObject(
    x = GAME_WIDTH // 1.1 + 55,
    y = GAME_HEIGHT // 1.1 - 60,
    shape = "rect",
    width = 150,
    height = 150,
    angle = 293,
    sound_path="assets(menu)/audio/secrets/floppy_disk.mp3"
)
objects_manager.add(floppy_disk)

phone = InteractiveObject(
    x = GAME_WIDTH // 2.9,
    y = GAME_HEIGHT // 1.51,
    shape = "rect",
    width = 140,
    height = 65,
    angle = 35,
    sound_path="assets(menu)/audio/secrets/phone.mp3"
)
objects_manager.add(phone)

stone_face = InteractiveObject(
    x = GAME_WIDTH // 4.65,
    y = GAME_HEIGHT // 2.5,
    shape = "rect",
    width = 250,
    height = 180,
    angle = 90,
    sound_path="assets(menu)/audio/secrets/face.mp3"
)
objects_manager.add(stone_face)

moon = InteractiveObject(
    x = GAME_WIDTH // 1.07,
    y = GAME_HEIGHT // 45,
    shape = "circle",
    width = 300,
    height = 250,
    sound_path="assets(menu)/audio/secrets/moon.mp3"
)
objects_manager.add(moon)

capybara = InteractiveObject(
    x = GAME_WIDTH // 1 - 90,
    y = GAME_HEIGHT // 1.7 - 20,
    shape = "circle",
    width = 150,
    height = 150,
    sound_path="assets(menu)/audio/secrets/capybara.mp3"
)
objects_manager.add(capybara)

coffee = InteractiveObject(
    x = GAME_WIDTH // 6,
    y = GAME_HEIGHT // 1.36,
    shape = "rect",
    width = 180,
    height = 180,
    angle = 90,
    sound_path="assets(menu)/audio/secrets/coffee.mp3"
)
objects_manager.add(coffee)

candy = InteractiveObject(
    x = GAME_WIDTH // 13,
    y = GAME_HEIGHT // 1.27,
    shape = "rect",
    width = 100,
    height = 50,
    angle = 312,
    sound_path="assets(menu)/audio/secrets/candy.mp3"
)
objects_manager.add(candy)

chair1 = InteractiveObject(
    x = GAME_WIDTH // 1.38,
    y = GAME_HEIGHT // 1.1,
    shape = "rect",
    width = 570,
    height = 400,
    angle = 64,
    sound_path="assets(menu)/audio/secrets/chair.mp3"
)
objects_manager.add(chair1)
objects_manager.add_special(chair1, "assets(menu)/audio/secrets/chair_falling.mp3")

chair2 = InteractiveObject(
    x = GAME_WIDTH // 1.25 + 10,
    y = GAME_HEIGHT // 1.5,
    shape = "rect",
    width = 380,
    height = 160,
    sound_path="assets(menu)/audio/secrets/chair.mp3"
)
objects_manager.add(chair2)
objects_manager.add_special(chair2, "assets(menu)/audio/secrets/chair_falling.mp3")

# Launch
pygame.display.set_caption("THE FOG")
running = True
clock = pygame.time.Clock()

# Flags
show_text = True
menu_active = False
menu_visible = False
key_pressed = False
selected_index = 0

# Sounds switch parts of menu
select_sound = pygame.mixer.Sound("assets(menu)/audio/navigation/switch.mp3")
activate_sound = pygame.mixer.Sound("assets(menu)/audio/navigation/select.mp3")

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
