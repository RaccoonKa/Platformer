import pygame
import random

from game.subsystems.scripts import LogInfoParams, MarioChaseInfoParams, PatrolInfoParams, \
    MoveLeftInfoParams, MoveRightInfoParams, JumpInfoParams, ScriptSwitcherInfoParams, FlagSwitchInfoParams, \
    PlaySoundInfoParams, ChangeAnimInfoParams
from game.subsystems.levels import Game, Level

from game.engine.objects import StaticObjectParams, MovingObjectParams, PlayerObjectParams, HitboxParams


def create_test_level()-> Level:
    level = Level()
    level.size = (5000,1080)

    #player
    player_id = level.set_player(
        params=PlayerObjectParams(
            pos = (0,0),
            sprite_path = "assets/character/char0.png",
            generate_hitbox = True,
            max_speed_x = 10*16,
            max_speed_y = 20*16,
            ground_friction_x = 3,
            air_friction_x = 0.05,
            air_friction_y = 0,
            gravitate = True,
            velocity_x = 0,
            velocity_y = 0,
            lives = 5,
        ),
        physics = True,
        physics_type = 'Stoppable',
        layer = 1,
        force_active = True
    )

    mario_sprite = "assets/character/mario.png"
    #mario1
    mario_id = level.add_object(
        params= MovingObjectParams(
            pos = (30, 1080-70-70-70-70-35),
            sprite_path= mario_sprite,
            generate_hitbox= True,
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
        params=MovingObjectParams(
            pos=(1500, 1080 - 70 - 70 - 70),
            sprite_path=mario_sprite,
            generate_hitbox=True,
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

    #background
    level.add_object(
        class_type="Static",
        physics=False,
        layer=0,
        params=StaticObjectParams(
            pos=(0, 0),
            sprite_path="assets/background/background.png",
            generate_hitbox=False
        )
    )

    #ground
    brick_path = "assets/test/brick.png"
    for i in range(73):
        level.add_object(
            class_type = "Static",
            physics = True,
            physics_type = "Static",
            layer = 1,
            params = StaticObjectParams(
                pos = (i * 70, 1080-35),
                sprite_path = brick_path,
                generate_hitbox = True
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
                    params=StaticObjectParams(
                        pos=(i,j),
                        sprite_path=brick_path,
                        generate_hitbox=True
                    )
                )

    #the_flying_brick
    level.add_object(
        class_type = "Moving",
        physics = True,
        physics_type = "Unstoppable",
        layer=1,
        params= MovingObjectParams
        (
            pos = (-200, 1080-70-70-70-70-35),
            max_speed_x = 5*16,
            max_speed_y = 5*16,
            sprite_path = brick_path,
            gravitate = False,
            generate_hitbox = True,
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

    #flag
    flag_id = level.add_object(
        class_type = "Static",
        physics = False,
        force_active = False,
        layer = 1,
        params= StaticObjectParams(
            pos = (70,1080-500),
            sprite_path = "assets/test/flagbox.png",
            generate_hitbox = True
        )
    )

    jump_sound_path = 'assets/sound/jump.mp3'
    zombie_path = "assets/sound/zombie.mp3"

    anim_name = 'rotate'
    level.add_animation(
        object_id= player_id,
        name = anim_name,
        delay = 2,
        frames=['assets/character/char0.png','assets/character/char1.png'],
        change_size= True,
        frames_size=[(100,100),(50,50)],
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


def test2()-> None:
    screen_size = (1920,1080)
    max_fps = 0

    pygame.init()
    screen = pygame.display.set_mode(size = screen_size,vsync = max_fps)
    pygame.display.set_caption("Окно так называется")  # Название окна

    icon = pygame.image.load("assets/icon.png")
    pygame.display.set_icon(icon)

    clock = pygame.time.Clock()

    level = create_test_level()
    level.save_to_file("saves/level1.json")
    level = Level()
    level.load_from_file("saves/level1.json")

    game = Game(screen,screen_size,clock,max_fps)
    game.load_level(level)

    game.game_loop()

if __name__ == "__main__":
    test2()

#sprite = pygame.transform.scale(sprite,(10,10))
