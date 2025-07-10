import pygame

from game.menu import menu
from game.subsystems.levels import Game, Level

from create_levels import  create_level_1, create_level_2
from game.create_levels import create_level_3_coming_soon


def z():
    screen_size = (1920,1080)
    max_fps = 0

    pygame.init()
    screen = pygame.display.set_mode(size=screen_size, flags=pygame.FULLSCREEN | pygame.SCALED)

    pygame.display.set_caption("The fog")
    icon = pygame.image.load("assets/icon.png")
    pygame.display.set_icon(icon)

    clock = pygame.time.Clock()


    return screen_size, max_fps, screen, clock, 0, 0.1, 0.1, False


def main():
    pygame.init()

    screen_size, max_fps, screen, clock, num, sound_volume, music_volume, full_exit = menu(sound_volume_ = 0.2, music_volume_ =0.2)

    level = Level()

    while not full_exit:

        if num != 0:
            level.load_from_file(filename = f"saves/level{num}/level{num}.json")

        game = Game(screen = screen, screen_size = level.screen_size, max_fps = max_fps, clock = clock, sound_volume = sound_volume, music_volume= music_volume)

        game.load_level(level = level, num = num)

        game.game_loop()

        full_exit = game.full_exit

        num = game.change_level[1]

        if num == 0:
            screen_size, max_fps, screen, clock, num, sound_volume, music_volume, full_exit = menu(sound_volume, music_volume)

    pygame.quit()
if __name__ == "__main__":
    #create_level_1()
    #create_level_2()
    #create_level_3_coming_soon()
    main()