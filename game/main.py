import pygame

from game.create_levels import create_level_3_coming_soon
from game.subsystems.levels import Game, Level

from create_levels import  create_level_1, create_level_2


def base_init():
    screen_size = (1920,1080)
    max_fps = 60

    pygame.init()
    screen = pygame.display.set_mode(size=screen_size, vsync=max_fps, flags=pygame.FULLSCREEN | pygame.SCALED)

    pygame.display.set_caption("The fog")
    icon = pygame.image.load("assets/icon.png")
    pygame.display.set_icon(icon)

    clock = pygame.time.Clock()


    return screen_size, max_fps, screen, clock, 1, 0.1, 0.1


def main():
    screen_size, max_fps, screen, clock, num, sound_volume, music_volume = base_init()

    full_exit = False

    level = Level()

    while not full_exit:
        level.load_from_file(filename = f"saves/level{num}/level{num}.json")

        game = Game(screen = screen, screen_size = level.screen_size, max_fps = max_fps, clock = clock, sound_volume = sound_volume, music_volume= music_volume)

        game.load_level(level = level, num = num)

        game.game_loop()

        full_exit = game.full_exit

        num = game.change_level[1]


if __name__ == "__main__":
    #create_level_1()
    #create_level_2()
    #create_level_3_coming_soon()
    main()