import pygame
import random

from game.subsystems.scripts import LogInfoParams, MarioChaseInfoParams, PatrolInfoParams, \
    MoveLeftInfoParams, MoveRightInfoParams, JumpInfoParams, ScriptSwitcherInfoParams, FlagSwitchInfoParams, \
    PlaySoundInfoParams, ChangeAnimInfoParams, MovementSystemInfoParams
from game.subsystems.levels import Game, Level

from game.engine.objects import StaticObjectInfoParams, MovingObjectInfoParams, PlayerObjectInfoParams, HitboxParams


def create_test_level()-> Level:
    level = Level()
    level.size = (5000,1080)

    player_sprite_id = level.add_sprite(
        path ='assets/test_level/character/char0.png'
    )

    #player
    player_id = level.set_player(
        params=PlayerObjectInfoParams(
            pos = (0,0),
            sprite_id = player_sprite_id,

            max_speed_x = 10*16,
            max_speed_y = 20*16,
            ground_friction_x = 3,
            air_friction_x = 0.05,
            air_friction_y = 0,
            gravitate = True,
            velocity_x = 0,
            velocity_y = 0,

            lives = 5
        ),
        physics = True,
        physics_type = 'Stoppable',
        layer = 1,
        force_active = True
    )

    mario_sprite_id = level.add_sprite("assets/character/mario.png")
    #mario1
    mario_id = level.add_object(
        params= MovingObjectInfoParams(
            pos = (30, 1080-70-70-70-70-35),
            sprite_id = mario_sprite_id,
            max_speed_x= 5*16,
            max_speed_y=20*16,
            gravitate= True,
            velocity_x=0,
            velocity_y=0,
            ground_friction_x = 3,
            air_friction_x = 0.05,
            air_friction_y = 0
        ),
        physics = True,
        physics_type = 'Stoppable',
        layer=1,
        force_active=False,
        class_type= 'Moving'
    )

    #mario2
    mario2_id = level.add_object(
        params=MovingObjectInfoParams(
            pos=(1500, 1080 - 70 - 70 - 70),
            sprite_id=mario_sprite_id,
            max_speed_x=10 * 16,
            max_speed_y=20 * 16,
            gravitate=True,
            velocity_x=0,
            velocity_y=0,
            ground_friction_x=3,
            air_friction_x=0.05,
            air_friction_y=0
        ),
        physics=True,
        physics_type='Stoppable',
        layer=1,
        force_active=False,
        class_type='Moving'
    )

    background_sprite_id = level.add_sprite("assets/background/background.png",)

    #background
    level.add_object(
        class_type="Static",
        physics=False,
        layer=0,
        need_hitbox= False,
        params=StaticObjectInfoParams(
            pos=(0, 0),
            sprite_id=background_sprite_id
        )

    )

    brick_sprite_id = level.add_sprite("assets/test/brick.png")

    #ground
    for i in range(73):
        level.add_object(
            class_type = "Static",
            physics = True,
            physics_type = "Static",
            layer = 1,
            params = StaticObjectInfoParams(
                pos = (i * 70, 1080-35),
                sprite_id = brick_sprite_id
            )
        )

    #platforms
    for i in range(100, 5000, 70):
        for j in range(0, 1080 - 35 * 3, 35):
            if random.randint(0, 100) % 100 == 0:
                level.add_object(
                    class_type="Static",
                    physics=True,
                    physics_type="Static",
                    layer=1,
                    params=StaticObjectInfoParams(
                        pos=(i,j),
                        sprite_id = brick_sprite_id
                    )
                )

    #the_flying_brick
    level.add_object(
        class_type = "Moving",
        physics = True,
        physics_type = "Unstoppable",
        layer=1,
        params= MovingObjectInfoParams
        (
            pos = (-200, 1080-70-70-70-70-35),
            sprite_id= brick_sprite_id,

            max_speed_x = 5*16,
            max_speed_y = 5*16,
            gravitate = False,
            velocity_x = 25,
            velocity_y = -5,
            ground_friction_x=0,
            air_friction_x=0,
            air_friction_y=0
        )
    )

    #cam_boxes
    level.add_cam_box(
        hitbox= HitboxParams(
            pos = (0,0),
            size = (5000-1920,0)
        )
    )

    flag_sprite_id = level.add_sprite('assets/test/flagbox.png')

    #flag
    flag_id = level.add_object(
        class_type = "Static",
        physics = False,
        force_active = False,
        layer = None,
        need_hitbox= True,
        params= StaticObjectInfoParams(
            pos = (70,1080-500),
            sprite_id = flag_sprite_id
        )
    )

    jump_sound_path = 'assets/test_level/sound/jump.mp3'
    zombie_path = "assets/test_level/sound/zombie.mp3"

    anim_name = 'rotate'

    anim_sprite_id1 = level.add_sprite("assets/character/char0.png", size=(100,100))
    anim_sprite_id2 = level.add_sprite("assets/character/char1.png", size=(100,100))

    level.add_animation(
        object_id=player_id,
        name=anim_name,
        delay=2,
        frames_ids=[anim_sprite_id1, anim_sprite_id2],
        change_hitboxes= True
    )

    level.add_sound('sound', jump_sound_path,0.1)
    level.add_sound('sound', zombie_path, 0.3)

    level.add_script(LogInfoParams(player_id))
    level.add_script(MarioChaseInfoParams(mario_id,player_id))
    level.add_script(PatrolInfoParams(mario2_id, [(1500,970),[2000,970]]))

    zombie_sound_id = level.add_script(PlaySoundInfoParams(zombie_path))
    anim_change_id = level.add_script(ChangeAnimInfoParams(target_id= player_id, animation_name = anim_name))


    switcher_id = level.add_script(ScriptSwitcherInfoParams(scripts_switch_ids=[anim_change_id], scripts_toggle_on_ids=[zombie_sound_id], enabled= True))
    level.add_script(FlagSwitchInfoParams(flag_obj_id= flag_id, target_obj_id= player_id,switcher_id = switcher_id, enabled = True))



    m_l_id = level.add_script(MoveLeftInfoParams(player_id, 500, 50, 10 * 16))
    m_r_id = level.add_script(MoveRightInfoParams(player_id, 500, 50, 10 * 16))
    j_id = level.add_script(JumpInfoParams(player_id,20*16,jump_sound_path))

    level.add_binds('press', pygame.K_a, m_l_id)
    level.add_binds('release', pygame.K_a, m_l_id)
    level.add_binds('press', pygame.K_d, m_r_id)
    level.add_binds('release', pygame.K_d, m_r_id)
    level.add_binds('hold', pygame.K_w, j_id)
    level.add_binds('hold', pygame.K_SPACE, j_id)
    level.add_binds('mouse_hold', pygame.BUTTON_LEFT, j_id)
    return level


def create_level_1()-> Level:
    level = Level()
    level.size = (2000,1200)
    level.g = 10*16*2

    #player #todo
    char_size = (47,94)
    player_sprite_id = level.add_sprite(
        path = "assets/characters/ANDY/andy.png",
        size = char_size
    )

    player_id = level.set_player(
        physics=True,
        physics_type= "Stoppable",
        params= PlayerObjectInfoParams(
            pos= (10,1200 - 2*94),
            sprite_id= player_sprite_id,

            max_speed_x= 1000,
            max_speed_y= 1000,
            ground_friction_x = 3,
            air_friction_x = 0.05,
            air_friction_y=0,
            gravitate= True,
            velocity_x=0,
            velocity_y=0,

            lives= 5
        ),
        layer = 1,
        force_active = True,
        need_hitbox = False
    )


    #borders
    horizontal_border_spr_id = level.add_sprite(
        path="assets/pictures/game/things/error.png",
        hb_size=(2000, 50),
        hb_offset=(0, 0)
    )


    vertical_border_spr_id = level.add_sprite(
        path="assets/pictures/game/things/error.png",
        hb_size=(50, 1200),
        hb_offset=(0, 0)
    )

    #down
    level.add_object(
        class_type= 'Static',
        physics = True,
        physics_type= 'Static',
        params = StaticObjectInfoParams(
            pos = (0,1200-25),
            sprite_id= horizontal_border_spr_id,
        ),
        layer= None,
        force_active = False,
        need_hitbox= True
    )

    #up
    level.add_object(
        class_type='Static',
        physics=True,
        physics_type='Static',
        params=StaticObjectInfoParams(
            pos=(0, -50),
            sprite_id=horizontal_border_spr_id,
        ),
        layer=None,
        force_active=False,
        need_hitbox=True
    )

    #left
    level.add_object(
        class_type='Static',
        physics=True,
        physics_type='Static',
        params=StaticObjectInfoParams(
            pos=(-50, 0),
            sprite_id=vertical_border_spr_id,
        ),
        layer=None,
        force_active=False,
        need_hitbox=True
    )

    #right
    level.add_object(
        class_type='Static',
        physics=True,
        physics_type='Static',
        params=StaticObjectInfoParams(
            pos=(2000, 0),
            sprite_id=vertical_border_spr_id,
        ),
        layer=None,
        force_active=False,
        need_hitbox=True
    )

    # background #todo
    bg_sprite_id = level.add_sprite(
        path = "assets/pictures/game/background_game/bg0.png",
        hb_size = (0,0),
        hb_offset = (0,0)
    )

    bg_id = level.add_object(
        class_type= "Static",
        physics=False,
        params= StaticObjectInfoParams(
            pos = (0,0),
            sprite_id= bg_sprite_id,
        ),
        layer= 0,
        force_active=True,
        need_hitbox=False
    )

    rain_sprite_id = level.add_sprite(
        path = "assets/pictures/game/rain/0.png",
        size= (2000,1200)
    )

    rain_id = level.add_object(
        class_type= "Static",
        physics=False,
        params= StaticObjectInfoParams(
            pos = (0,0),
            sprite_id= rain_sprite_id,
        ),
        layer= 2,
        force_active=True,
        need_hitbox=False
    )

    #rain animation
    rain_anim_name = "rain"
    num = 9
    core = "assets/pictures/game/rain/"
    sprites = [level.add_sprite(path=f"{core}{i}.png", size=(2000,1200)) for i in range(0, num)]

    level.add_animation(
        object_id=rain_id,
        name=rain_anim_name,
        delay= 1 / num,
        frames_ids=sprites,
        change_hitboxes=False
    )

    level.add_script(
        ChangeAnimInfoParams(
            target_id= rain_id,
            animation_name= rain_anim_name,
            enabled= True
        )
    )

    #platforms #todo
    platform0_spr_id = level.add_sprite(
        path="assets/pictures/game/things/platform0.png"
    )
    platform1_spr_id = level.add_sprite(
        path="assets/pictures/game/things/platform1.png"
    )
    platform2_spr_id = level.add_sprite(
        path="assets/pictures/game/things/platform2.png"
    )
    platform3_spr_id = level.add_sprite(
        path="assets/pictures/game/things/platform3.png"
    )

    level.add_object(
        class_type= "Static",
        physics= True,
        physics_type= "Static",
        params= StaticObjectInfoParams(
            pos = (1600,1100),
            sprite_id = platform0_spr_id
        ),
        layer= 1,
        force_active= False,
        need_hitbox= True
    )


    #cameraboxes
    level.add_cam_box(
        hitbox= HitboxParams(
            pos = (0,0),
            size = (80,120)
        )
    )

    #animations
    #walk left
    core = "assets/characters/ANDY/walk_animation_left/"
    num = 8
    sprites = [level.add_sprite(path = f"{core}{i}.png", size= (47,94)) for i in range(0,num)]

    level.add_animation(
        object_id=player_id,
        name = "walk_left",
        delay = 1/num,
        frames_ids = sprites,
        change_hitboxes= False
    )

    #walk right
    num = 8
    core = "assets/characters/ANDY/walk_animation_right/"
    sprites = [level.add_sprite(path=f"{core}{i}.png", size= (47,94)) for i in range(0, num)]

    level.add_animation(
        object_id=player_id,
        name="walk_right",
        delay=1 / num,
        frames_ids=sprites,
        change_hitboxes=False
    )

    # jump_left
    num = 11
    core = "assets/characters/ANDY/jump_animation_left/"
    sprites = [level.add_sprite(path=f"{core}{i}.png", size= (47,94)) for i in range(0, num)]

    level.add_animation(
        object_id=player_id,
        name="jump_left",
        delay=1 / num,
        frames_ids=sprites,
        change_hitboxes=False
    )

    # jump_right
    num = 11
    core = "assets/characters/ANDY/jump_animation_right/"
    sprites = [level.add_sprite(path=f"{core}{i}.png", size= (47,94)) for i in range(0, num)]

    level.add_animation(
        object_id=player_id,
        name="jump_right",
        delay=1 / num,
        frames_ids=sprites,
        change_hitboxes=False
    )
    # fall_left
    num = 6
    core = "assets/characters/ANDY/fall_animation_left/"
    sprites = [level.add_sprite(path=f"{core}{i}.png", size= (47,94)) for i in range(0, num)]

    level.add_animation(
        object_id=player_id,
        name="fall_left",
        delay=1 / num,
        frames_ids=sprites,
        change_hitboxes=False
    )
    # fall_right
    num = 6
    core = "assets/characters/ANDY/fall_animation_right/"
    sprites = [level.add_sprite(path=f"{core}{i}.png", size= (47,94)) for i in range(0, num)]

    level.add_animation(
        object_id=player_id,
        name="fall_right",
        delay=1 / num,
        frames_ids=sprites,
        change_hitboxes=False
    )
    # stay_left
    num = 35
    core = "assets/characters/ANDY/stay_animation_left/"
    sprites = [level.add_sprite(path=f"{core}{i}.png", size= (47,94)) for i in range(0, num)]

    level.add_animation(
        object_id=player_id,
        name="stay_left",
        delay= 5 / num,
        frames_ids=sprites,
        change_hitboxes=False
    )
    # stay_right
    num = 35
    core = "assets/characters/ANDY/stay_animation_right/"
    sprites = [level.add_sprite(path=f"{core}{i}.png", size= (47,94)) for i in range(0, num)]

    level.add_animation(
        object_id=player_id,
        name="stay_right",
        delay= 5 / num,
        frames_ids=sprites,
        change_hitboxes=False
    )

    #scripts #todo
    level.add_script(LogInfoParams(player_id))

    #sounds #todo
    jump_sound_path = 'assets/audio/game/sounds/ANDY/jump/up.mp3'
    level.add_sound('sound',jump_sound_path, 0.1)

    #binds #todo
    m_l_id = level.add_script(MoveLeftInfoParams(player_id, 500, 50, 10 * 16))
    m_r_id = level.add_script(MoveRightInfoParams(player_id, 500, 50, 10 * 16))
    j_id = level.add_script(JumpInfoParams(player_id, 20 * 16, jump_sound_path))

    level.add_script(
        MovementSystemInfoParams(
            target_id = player_id,
            m_l_scr_id = m_l_id,
            m_r_scr_id = m_r_id,
            j_scr_id = j_id,
            enabled = True
        )
    )


    level.add_binds('press', pygame.K_a, m_l_id)
    level.add_binds('release', pygame.K_a, m_l_id)
    level.add_binds('press', pygame.K_d, m_r_id)
    level.add_binds('release', pygame.K_d, m_r_id)
    level.add_binds('hold', pygame.K_w, j_id)
    level.add_binds('hold', pygame.K_SPACE, j_id)
    level.add_binds('mouse_hold', pygame.BUTTON_LEFT, j_id)

    return level


def test2()-> None:
    screen_size = (1920,1080)
    max_fps = 0

    pygame.init()
    screen = pygame.display.set_mode(size = screen_size,vsync = max_fps)
    pygame.display.set_caption("Окно так называется")  # Название окна

    icon = pygame.image.load("assets/icon.png")
    pygame.display.set_icon(icon)

    clock = pygame.time.Clock()

    level_path = "saves/level1/level1.json"

    level = create_level_1()
    level.save_to_file(level_path)
    level = Level()
    level.load_from_file(level_path)

    game = Game(screen,screen_size,clock,max_fps)

    game.load_level(level)

    game.game_loop()

if __name__ == "__main__":
    test2()