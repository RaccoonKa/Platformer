import pygame

pygame.init()

GAME_WIDTH, GAME_HEIGHT = 1920, 1080

# Настройка разрешения экрана
info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
game_surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))

# Картинка на фон
background = pygame.image.load("assets/pictures/background/menu(1920x1080).png").convert()
background = pygame.transform.scale(background, (GAME_WIDTH, GAME_HEIGHT))

pygame.display.set_caption("GAME_MENU")

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Подгоняем под экран
    game_surface.blit(background, (0, 0))
    scaled_surface = pygame.transform.scale(game_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_surface, (0, 0))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
