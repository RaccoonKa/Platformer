import pygame
import sys
import random

from engine.objects import StaticObject, MovingObject, Player
from engine.render import Camera, Layer, MainSurface
from engine.physics import PhysicEngine
from engine.animation import  AnimationEngine
from engine.sound import SoundEngine


def main() -> None:
    screen_size = (1920,1080)
    max_fps = 60

    #Базовые настройки
    pygame.init()
    screen = pygame.display.set_mode(size = screen_size, vsync = max_fps) #Разрешение
    pygame.display.set_caption("Окно так называется, йоу") #Название окна

    icon = pygame.image.load("assets/icon.png")
    pygame.display.set_icon(icon)

    clock = pygame.time.Clock()
    # флаги
    full_exit = False

    #Загрузка базовых объектов
    level_size = (5000,1080)

    player = Player((0,0),10,10,pygame.image.load("assets/character/char0.png"))
    camera = Camera(player,screen_size)

    main_sf = MainSurface(level_size,screen)

    #tmp background
    bg = Layer()
    tmp_bg = pygame.Surface(level_size)
    tmp_bg.fill('white')
    background = StaticObject((0,0),tmp_bg)
    bg.objects.append(background)

    #tmp
    l1 = Layer()
    tmp_l1 = pygame.Surface((level_size[0]-2,level_size[1]-2))
    tmp_l1.fill('black')
    layer1 = StaticObject((1, 1), tmp_l1)
    l1.objects.append(layer1)

    l2 = Layer()
    l2.objects.append(player)

    physics = PhysicEngine(max_fps)
    physics.add_moving_object(player)

    brick_sprite = pygame.image.load("assets/test/brick.png")
    for i in range(100,5000,70):
        for j in range(0,1080-35,35):
            if random.randint(0,100) % 100 == 0:
                brick = StaticObject((i,j),brick_sprite)
                l2.objects.append(brick)
                physics.add_static_object(brick)

    for i in range(0,5000,70):
        brick = StaticObject((i, 1080-35), brick_sprite)
        l2.objects.append(brick)
        physics.add_static_object(brick)


    #meow
    main_sf.layers.append(bg)
    main_sf.layers.append(l1)
    main_sf.layers.append(l2)

    frame_cnt = 0
    #Основной цикл
    while not full_exit:
        start_frame = clock.get_time()

        # Обработка клавиатуры

        #tmp
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player.velocity_y = -player.max_speed_y
        if keys[pygame.K_a]:
            player.velocity_x = -player.max_speed_x
        if keys[pygame.K_d]:
            player.velocity_x = player.max_speed_x
        if not keys[pygame.K_a] and not keys[pygame.K_d]:
            player.velocity_x = 0.05* player.velocity_x

        # какие-то взаимодействия с чем-то

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                full_exit = True

        # Работа физики
        physics.fps = clock.get_fps()
        physics.update()

        # Работа движка анимаций

        # Работа наложения поверхностей
        main_sf.update()

        # Работа камеры
        camera.update()

        main_sf.draw_by_camera(screen,camera)

        pygame.display.update()

        end_frame = clock.get_time()

        if frame_cnt == max_fps*5:
            print(f"camera: {camera.x,camera.y}, player: {player.x,player.y}, fps: {clock.get_fps()}, frame_time: {clock.get_time()} or {end_frame - start_frame}")
            frame_cnt = 0

        frame_cnt +=1
        clock.tick(max_fps)

    if full_exit:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()

#
# Хитбоксы должны как-то сами следить за своими объектами. Или вообще их объединить
# Сделать так, чтобы стоя на поверхности перс не падал вниз
# Собственно если откреплён от поверхности, то прыгать не может
# там чо то ещё, я забыл