import pygame
from menu_classes.menu_animations import GlitchEffect
from menu_classes.menu_objects import Objects
from menu_classes.menu_music import Music
from menu_things.secrets import setup_secrets
from menu_things.menu_ui import (
    create_main_menu_elements,
    create_settings_elements,
    create_authors_elements,
    create_game_start_elements,
    create_intro,
    create_background_manager,
    create_game_intro_text
)

pygame.init()

# Setting the screen resolution
GAME_WIDTH, GAME_HEIGHT = 1920, 1080
info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
game_surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))

# Intro & Background
create_intro(screen)
background_manager = create_background_manager(screen)
background_manager.start()

# Launch music
music = Music()
music.play_loop()

# Create menu elements
title, press_any_button, menu_items = create_main_menu_elements(GAME_WIDTH, GAME_HEIGHT)
settings_title, music_slider, sound_slider, back_button = create_settings_elements(GAME_WIDTH, GAME_HEIGHT, music)
authors_title, authors_lines, authors_back_button = create_authors_elements(GAME_WIDTH, GAME_HEIGHT)
next_button = create_game_start_elements(GAME_WIDTH, GAME_HEIGHT)

text_alpha = 0
text_target_alpha = 255
text_fade_speed = 2
fade_out_speed = 2
menu_alpha = 0
menu_fade_speed = 5
objects_manager = Objects()
setup_secrets(objects_manager, GAME_WIDTH, GAME_HEIGHT)
sound_volume = 0.5
switch_sound = pygame.mixer.Sound("assets(menu)/audio/navigation/switch.mp3")
switch_sound.set_volume(sound_volume)
select_sound = pygame.mixer.Sound("assets(menu)/audio/navigation/select.mp3")
select_sound.set_volume(sound_volume)

# Launch
pygame.display.set_caption("THE FOG")
running = True
clock = pygame.time.Clock()

# Flags of activities
glitch_effect = None
show_text = True
take_snapshot = False
menu_active = False
menu_visible = False
key_pressed = False
settings_active = False
authors_active = False
game_start_active = False
intro_text_finished = False
current_state = "main_menu"
selected_index = 0
settings_alpha = 0
authors_alpha = 0
game_start_alpha = 0
selected_setting_index = 0
selected_authors_index = 0
selected_game_start_index = -1

# For GAME START
current_image_index = 0
game_images = []
dark_image_path = "assets(menu)/pictures/comic/dark.jpg"
game_images_paths = [
    "assets(menu)/pictures/comic/bg0.png",
    "assets(menu)/pictures/comic/bg38.png",
]

intro_text, intro_text_rect = create_game_intro_text(GAME_WIDTH, GAME_HEIGHT)
intro_text_alpha = 0
intro_text_start_time = 0
intro_text_duration = 4000
intro_text_shown = False

# Drawing images in the start menu
dark_image = pygame.image.load(dark_image_path).convert_alpha()
for path in game_images_paths:
    img = pygame.image.load(path).convert_alpha()
    game_images.append(img)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            music.stop()
            background_manager.stop()

        # Handling mouse release
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            music_slider.dragging = False
            sound_slider.dragging = False

        # Preventing the processing of a single event in multiple states
        if current_state == "main_menu":
            if event.type == pygame.KEYDOWN and show_text:
                show_text = False
                menu_visible = True
                selected_index = 0

            # Menu navigation
            if event.type == pygame.KEYDOWN and menu_active:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(menu_items)
                    if switch_sound: switch_sound.play()
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(menu_items)
                    if switch_sound: switch_sound.play()
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    if select_sound: select_sound.play()
                    if selected_index == 0:
                        current_state = "game_start"
                        take_snapshot = True
                        current_image_index = 0
                    elif selected_index == 1:
                        current_state = "settings"
                        settings_active = True
                        selected_setting_index = 0
                    elif selected_index == 2:
                        current_state = "authors"
                        authors_active = True
                    elif selected_index == 3:
                        running = False

            # Mouse Processing
            if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION):
                mouse_x, mouse_y = pygame.mouse.get_pos()
                game_x = mouse_x * GAME_WIDTH / SCREEN_WIDTH
                game_y = mouse_y * GAME_HEIGHT / SCREEN_HEIGHT
                objects_manager.handle_event(event, (game_x, game_y), sound_volume)

                # Selecting a menu item
                if menu_active:
                    if event.type == pygame.MOUSEMOTION:
                        for i, item in enumerate(menu_items):
                            if item.bg_rect.collidepoint(game_x, game_y):
                                if i != selected_index and switch_sound:
                                    switch_sound.play()
                                selected_index = i
                                break

                    # Activating menu items
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        for i, item in enumerate(menu_items):
                            if item.bg_rect.collidepoint(game_x, game_y):
                                if select_sound: select_sound.play()
                                if i == 0:
                                    current_state = "game_start"
                                    take_snapshot = True
                                    current_image_index = 0
                                elif i == 1:
                                    current_state = "settings"
                                    selected_setting_index = 0
                                    settings_active = True
                                elif i == 2:
                                    current_state = "authors"
                                    authors_active = True
                                    selected_authors_index = 0
                                elif i == 3:
                                    running = False
                                break

        # Event handling in settings
        elif current_state == "settings":
            if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION):
                mouse_x, mouse_y = pygame.mouse.get_pos()
                game_x = mouse_x * GAME_WIDTH / SCREEN_WIDTH
                game_y = mouse_y * GAME_HEIGHT / SCREEN_HEIGHT

                # Updating the selected item on hover
                if event.type == pygame.MOUSEMOTION:
                    if music_slider.rect.collidepoint(game_x, game_y) or \
                            pygame.Rect(music_slider.rect.x, music_slider.rect.y - 40,
                                        music_slider.rect.width, 40).collidepoint(game_x, game_y):
                        selected_setting_index = 0
                    elif sound_slider.rect.collidepoint(game_x, game_y) or \
                            pygame.Rect(sound_slider.rect.x, sound_slider.rect.y - 40,
                                        sound_slider.rect.width, 40).collidepoint(game_x, game_y):
                        selected_setting_index = 1
                    elif back_button.bg_rect.collidepoint(game_x, game_y):
                        selected_setting_index = 2

                # Slider processing
                music_slider.handle_event(event, (game_x, game_y))
                sound_slider.handle_event(event, (game_x, game_y))

                # "Back" processing
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if back_button.bg_rect.collidepoint(game_x, game_y):
                        if select_sound: select_sound.play()
                        current_state = "main_menu"
                        settings_active = False

            # Keyboard handling in settings
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_w, pygame.K_UP]:
                    selected_setting_index = (selected_setting_index - 1) % 3
                    if switch_sound: switch_sound.play()
                elif event.key in [pygame.K_s, pygame.K_DOWN]:
                    selected_setting_index = (selected_setting_index + 1) % 3
                    if switch_sound: switch_sound.play()
                elif event.key in [pygame.K_a, pygame.K_LEFT]:
                    if selected_setting_index == 0:
                        new_val = max(0.0, music_slider.val - 0.05)
                        music_slider.val = new_val
                        music_slider.knob_x = music_slider.rect.left + (new_val - music_slider.min_val) / (
                                music_slider.max_val - music_slider.min_val) * music_slider.rect.width
                        if switch_sound: switch_sound.play()
                    elif selected_setting_index == 1:
                        new_val = max(0.0, sound_slider.val - 0.05)
                        sound_slider.val = new_val
                        sound_slider.knob_x = sound_slider.rect.left + (new_val - sound_slider.min_val) / (
                                sound_slider.max_val - sound_slider.min_val) * sound_slider.rect.width
                        if switch_sound: switch_sound.play()
                elif event.key in [pygame.K_d, pygame.K_RIGHT]:
                    if selected_setting_index == 0:
                        new_val = min(1.0, music_slider.val + 0.05)
                        music_slider.val = new_val
                        music_slider.knob_x = music_slider.rect.left + (new_val - music_slider.min_val) / (
                                music_slider.max_val - music_slider.min_val) * music_slider.rect.width
                        if switch_sound: switch_sound.play()
                    elif selected_setting_index == 1:
                        new_val = min(1.0, sound_slider.val + 0.05)
                        sound_slider.val = new_val
                        sound_slider.knob_x = sound_slider.rect.left + (new_val - sound_slider.min_val) / (
                                sound_slider.max_val - sound_slider.min_val) * sound_slider.rect.width
                        if switch_sound: switch_sound.play()
                elif event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                    if selected_setting_index == 2:
                        if select_sound: select_sound.play()
                        current_state = "main_menu"
                        settings_active = False
                elif event.key == pygame.K_ESCAPE:
                    clear_menus()
                    current_state = "main_menu"

        # Event handling in authors
        elif current_state == "authors":
            if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION):
                mouse_x, mouse_y = pygame.mouse.get_pos()
                game_x = mouse_x * GAME_WIDTH / SCREEN_WIDTH
                game_y = mouse_y * GAME_HEIGHT / SCREEN_HEIGHT
                if event.type == pygame.MOUSEMOTION:
                    if authors_back_button.bg_rect.collidepoint(game_x, game_y):
                        selected_authors_index = 0
                    else:
                        selected_authors_index = -1

                # Click handling
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if authors_back_button.bg_rect.collidepoint(game_x, game_y):
                        if select_sound: select_sound.play()
                        current_state = "main_menu"

            # Keyboard handling in authors
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    if selected_authors_index == 0:
                        if select_sound: select_sound.play()
                        clear_menus()
                        current_state = "main_menu"
                elif event.key == pygame.K_ESCAPE:
                    clear_menus()
                    current_state = "main_menu"

        # GAME LAUNCH
        elif current_state == "game_start":
            # Mouse Processing
            if current_image_index > 0:
                if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION):
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    game_x = mouse_x * GAME_WIDTH / SCREEN_WIDTH
                    game_y = mouse_y * GAME_HEIGHT / SCREEN_HEIGHT

                    # Updating the selected item on hover
                    if event.type == pygame.MOUSEMOTION:
                        if next_button.bg_rect.collidepoint(game_x, game_y):
                            selected_game_start_index = 0
                        else:
                            selected_game_start_index = -1

                    # Click processing
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if next_button.bg_rect.collidepoint(game_x, game_y):
                            if select_sound: select_sound.play()
                            current_image_index += 1
                            if current_image_index > len(game_images):
                                print("Starting actual game...")
                                current_state = "main_menu"
                                background_manager.start()
                                music.play_loop()
                                game_start_active = False
                                current_image_index = 0
                                intro_text_shown = False
                                intro_text_alpha = 0
                                intro_text_finished = False

            # Keyboard handling for NEXT and ESC only
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_RETURN,
                                 pygame.K_SPACE] and current_image_index > 0:
                    if select_sound: select_sound.play()
                    current_image_index += 1
                    if current_image_index > len(game_images):
                        print("Starting actual game...")
                        current_state = "main_menu"
                        background_manager.start()
                        music.play_loop()
                        game_start_active = False
                        current_image_index = 0
                        intro_text_shown = False
                        intro_text_alpha = 0
                        intro_text_finished = False
                elif event.key == pygame.K_ESCAPE:
                    current_state = "main_menu"
                    background_manager.start()
                    music.play_loop()
                    game_start_active = False
                    current_image_index = 0
                    intro_text_shown = False
                    intro_text_alpha = 0
                    intro_text_finished = False


    # Cleaner
    def clear_menus():
        global selected_authors_index, selected_game_start_index
        selected_authors_index = -1
        selected_game_start_index = -1


    # Drawing
    if current_state in ["main_menu", "settings", "authors", "prepare_glitch"]:
        current_bg = background_manager.get_current_background()
        if current_bg:
            game_surface.blit(current_bg, (0, 0))

    if current_state in ["main_menu", "settings", "authors", "prepare_glitch"]:
        objects_manager.draw(game_surface)

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
        highlight_active = current_state == "main_menu"

        for i, item in enumerate(menu_items):
            item.set_alpha(menu_alpha)
            item.set_active(i == selected_index and highlight_active)
            item.draw(game_surface)

    if current_state == "settings":
        if settings_alpha < 255:
            settings_alpha = min(settings_alpha + 5, 255)
    else:
        if settings_alpha > 0:
            settings_alpha = max(settings_alpha - 5, 0)

    if current_state == "settings":
        music.set_volume(music_slider.get_value())
        sound_volume = sound_slider.get_value()
        switch_sound.set_volume(sound_volume)
        select_sound.set_volume(sound_volume)

    if current_state == "settings":
        music_slider.set_active(selected_setting_index == 0)
        sound_slider.set_active(selected_setting_index == 1)
        back_button.set_active(selected_setting_index == 2)

    if settings_alpha > 0:
        settings_title.set_alpha(settings_alpha)
        settings_title.draw(game_surface)
        music_slider.set_alpha(settings_alpha)
        music_slider.draw(game_surface)
        sound_slider.set_alpha(settings_alpha)
        sound_slider.draw(game_surface)
        back_button.set_alpha(settings_alpha)
        back_button.draw(game_surface)

    if current_state == "authors":
        if authors_alpha < 255:
            authors_alpha = min(authors_alpha + 5, 255)
    else:
        if authors_alpha > 0:
            authors_alpha = max(authors_alpha - 5, 0)

    if authors_alpha > 0:
        authors_title.set_alpha(authors_alpha)
        authors_title.draw(game_surface)

        for line in authors_lines:
            line.set_alpha(authors_alpha)
            line.draw(game_surface)

        authors_back_button.set_alpha(authors_alpha)
        authors_back_button.set_active(selected_authors_index == 0)
        authors_back_button.draw(game_surface)

    if current_state == "game_start":
        game_surface.fill((0, 0, 0))
        if current_image_index == 0:
            game_surface.blit(dark_image, (0, 0))
        elif 0 < current_image_index <= len(game_images):
            game_surface.blit(game_images[current_image_index - 1], (0, 0))

        if current_image_index == 0:
            if not intro_text_shown:
                intro_text_alpha = min(intro_text_alpha + 3, 255)
                intro_text.set_alpha(intro_text_alpha)
                if intro_text_alpha == 255:
                    intro_text_shown = True
                    intro_text_start_time = pygame.time.get_ticks()

            if intro_text_shown and (pygame.time.get_ticks() - intro_text_start_time) > intro_text_duration:
                intro_text_alpha = max(intro_text_alpha - 3, 0)
                intro_text.set_alpha(intro_text_alpha)
                if intro_text_alpha == 0:
                    intro_text_finished = True
                    current_image_index = 1

            if intro_text_alpha > 0:
                game_surface.blit(intro_text, intro_text_rect)

        if current_image_index >= 1 and current_image_index <= len(game_images):
            next_button.set_alpha(255)
            next_button.set_active(selected_game_start_index == 0)
            next_button.draw(game_surface)

    if take_snapshot:
        glitch_base = game_surface.copy()
        glitch_effect = GlitchEffect(screen, glitch_base, duration = 1.0)
        background_manager.stop()
        music.stop()
        current_state = "glitch_effect"
        take_snapshot = False

    if current_state == "glitch_effect":
        glitch_frame, finished = glitch_effect.update()
        game_surface.blit(glitch_frame, (0, 0))

        if finished:
            current_state = "game_start"
            game_start_active = True
            current_image_index = 0
            glitch_effect = None


    objects_manager.draw(game_surface)
    scaled_surface = pygame.transform.scale(game_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_surface, (0, 0))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
