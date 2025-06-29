import pygame
import sys
import random

from pygame import HWSURFACE

from game.engine.objects import StaticObject, MovingObject, Player, Hitbox
from game.engine.render import Camera, CameraManager, Layer, LayerSystem, ActivityManager
from game.engine.physics import PhysicEngine
from game.engine.animation import  AnimationEngine
from game.engine.control import InputHandler
from game.engine.script_system import ScriptingSystem
from game.engine.sound import SoundEngine
from game.subsystems.control_commands import MoveLeftCommand, MoveRightCommand, JumpCommand, MousePositionCommand, ExampleMouseButtonCommand
from game.subsystems.scripts import MarioChaseScript, Patrol, LogScript
from game.subsystems.levels import Game, Level


def test() -> None:
    screen_size = (1920,1080)
    max_fps = 60

    #Базовые настройки
    pygame.init()
    screen = pygame.display.set_mode(size = screen_size, vsync = max_fps) #Разрешение
    pygame.display.set_caption("Окно так называется") #Название окна

    icon = pygame.image.load("assets/icon.png")
    pygame.display.set_icon(icon)

    clock = pygame.time.Clock()
    # флаги
    full_exit = False


    #Загрузка базовых объектов
    level_size = (5000,1080)

    player = Player(pos = (0,0), speed_x=10*16, speed_y=20*16,sprite= pygame.image.load("assets/character/char0.png"), ground_friction_x = 3, air_friction_x= 0.5, generate_hitbox = True)
    camera = Camera(player,screen_size)
    cam_manager = CameraManager(camera)
    cam_box_1 = Hitbox((0,0),(5000-1920,0))
    cam_box_2 = Hitbox((2000, -1000), (200, 4000))
    cam_manager.add_cam_box(cam_box_1)
    cam_manager.add_cam_box(cam_box_2)

    activity_manager = ActivityManager(camera, activation_distance=2500)


    layer_system = LayerSystem(level_size, screen)

    #tmp background
    bg = Layer()
    tmp_bg = pygame.Surface(level_size)
    tmp_bg.fill('white')
    background = StaticObject((0,0),tmp_bg)
    bg.objects.append(background)
    activity_manager.add_object(background)
    background.set_force_active(True)

    #tmp
    l1 = Layer()
    tmp_l1 = pygame.Surface((level_size[0]-2,level_size[1]-2))
    tmp_l1.fill('black')
    layer1 = StaticObject((1, 1), tmp_l1)
    l1.objects.append(layer1)
    activity_manager.add_object(layer1)
    activity_manager.set_force_active(layer1,True)


    l2 = Layer()
    l2.objects.append(player)

    physics = PhysicEngine()
    physics.add_stoppable_object(player)

    activity_manager.add_object(player)
    player.set_force_active(True)
    brick_sprite = pygame.image.load("assets/test/brick.png")
    for i in range(100,5000,70):
        for j in range(0,1080-35*3,35):
            if random.randint(0,100) % 100 == 0:
                brick = StaticObject((i,j),brick_sprite, generate_hitbox= True)
                l2.objects.append(brick)
                physics.add_static_object(brick)
                activity_manager.add_object(brick)

    for i in range(0,5000,70):
        brick = StaticObject((i, 1080-35), brick_sprite, generate_hitbox= True)
        l2.objects.append(brick)
        physics.add_static_object(brick)
        activity_manager.add_object(brick)

    the_flying_brick = MovingObject(pos=(-200, 1080-70-70-70-70-35),speed_x=5*16,speed_y=5*16,sprite=brick_sprite,gravitation=False,generate_hitbox=True,hitbox=None)
    the_flying_brick.velocity_x = 25
    the_flying_brick.velocity_y = -5
    l2.objects.append(the_flying_brick)
    physics.add_unstoppable_object(the_flying_brick)
    activity_manager.add_object(the_flying_brick)

    mariosprite = pygame.image.load("assets/character/mario.png")

    mario = MovingObject(pos=(30, 1080-70-70-70-70-35),speed_x=5*16,speed_y=20*16,sprite=mariosprite,gravitation=True,generate_hitbox=True,hitbox=None,ground_friction_x=3, air_friction_x=0.05)
    l2.objects.append(mario)
    physics.add_stoppable_object(mario)
    activity_manager.add_object(mario)

    sound_engine = SoundEngine()
    sound_engine.load_sound('jump',"assets/sound/jump.mp3", sound_volume=0.1)
    sound_engine.load_music("assets/sound/town.mp3")
    sound_engine.play_music(volume=0.3)


    ground_a = 500
    air_a = 50
    max_speed_x = player.max_speed_x-20
    jump_speed = player.max_speed_y

    m_l_command = MoveLeftCommand(player, ground_a, air_a, max_speed_x)
    m_r_command = MoveRightCommand(player, ground_a, air_a, max_speed_x)
    j_command = JumpCommand(player,sound_engine, jump_speed)

    input_engine = InputHandler(camera)
    input_engine.bind_key(pygame.K_a, m_l_command, 'hold')
    input_engine.bind_key(pygame.K_d, m_r_command, 'hold')
    input_engine.bind_key(pygame.K_w, j_command, 'hold')
    input_engine.bind_key(pygame.K_SPACE, j_command, 'hold')
    input_engine.bind_mouse_button(3, MousePositionCommand(input_engine), 'press')

    script_engine = ScriptingSystem()
    script_engine.add_script(MarioChaseScript(mario,player))
    input_engine.bind_mouse_button(1, ExampleMouseButtonCommand(input_engine, mario.hitbox), 'press')


    mario2 = MovingObject(pos = (1500,1080-70-70-70),speed_x=10*16, speed_y=20*16, sprite=mariosprite,gravitation=True,generate_hitbox=True,hitbox= None, ground_friction_x=3, air_friction_x=0.05)
    l2.objects.append(mario2)
    physics.add_stoppable_object(mario2)
    activity_manager.add_object(mario2)
    mario2patrol = Patrol(mario2,[(1500,970),[2000,970]])
    script_engine.add_script(mario2patrol)


    #meow
    layer_system.layers.append(bg)
    layer_system.layers.append(l1)
    layer_system.layers.append(l2)

    animation_engine = AnimationEngine()
    animation_engine.add_object(player)
    animation_engine.add_anim(player,'rotate',1,[pygame.image.load('assets/character/char0.png'),pygame.image.load('assets/character/char1.png')])
    animation_engine.switch_anim(player,'rotate')
    animation_engine.turn_on(player)


    log = LogScript(camera,clock,player,activity_manager)
    script_engine.add_script(log)
    #Основной цикл
    while not full_exit:
        fps = clock.get_fps()
        dt = 1/fps if fps != 0 else 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                full_exit = True
            input_engine.handle_event(event)

        activity_manager.update()

        input_engine.update(dt)

        script_engine.update(dt)

        physics.update(dt, activity_manager)

        animation_engine.update(dt, activity_manager)

        cam_manager.update()

        layer_system.update(activity_manager)

        layer_system.draw_by_camera(screen,camera)

        pygame.display.update()

        clock.tick_busy_loop(max_fps)


    if full_exit:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    test()
