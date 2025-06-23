import pygame
import sys
import random

from engine.objects import StaticObject, MovingObject, Player
from engine.render import Camera, Layer, LayerSystem, ActivityManager
from engine.physics import PhysicEngine
from engine.animation import  AnimationEngine
from engine.control import InputHandler
from engine.script_system import ScriptingSystem
from engine.sound import SoundEngine
from game.subsystems.control_commands import MoveLeftCommand, MoveRightCommand, JumpCommand, MousePositionCommand, MouseButtonCommand
from game.subsystems.scripts import MarioChaseScript, Patrol


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

    player = Player(pos = (0,0), speed_x=10*16, speed_y=20*16,sprite= pygame.image.load("assets/character/char0.png"), friction_x = 0.05, generate_hitbox = True)
    camera = Camera(player,screen_size)

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

    physics = PhysicEngine(max_fps)
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

    the_flying_brick = MovingObject(pos=(-200, 1080-70-70-70-70-35),speed_x=5*16,speed_y=5*16,sprite=brick_sprite,gravitation=False,generate_hitbox=True,hitbox=None,friction_x=0,friction_y=0)
    the_flying_brick.velocity_x = 25
    the_flying_brick.velocity_y = -5
    l2.objects.append(the_flying_brick)
    physics.add_unstoppable_object(the_flying_brick)
    activity_manager.add_object(the_flying_brick)

    mariosprite = pygame.image.load("assets/character/mario.png")

    mario = MovingObject(pos=(30, 1080-70-70-70-70-35),speed_x=5*16,speed_y=20*16,sprite=mariosprite,gravitation=True,generate_hitbox=True,hitbox=None,friction_x=0.05,friction_y=0)
    l2.objects.append(mario)
    physics.add_stoppable_object(mario)
    activity_manager.add_object(mario)

    sound_engine = SoundEngine()
    sound_engine.load_sound('jump',"assets/sound/jump.mp3", sound_volume=0.1)
    sound_engine.load_music("assets/sound/town.mp3")
    sound_engine.play_music(volume=0.3)


    input_engine = InputHandler(camera)
    input_engine.bind_key(pygame.K_a, MoveLeftCommand(player))
    input_engine.bind_key(pygame.K_d, MoveRightCommand(player))
    input_engine.bind_key(pygame.K_w, JumpCommand(player,sound_engine))
    input_engine.bind_key(pygame.K_SPACE, JumpCommand(player,sound_engine))
    input_engine.bind_mouse_button(3, MousePositionCommand(input_engine))


    script_engine = ScriptingSystem()
    script_engine.add_script(MarioChaseScript(mario,player))
    input_engine.bind_mouse_button(1,MouseButtonCommand(input_engine,mario.hitbox))


    mario2 = MovingObject(pos = (1500,1080-70-70-70),speed_x=10*16, speed_y=20*16, sprite=mariosprite,gravitation=True,generate_hitbox=True,hitbox= None, friction_x=0.05,friction_y=0)
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

    #Основной цикл
    frame_cnt = 0
    game_time = 0
    log_delay = 0
    while not full_exit:
        fps = clock.get_fps()
        dt = 1/fps if fps != 0 else 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                full_exit = True
            input_engine.handle_event(event)

        activity_manager.update()

        input_engine.update()

        script_engine.update(dt)

        physics.update(dt, activity_manager)

        animation_engine.update(dt, activity_manager)

        layer_system.update(activity_manager)

        camera.update()
        # + => render.update()?
        layer_system.draw_by_camera(screen,camera)

        pygame.display.update()

        #tmp gonna script?
        game_time += dt#clock.get_time()/1000
        log_delay += dt
        if log_delay > 5:
            print("активных объектов:",len(activity_manager.get_active_objects()))
            print(f"camera: {camera.x,camera.y}, player: {player.x,player.y}, fps: {clock.get_fps()}, frame_time: {dt}")
            print("game time:",game_time)
            frame_cnt = 0
            log_delay = 0
        frame_cnt +=1

        clock.tick_busy_loop(max_fps)


    if full_exit:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    test()