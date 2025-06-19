import pygame
from menu_classes import FadeAnimation, Music, Background, InteractiveObject

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
background_manager = Background(screen, image_paths=custom_background_order, change_interval=1.0)
background_manager.start()

# Intro
intro = pygame.image.load("assets(menu)/pictures/intro/intro.png").convert_alpha()
intro = pygame.transform.scale(intro, (600, 600))
animator.fade_in(intro, duration=0)
pygame.time.delay(100)
animator.fade_out(intro, duration=0)

# Background
background = pygame.image.load("assets(menu)/pictures/background/bg0.png").convert()
background = pygame.transform.scale(background, (GAME_WIDTH, GAME_HEIGHT))

# Launch music
music.play_loop()

# Create objects
interactive_objects = [
    InteractiveObject(
        x=625, y=660,
        width=100, height=90,
        sound_path="assets(menu)/audio/secrets/phone.mp3",
    ),
    InteractiveObject(
        x=700, y=300,
        width=150, height=150,
        sound_path="assets(menu)/audio/secrets/face.mp3"
    )
]

pygame.display.set_caption("GAME_MENU")
running = True
clock = pygame.time.Clock()

while running:
    scale_x = SCREEN_WIDTH / GAME_WIDTH
    scale_y = SCREEN_HEIGHT / GAME_HEIGHT
    mouse_pos = pygame.mouse.get_pos()
    mouse_clicked = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            music.stop()
            background_manager.stop()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_clicked = True

    current_bg = background_manager.get_current_background()
    if current_bg:
        game_surface.blit(current_bg, (0, 0))

    # Debug
    for obj in interactive_objects:
        obj.check_hover(mouse_pos, scale_x, scale_y)
        if mouse_clicked:
            if obj.handle_click():
                print("Correct click!")

        # Debug draw
        obj.draw_debug(game_surface, scale_x, scale_y)

    scaled_surface = pygame.transform.scale(game_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_surface, (0, 0))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
