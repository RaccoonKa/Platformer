import pygame
import sys

from player import Player


def main() -> None:
    screenX = 1920
    screenY = 1080
    max_fps = 60

    #Базовые настройки
    pygame.init()
    screen = pygame.display.set_mode(size =(screenX, screenY),vsync= max_fps) #Разрешение
    pygame.display.set_caption("TestNAME") #Название окна

    icon = pygame.image.load("assets/icon.png")
    pygame.display.set_icon(icon)

    clock = pygame.time.Clock()

    # флаги
    full_exit = False

    #Загрузка базовых объектов
    player = Player(sprite_name="assets/character/char0.png", speed_= 5)
    bg = pygame.Rect((0,0),(screenX,screenY))


    #Основной цикл
    while not full_exit:
        pygame.draw.rect(screen,'gray',bg,0)

        player.draw(screen)
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d] :
            player.pos[0] += player.speed
        if keys[pygame.K_a]:
            player.pos[0] -= player.speed
        if keys[pygame.K_w]:
            player.pos[1] -= player.speed
        if keys[pygame.K_s]:
            player.pos[1] += player.speed

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                full_exit = True

        pygame.display.update()

        clock.tick(max_fps)

    if full_exit:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()