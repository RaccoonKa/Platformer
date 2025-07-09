import pygame

from game.subsystems.scripts import LogInfoParams, PatrolInfoParams, \
    MoveLeftInfoParams, MoveRightInfoParams, JumpInfoParams, ScriptSwitcherInfoParams, \
    PlaySoundInfoParams, ChangeAnimInfoParams, MovementSystemInfoParams, MousePositionInfoParams, \
    PlatformAppearSystemInfoParams, ZoneSwitchInfoParams, MovementSwitcherInfoParams, MouseTeleportInfoParams, \
    MusicPlayerInfoParams, ChangeLevelInfoParams, LivesControlInfoParams, TeleportObjectInfoParams, DeadZoneInfoParams, \
    NpcMoveLeftInfoParams, NpcMoveRightInfoParams

from game.engine.objects import StaticObjectInfoParams, MovingObjectInfoParams, PlayerObjectInfoParams, HitboxParams

from game.subsystems.levels import Level


def create_level_1()-> Level:
    level_path = "saves/level1/level1.json"

    level = Level()
    level.screen_size = (1152,648)
    level.size = (2000,1200)
    level.g = 10*16*2

    sounds_volume = 0.2
    music_volume = 0.2





    #cameraboxes
    level.add_cam_box(
        hitbox= HitboxParams(
            pos = (0,0),
            size = (level.size[0] - level.screen_size[0], level.size[1] - level.screen_size[1])
        )
    )





    #change_level
    level_to_next = level.add_script(
        ChangeLevelInfoParams(
            to_num= 2
        )
    )

    level_to_this = level.add_script(
        ChangeLevelInfoParams(
            to_num=1
        )
    )
    switcher_to_next = level.add_script(
        ScriptSwitcherInfoParams(
            enabled= True,
            scripts_toggle_on_ids=[level_to_next]
        )
    )

    switcher_to_this = level.add_script(
        ScriptSwitcherInfoParams(
            enabled=True,
            scripts_toggle_on_ids=[level_to_this]
        )
    )





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
            ground_friction_x = 6,
            air_friction_x = 0.2,
            air_friction_y=0,
            gravitate= True,
            velocity_x=0,
            velocity_y=0,

            lives= 3
        ),
        layer = 2,
        force_active = True,
        need_hitbox = False
    )





    # sounds #todo
    jump_sound_path = 'assets/audio/game/sounds/ANDY/jump/up.mp3'
    level.add_sound('sound', jump_sound_path, sounds_volume)
    land_sound_path = 'assets/audio/game/sounds/ANDY/jump/down.mp3'
    level.add_sound('sound', land_sound_path, sounds_volume)
    fall_sound_path = 'assets/audio/game/sounds/ANDY/fall/fall.mp3'
    level.add_sound('sound', fall_sound_path, sounds_volume)
    walk_sound_path = 'assets/audio/game/sounds/ANDY/steps/steps.mp3'
    level.add_sound('sound', walk_sound_path, sounds_volume)
    damage_sound_path = 'assets/audio/game/sounds/ANDY/damage/damage.mp3'
    level.add_sound('sound', damage_sound_path, sounds_volume)
    death_sound_path = 'assets/audio/game/sounds/ANDY/death/death.mp3'
    level.add_sound('sound', death_sound_path, sounds_volume)

    server_sound_path = 'assets/audio/game/sounds/platforms/platform_server.mp3'
    level.add_sound('sound', server_sound_path, sounds_volume)
    printer_sound_path = 'assets/audio/game/sounds/platforms/platform_printer.mp3'
    level.add_sound('sound', printer_sound_path, sounds_volume)
    platform_bug_sound_path = 'assets/audio/game/sounds/platforms/platform_bug_texture.mp3'
    level.add_sound('sound', platform_bug_sound_path, sounds_volume)
    rain_sound_path = 'assets/audio/game/sounds/rain/rain.mp3'
    level.add_sound('sound', rain_sound_path, sounds_volume)

    #music
    music_script_id = level.add_script(
        MusicPlayerInfoParams(
            enabled= False,
            playlist=[
                ('assets/audio/game/game_music/0.mp3', music_volume),
                ('assets/audio/game/game_music/1.mp3', music_volume)
            ]
        )
    )

    #rain
    level.add_script(
        PlaySoundInfoParams(
            sound= rain_sound_path,
            loops = -1,
            enabled= True
        )
    )





    # binds #todo
    m_l_id = level.add_script(MoveLeftInfoParams(player_id, 500, 50, 10 * 16))
    m_r_id = level.add_script(MoveRightInfoParams(player_id, 500, 50, 10 * 16))
    j_id = level.add_script(JumpInfoParams(player_id, 20 * 16, jump_sound_path, land_sound_path))

    movement_system_id = level.add_script(
        MovementSystemInfoParams(
            target_id=player_id,
            m_l_scr_id=m_l_id,
            m_r_scr_id=m_r_id,
            j_scr_id=j_id,
            enabled=True,
            fall_sound=fall_sound_path,
            land_sound=land_sound_path,
            walk_sound=walk_sound_path,
            damage_sound= damage_sound_path,
            fall_damage_threshold= 500
        )
    )

    level.add_binds('press', pygame.K_a, m_l_id)
    level.add_binds('release', pygame.K_a, m_l_id)
    level.add_binds('press', pygame.K_d, m_r_id)
    level.add_binds('release', pygame.K_d, m_r_id)
    level.add_binds('press', pygame.K_w, j_id)
    level.add_binds('press', pygame.K_SPACE, j_id)

    move_switcher_id = level.add_script(
        MovementSwitcherInfoParams(
            scripts_to_block_ids= [m_r_id, m_l_id, j_id],
            max_switches = 1,
            enabled= True
        )
    )





    #lives
    death_time = 1.5

    lives_control_script = level.add_script(
        LivesControlInfoParams(
            player_id= player_id,
            change_level_script_id = switcher_to_this,
            move_block_script_id= move_switcher_id,
            mov_sys_id= movement_system_id,
            death_sound= death_sound_path,
            death_time= death_time,
            fall_sound= fall_sound_path,
            enabled= True
        )
    )

    level.add_binds(type_= "press", key = pygame.K_r, command_script_id= lives_control_script)




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
        delay= 2 / num,
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
        delay= 2 / num,
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
    # death
    num = 5
    core = "assets/characters/ANDY/death_animation/"
    sprites = [level.add_sprite(path=f"{core}{i}.png", size=(47+i*(94-47)//(num-1), 94+i*(47-94)//(num-1))) for i in range(0, num)]

    level.add_animation(
        object_id=player_id,
        name="death",
        delay=death_time / num,
        frames_ids=sprites,
        change_hitboxes=True
    )

    #death_lay
    sprites = [level.add_sprite(path=f"assets/characters/ANDY/death_animation/4.png", size=(94, 47), hb_size= (94,47), hb_offset= (0,0))]
    level.add_animation(
        object_id=player_id,
        name="death_lay",
        delay=100,
        frames_ids=sprites,
        change_hitboxes=True
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
            pos=(2000, 320),
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

    level.add_object(
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




    #rain
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
        layer= 3,
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
        path="assets/pictures/game/things/platform0.png",
        size = (254,60),
        hb_size = (254,50),
        hb_offset=(0,10)
    )
    platform1_spr_id = level.add_sprite(
        path="assets/pictures/game/things/platform1.png",
        size = (107,66),
        hb_size=(107,50),
        hb_offset=(0,16)
    )
    platform_bug_spr_id = level.add_sprite(
        path="assets/pictures/game/things/platform2.png"
    )
    platform2_spr_id = level.add_sprite(
        path="assets/pictures/game/things/platform3.png"
    )

    platform_ids = [level.add_object(
        class_type= "Static",
        physics= True,
        physics_type= "Static",
        params= StaticObjectInfoParams(
            pos = (1800-i*350,1100-i*100),
            sprite_id = platform0_spr_id
        ),
        layer= 1,
        force_active= False,
        need_hitbox= True
    ) for i in range(0,6)]

    platform_ids.append(level.add_object(
        class_type="Static",
        physics=True,
        physics_type="Static",
        params=StaticObjectInfoParams(
            pos=(420, 500),
            sprite_id=platform0_spr_id
        ),
        layer=1,
        force_active=False,
        need_hitbox=True
    ))
    platform_ids+= [
        level.add_object(
            class_type="Static",
            physics=True,
            physics_type="Static",
            params=StaticObjectInfoParams(
                pos=(770+300*i, 500-50*i),
                sprite_id=platform1_spr_id
            ),
            layer=1,
            force_active=False,
            need_hitbox=True
        ) for i in range(4)
    ]

    platform_ids.append(level.add_object(
        class_type="Moving",
        physics=True,
        physics_type="Unstoppable",
        params=MovingObjectInfoParams(
            pos=(1810, 310),
            sprite_id=platform_bug_spr_id,
            max_speed_x= 50,
            max_speed_y= 0,
            velocity_x= 0,
            velocity_y= 0,
            ground_friction_x= 0,
            air_friction_x= 0,
            air_friction_y= 0,
            gravitate= False
        ),
        layer=1,
        force_active=False,
        need_hitbox=True
    ))

    platform_appear_id = level.add_script(
        PlatformAppearSystemInfoParams(
            platforms_ids=platform_ids,
            target_id=player_id,
            appear_sounds=[(server_sound_path,-1)]*6 + [(printer_sound_path,-1)]*4 + [(platform_bug_sound_path,-1)],
            flag_size= (100,10),
            enabled= False
        )
    )

    platform_appear_switcher = level.add_script(
        ScriptSwitcherInfoParams(
            scripts_toggle_on_ids = [platform_appear_id, music_script_id],
            max_switches= 1
        )
    )
    level.add_script(
        ZoneSwitchInfoParams(
            target_obj_id= player_id,
            switcher_id= platform_appear_switcher,
            zone_pos= (1450,970),
            zone_size=(50,200),
        )
    )

    patrol_id = level.add_script(
        PatrolInfoParams(
            patrol_obj_id=platform_ids[-1],
            points = [(2500,310),(1810,310)],
            enabled = False
        )
    )
    patrol_switcher_id = level.add_script(
        ScriptSwitcherInfoParams(
            scripts_toggle_on_ids= [patrol_id],
            max_switches= 1,
            enabled= True
        )
    )

    level.add_script(
        ZoneSwitchInfoParams(
            zone_pos = (1810, 300),
            zone_size= (80,10),
            switcher_id= move_switcher_id,
            target_obj_id= player_id,
            enabled= True
        )
    )
    level.add_script(
        ZoneSwitchInfoParams(
            zone_pos=(1810, 300),
            zone_size=(80, 10),
            switcher_id=patrol_switcher_id,
            target_obj_id=player_id,
            enabled= True
        )
    )

    level.add_script(
        ZoneSwitchInfoParams(
            zone_pos= (2200, 220),
            zone_size= (100,100),
            target_obj_id= player_id,
            switcher_id = switcher_to_next
        )
    )





    #scripts #todo
    level.add_script(LogInfoParams(player_id))

    #tmp
    # mouse_script_id = level.add_script(MousePositionInfoParams())
    # level.add_binds('mouse_press', pygame.BUTTON_LEFT, mouse_script_id)
    # mouse_tp_script_id = level.add_script(
    #     MouseTeleportInfoParams(
    #         target_id= player_id
    #     )
    # )
    # level.add_binds('mouse_press', pygame.BUTTON_RIGHT, mouse_tp_script_id)

    level.save_to_file(level_path)
    return level




def create_level_2():
    level_path = "saves/level2/level2.json"

    level = Level()
    level.screen_size = (1152,648)
    #level.screen_size = (1920, 1080)
    level.size = (2000, 1200)
    level.g = 10 * 16 * 2

    sounds_volume = 0.2
    music_volume = 0.2

    # camera boxes
    level.add_cam_box(
        hitbox=HitboxParams(
            pos=(0, 0),
            size=(level.size[0] - level.screen_size[0], level.size[1] - level.screen_size[1])
        )
    )






    # change_level
    level_to_next = level.add_script(
        ChangeLevelInfoParams(
            to_num=3
        )
    )

    level_to_this = level.add_script(
        ChangeLevelInfoParams(
            to_num=2
        )
    )
    switcher_to_next = level.add_script(
        ScriptSwitcherInfoParams(
            enabled=True,
            scripts_toggle_on_ids=[level_to_next]
        )
    )

    switcher_to_this = level.add_script(
        ScriptSwitcherInfoParams(
            enabled=True,
            scripts_toggle_on_ids=[level_to_this]
        )
    )







    # player #todo
    char_size = (47, 94)
    player_sprite_id = level.add_sprite(
        path="assets/characters/ANDY/andy.png",
        size=char_size
    )

    player_id = level.set_player(
        physics=True,
        physics_type="Stoppable",
        params=PlayerObjectInfoParams(
            pos=(-50, 370-94-1),
            sprite_id=player_sprite_id,

            max_speed_x=1000,
            max_speed_y=1000,
            ground_friction_x=6,
            air_friction_x=0.2,
            air_friction_y=0,
            gravitate=True,
            velocity_x=0,
            velocity_y=0,

            lives=3
        ),
        layer=2,
        force_active=True,
        need_hitbox=False
    )







    # sounds #todo
    jump_sound_path = 'assets/audio/game/sounds/ANDY/jump/up.mp3'
    level.add_sound('sound', jump_sound_path, sounds_volume)
    land_sound_path = 'assets/audio/game/sounds/ANDY/jump/down.mp3'
    level.add_sound('sound', land_sound_path, sounds_volume)
    fall_sound_path = 'assets/audio/game/sounds/ANDY/fall/fall.mp3'
    level.add_sound('sound', fall_sound_path, sounds_volume)
    walk_sound_path = 'assets/audio/game/sounds/ANDY/steps/steps.mp3'
    level.add_sound('sound', walk_sound_path, sounds_volume)
    damage_sound_path = 'assets/audio/game/sounds/ANDY/damage/damage.mp3'
    level.add_sound('sound', damage_sound_path, sounds_volume)
    death_sound_path = 'assets/audio/game/sounds/ANDY/death/death.mp3'
    level.add_sound('sound', death_sound_path, sounds_volume)

    server_sound_path = 'assets/audio/game/sounds/platforms/platform_server.mp3'
    level.add_sound('sound', server_sound_path, sounds_volume)
    printer_sound_path = 'assets/audio/game/sounds/platforms/platform_printer.mp3'
    level.add_sound('sound', printer_sound_path, sounds_volume)
    platform_bug_sound_path = 'assets/audio/game/sounds/platforms/platform_bug_texture.mp3'
    level.add_sound('sound', platform_bug_sound_path, sounds_volume)
    platform_error_sound_path = 'assets/audio/game/sounds/platforms/platform_window_error.mp3'
    level.add_sound('sound', platform_error_sound_path, sounds_volume)
    rain_sound_path = 'assets/audio/game/sounds/rain/rain.mp3'
    level.add_sound('sound', rain_sound_path, sounds_volume)
    door_sound_path = 'assets/audio/game/sounds/other/door.wav'
    level.add_sound('sound', door_sound_path, sounds_volume)

    # music
    level.add_script(
        MusicPlayerInfoParams(
            enabled=True,
            playlist=[
                ('assets/audio/game/game_music/0.mp3', music_volume),
                ('assets/audio/game/game_music/1.mp3', music_volume)
            ]
        )
    )

    # rain
    level.add_script(
        PlaySoundInfoParams(
            sound=rain_sound_path,
            loops=-1,
            enabled=True
        )
    )








    # binds #todo
    m_l_id = level.add_script(MoveLeftInfoParams(player_id, 500, 50, 10 * 16))
    m_r_id = level.add_script(MoveRightInfoParams(player_id, 500, 50, 10 * 16))
    j_id = level.add_script(JumpInfoParams(player_id, 20 * 16, jump_sound_path, land_sound_path))

    movement_system_id = level.add_script(
        MovementSystemInfoParams(
            target_id=player_id,
            m_l_scr_id=m_l_id,
            m_r_scr_id=m_r_id,
            j_scr_id=j_id,
            enabled=True,
            fall_sound=fall_sound_path,
            land_sound=land_sound_path,
            walk_sound=walk_sound_path,
            damage_sound=damage_sound_path,
            fall_damage_threshold=500
        )
    )

    level.add_binds('press', pygame.K_a, m_l_id)
    level.add_binds('release', pygame.K_a, m_l_id)
    level.add_binds('press', pygame.K_d, m_r_id)
    level.add_binds('release', pygame.K_d, m_r_id)
    level.add_binds('press', pygame.K_w, j_id)
    level.add_binds('press', pygame.K_SPACE, j_id)

    spawn_move_switcher_id = level.add_script(
        MovementSwitcherInfoParams(
            scripts_block_switch_ids= [m_r_id, m_l_id, j_id],
            max_switches=2,
            enabled=True
        )
    )

    death_move_switcher_id = level.add_script(
        MovementSwitcherInfoParams(
            scripts_block_switch_ids=[m_r_id, m_l_id, j_id],
            max_switches=1,
            enabled=True
        )
    )

    move_switcher_id = level.add_script(
        MovementSwitcherInfoParams(
            scripts_block_switch_ids=[m_r_id, m_l_id, j_id],
            max_switches=1,
            enabled=True
        )
    )





    # lives
    death_time = 1.5

    lives_control_script = level.add_script(
        LivesControlInfoParams(
            player_id=player_id,
            change_level_script_id=switcher_to_this,
            move_block_script_id=death_move_switcher_id,
            mov_sys_id=movement_system_id,
            death_sound=death_sound_path,
            death_time=death_time,
            fall_sound= fall_sound_path,
            enabled=True
        )
    )

    level.add_binds(type_="press", key=pygame.K_r, command_script_id=lives_control_script)







    # animations
    # walk left
    core = "assets/characters/ANDY/walk_animation_left/"
    num = 8
    sprites = [level.add_sprite(path=f"{core}{i}.png", size=(47, 94)) for i in range(0, num)]

    level.add_animation(
        object_id=player_id,
        name="walk_left",
        delay=1 / num,
        frames_ids=sprites,
        change_hitboxes=False
    )

    # walk right
    num = 8
    core = "assets/characters/ANDY/walk_animation_right/"
    sprites = [level.add_sprite(path=f"{core}{i}.png", size=(47, 94)) for i in range(0, num)]

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
    sprites = [level.add_sprite(path=f"{core}{i}.png", size=(47, 94)) for i in range(0, num)]

    level.add_animation(
        object_id=player_id,
        name="jump_left",
        delay=2 / num,
        frames_ids=sprites,
        change_hitboxes=False
    )

    # jump_right
    num = 11
    core = "assets/characters/ANDY/jump_animation_right/"
    sprites = [level.add_sprite(path=f"{core}{i}.png", size=(47, 94)) for i in range(0, num)]

    level.add_animation(
        object_id=player_id,
        name="jump_right",
        delay=2 / num,
        frames_ids=sprites,
        change_hitboxes=False
    )
    # fall_left
    num = 6
    core = "assets/characters/ANDY/fall_animation_left/"
    sprites = [level.add_sprite(path=f"{core}{i}.png", size=(47, 94)) for i in range(0, num)]

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
    sprites = [level.add_sprite(path=f"{core}{i}.png", size=(47, 94)) for i in range(0, num)]

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
    sprites = [level.add_sprite(path=f"{core}{i}.png", size=(47, 94)) for i in range(0, num)]

    level.add_animation(
        object_id=player_id,
        name="stay_left",
        delay=5 / num,
        frames_ids=sprites,
        change_hitboxes=False
    )
    # stay_right
    num = 35
    core = "assets/characters/ANDY/stay_animation_right/"
    sprites = [level.add_sprite(path=f"{core}{i}.png", size=(47, 94)) for i in range(0, num)]

    level.add_animation(
        object_id=player_id,
        name="stay_right",
        delay=5 / num,
        frames_ids=sprites,
        change_hitboxes=False
    )
    # death
    num = 5
    core = "assets/characters/ANDY/death_animation/"
    sprites = [
        level.add_sprite(path=f"{core}{i}.png", size=(47 + i * (94 - 47) // (num - 1), 94 + i * (47 - 94) // (num - 1)))
        for i in range(0, num)]

    level.add_animation(
        object_id=player_id,
        name="death",
        delay=death_time / num,
        frames_ids=sprites,
        change_hitboxes=True
    )

    # death_lay
    sprites = [level.add_sprite(path=f"assets/characters/ANDY/death_animation/4.png", size=(94, 47), hb_size=(94, 47),
                                hb_offset=(0, 0))]
    level.add_animation(
        object_id=player_id,
        name="death_lay",
        delay=100,
        frames_ids=sprites,
        change_hitboxes=True
    )






    #borders
    horizontal_border_spr_id = level.add_sprite(
        path="assets/pictures/game/things/error.png",
        hb_size=(2300, 50),
        hb_offset=(-150, 0)
    )

    vertical_border_spr_id = level.add_sprite(
        path="assets/pictures/game/things/error.png",
        hb_size=(50, 950),
        hb_offset=(0, 0)
    )

    right_vertical_border_spr_id = level.add_sprite(
        path="assets/pictures/game/things/error.png",
        hb_size=(50, 1200-250-385),
        hb_offset=(0, 0)
    )


    #down
    level.add_object(
        class_type= 'Static',
        physics = True,
        physics_type= 'Static',
        params = StaticObjectInfoParams(
            pos = (0,1136),
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
    left_border_id = level.add_object(
        class_type='Static',
        physics=True,
        physics_type='Static',
        params=StaticObjectInfoParams(
            pos=(-50, 385),
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
            pos=(2000, 385),
            sprite_id=right_vertical_border_spr_id,
        ),
        layer=None,
        force_active=False,
        need_hitbox=True
    )








    # background #todo
    bg_sprite_id = level.add_sprite(
        path = "assets/pictures/game/background_game/bg3.png",
        hb_size = (0,0),
        hb_offset = (0,0)
    )

    level.add_object(
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






    #rain
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
        layer= 3,
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
        path="assets/pictures/game/things/platform0.png",
        size = (254,60),
        hb_size = (254,50),
        hb_offset=(0,10)
    )
    platform1_spr_id = level.add_sprite(
        path="assets/pictures/game/things/platform1.png",
        size = (107,66),
        hb_size=(107,50),
        hb_offset=(0,16)
    )
    platform_bug_spr_id = level.add_sprite(
        path="assets/pictures/game/things/platform2.png",
        hb_offset=(0,1)
    )
    platform_error_spr_id = level.add_sprite(
        path="assets/pictures/game/things/platform3.png"
    )


    platform_respawn_id = level.add_object(
        class_type="Moving",
        physics=True,
        physics_type="Unstoppable",
        params=MovingObjectInfoParams(
            pos=(-100, 370),
            sprite_id=platform_bug_spr_id,
            max_speed_x=50,
            max_speed_y=0,
            velocity_x=0,
            velocity_y=0,
            ground_friction_x=0,
            air_friction_x=0,
            air_friction_y=0,
            gravitate=False
        ),
        layer=1,
        force_active=False,
        need_hitbox=True
    )

    level.add_script(
        PatrolInfoParams(
            patrol_obj_id= platform_respawn_id,
            points = [(-200,370),(30,370)],
            cyclic= False,
            enabled= True
        )
    )

    border_tp = level.add_script(
        TeleportObjectInfoParams(
            target_id= left_border_id,
            pos = (-50,0)
        )

    )



    respawn_switcher = level.add_script(
        ScriptSwitcherInfoParams(
            enabled= True,
            scripts_toggle_on_ids = [border_tp]
        )
    )

    level.add_script(
        ZoneSwitchInfoParams(
            zone_pos = (89,350),
            zone_size= (50,20),
            target_obj_id= player_id,
            switcher_id = respawn_switcher,
            enabled= True
        )
    )
    level.add_script(
        ZoneSwitchInfoParams(
            zone_pos = (-40, 370-94-1),
            zone_size= (1,1),
            target_obj_id= player_id,
            switcher_id = spawn_move_switcher_id,
            enabled= True
        )
    )

    level.add_script(
        ZoneSwitchInfoParams(
            zone_pos = (89,350),
            zone_size= (50,20),
            target_obj_id= player_id,
            switcher_id = spawn_move_switcher_id,
            enabled= True
        )
    )


    platform0 = level.add_object(
        class_type="Moving",
        physics=True,
        physics_type="Unstoppable",
        params=MovingObjectInfoParams(
            pos=(500, 370),
            sprite_id=platform1_spr_id,
            max_speed_x=50,
            max_speed_y=0,
            velocity_x=0,
            velocity_y=0,
            ground_friction_x=0,
            air_friction_x=0,
            air_friction_y=0,
            gravitate=False
        ),
        layer=1,
        force_active=False,
        need_hitbox=True
    )


    level.add_script(
        PatrolInfoParams(
            patrol_obj_id=platform0,
            points=[(500,370),(200,370)],
            reach_distance=1,
            speed_x=50
        )
    )


    platform1 = level.add_object(
        class_type="Moving",
        physics=True,
        physics_type="Unstoppable",
        params=MovingObjectInfoParams(
            pos=(600, 375),
            sprite_id=platform1_spr_id,
            max_speed_x=50,
            max_speed_y=0,
            velocity_x=0,
            velocity_y=0,
            ground_friction_x=0,
            air_friction_x=0,
            air_friction_y=0,
            gravitate=False
        ),
        layer=1,
        force_active=False,
        need_hitbox=True
    )


    level.add_script(
        PatrolInfoParams(
            patrol_obj_id=platform1,
            points=[(600,375),(900,375)],
            reach_distance=1,
            speed_x =50
        )
    )

    platform2 = level.add_object(
        class_type="Moving",
        physics=True,
        physics_type="Unstoppable",
        params=MovingObjectInfoParams(
            pos=(1050, 600),
            sprite_id=platform_error_spr_id,
            max_speed_x=0,
            max_speed_y=50,
            velocity_x=0,
            velocity_y=0,
            ground_friction_x=0,
            air_friction_x=0,
            air_friction_y=0,
            gravitate=False
        ),
        layer=1,
        force_active=False,
        need_hitbox=True
    )

    appear_id = level.add_script(
        PlatformAppearSystemInfoParams(
            target_id= player_id,
            platforms_ids=[platform2],
            appear_sounds= [(platform_error_sound_path, -1)],
            enabled= False
        )
    )

    appear_switcher = level.add_script(
        ScriptSwitcherInfoParams(
            scripts_toggle_on_ids=[appear_id],
            max_switches=1
        )
    )

    level.add_script(
        ZoneSwitchInfoParams(
            zone_pos=(900,375),
            zone_size=(100,50),
            switcher_id=appear_switcher,
            target_obj_id=player_id
        )
    )

    platform3 = level.add_object(
        class_type="Moving",
        physics=True,
        physics_type="Unstoppable",
        params=MovingObjectInfoParams(
            pos=(920, 830),
            sprite_id=platform0_spr_id,
            max_speed_x=0,
            max_speed_y=50,
            velocity_x=0,
            velocity_y=0,
            ground_friction_x=0,
            air_friction_x=0,
            air_friction_y=0,
            gravitate=False
        ),
        layer=1,
        force_active=False,
        need_hitbox=True
    )

    level.add_script(
        PatrolInfoParams(
            patrol_obj_id=platform3,
            points=[(920, 830), (1500, 830)],
            reach_distance=1,
            speed_x=50
        )
    )


    #deadzone
    level.add_script(
        DeadZoneInfoParams(
            zone_size=(2000,130+50),
            zone_pos=(0,1005-50),
            target_obj_id= player_id
        )
    )


    platform_out = level.add_object(
        class_type="Moving",
        physics=True,
        physics_type="Unstoppable",
        params=MovingObjectInfoParams(
            pos=(1800, 830),
            sprite_id=platform_bug_spr_id,
            max_speed_x=100,
            max_speed_y=100,
            velocity_x=0,
            velocity_y=0,
            ground_friction_x=0,
            air_friction_x=0,
            air_friction_y=0,
            gravitate=False
        ),
        layer=1,
        force_active=False,
        need_hitbox=True
    )

    out_flight = level.add_script(
        PatrolInfoParams(
            patrol_obj_id= platform_out,
            points=[(1800,830),(1800,300),(2500,300)],
            speed_y=100,
            speed_x=100,
            cyclic= False,
            enabled= False,
        )
    )

    out_flight_switcher = level.add_script(
        ScriptSwitcherInfoParams(
            scripts_toggle_on_ids=[out_flight],
            enabled=True,
            max_switches=1
        )
    )

    level.add_script(
        ZoneSwitchInfoParams(
            switcher_id= out_flight_switcher,
            zone_pos= (1850,830-10),
            zone_size= (60,20),
            target_obj_id= player_id
        )
    )

    level.add_script(
        ZoneSwitchInfoParams(
            switcher_id= move_switcher_id,
            zone_pos= (1850,830-10),
            zone_size= (60,20),
            target_obj_id= player_id
        )
    )

    level.add_script(
        ZoneSwitchInfoParams(
            zone_pos= (2200, 300),
            zone_size= (100,100),
            target_obj_id= player_id,
            switcher_id = switcher_to_next
        )
    )







    #zombies #todo
    zombie_sprite_id = level.add_sprite(path= "assets/characters/NPC/passive/office-zombie/office_zombie.png", size= (100,120))

    door_play_sound = level.add_script(
        PlaySoundInfoParams(
            sound=door_sound_path
        )
    )

    zombie0_id = level.add_object(
    class_type="Moving",
    physics=True,
    physics_type="Stoppable",
    params=MovingObjectInfoParams(
        pos=(940, 1000),
        sprite_id=zombie_sprite_id,
        max_speed_x=50,
        max_speed_y=400,
        ground_friction_x=6,
        air_friction_y=0.05,
        air_friction_x=0,
        velocity_y=0,
        velocity_x=0,
        gravitate= True
    ),
    layer=2
    )

    num = 7
    core = "assets/characters/NPC/passive/office-zombie/walk_zombie_left/"
    sprites = [level.add_sprite(path=f"{core}{i}.png", size=(100, 120)) for i in range(0, num)]

    level.add_animation(
        object_id=zombie0_id,
        name="left",
        delay=1.5 / num,
        frames_ids=sprites,
        change_hitboxes=False
    )

    level.add_script(
        NpcMoveLeftInfoParams(
            obj_id= zombie0_id,
            ground_acceleration = 1000,
            air_acceleration = 100,
            max_speed= 20,
            enabled = True,
            anim= True
        )
    )

    left_zombie_teleport = level.add_script(
        TeleportObjectInfoParams(
            target_id= zombie0_id,
            pos=(940,1000)
        )
    )

    switcher_left_zombie = level.add_script(
        ScriptSwitcherInfoParams(
            scripts_toggle_on_ids=[left_zombie_teleport, door_play_sound],
            enabled= True
        )
    )

    level.add_script(
        ZoneSwitchInfoParams(
            zone_pos=(-150,900),
            zone_size=(20,300),
            target_obj_id= zombie0_id,
            switcher_id= switcher_left_zombie,
            enabled= True
        )
    )








    zombie1_id = level.add_object(
        class_type="Moving",
        physics=True,
        physics_type="Stoppable",
        params=MovingObjectInfoParams(
            pos=(1600, 1000),
            sprite_id=zombie_sprite_id,
            max_speed_x=50,
            max_speed_y=400,
            ground_friction_x=6,
            air_friction_y=0.05,
            air_friction_x=0,
            velocity_y=0,
            velocity_x=0,
            gravitate=True
        ),
        layer=2
    )

    num = 7
    core = "assets/characters/NPC/passive/office-zombie/walk_zombie_right/"
    sprites = [level.add_sprite(path=f"{core}{i}.png", size=(100, 120)) for i in range(0, num)]

    level.add_animation(
        object_id=zombie1_id,
        name="right",
        delay=1.5 / num,
        frames_ids=sprites,
        change_hitboxes=False
    )

    level.add_script(
        NpcMoveRightInfoParams(
            obj_id=zombie1_id,
            ground_acceleration=1000,
            air_acceleration=100,
            max_speed=20,
            enabled=True,
            anim=True
        )
    )

    right_zombie_teleport = level.add_script(
        TeleportObjectInfoParams(
            target_id=zombie1_id,
            pos=(1040, 1000)
        )
    )

    switcher_right_zombie = level.add_script(
        ScriptSwitcherInfoParams(
            scripts_toggle_on_ids=[right_zombie_teleport, door_play_sound],
            enabled=True
        )
    )

    level.add_script(
        ZoneSwitchInfoParams(
            zone_pos=(2000+150, 900),
            zone_size=(20, 300),
            target_obj_id=zombie1_id,
            switcher_id=switcher_right_zombie,
            enabled=True
        )
    )



    # scripts #todo
    level.add_script(LogInfoParams(player_id))

    # #tmp
    # mouse_script_id = level.add_script(MousePositionInfoParams())
    # level.add_binds('mouse_press', pygame.BUTTON_LEFT, mouse_script_id)
    # mouse_tp_script_id = level.add_script(
    #     MouseTeleportInfoParams(
    #         target_id= player_id
    #     )
    # )
    # level.add_binds('mouse_press', pygame.BUTTON_RIGHT, mouse_tp_script_id)


    level.save_to_file(level_path)


def create_level_3_coming_soon():
    level_path = "saves/level3/level3.json"

    level = Level()
    #level.screen_size = (1152, 648)
    level.screen_size = (1920, 1080)
    level.size = (1920, 1080)
    level.g = 10 * 16 * 2

    sounds_volume = 0.2
    music_volume = 0.2

    # camera boxes
    level.add_cam_box(
        hitbox=HitboxParams(
            pos=(0, 0),
            size=(level.size[0] - level.screen_size[0], level.size[1] - level.screen_size[1])
        )
    )


    # player #todo
    char_size = (47, 94)
    player_sprite_id = level.add_sprite(
        path="assets/characters/ANDY/andy.png",
        size=char_size
    )

    player_id = level.set_player(
        physics=False,
        params=PlayerObjectInfoParams(
            pos=(500, 500),
            sprite_id=player_sprite_id,

            max_speed_x=0,
            max_speed_y=0,
            ground_friction_x=0,
            air_friction_x=0,
            air_friction_y=0,
            gravitate=False,
            velocity_x=0,
            velocity_y=0,

            lives=0
        ),
        layer=None,
        force_active=True,
        need_hitbox=False
    )









    # background #todo
    bg_sprite_id = level.add_sprite(
        path = "assets/pictures/game/background_game/bg_soon.png",
        size=(1920,1080),
        hb_size = (0,0),
        hb_offset = (0,0)
    )

    level.add_object(
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





    level.add_script(
        MusicPlayerInfoParams(
            enabled=True,
            playlist=[
                ('assets/audio/game/game_music/1.mp3', music_volume),
                ('assets/audio/game/game_music/0.mp3', music_volume)
            ]
        )
    )


    level.save_to_file(level_path)



#def create_test_level():
#     level = Level()
#     level.size = (5000,1080)
#
#     player_sprite_id = level.add_sprite(
#         path ='assets/test_level/character/char0.png'
#     )
#
#     #player
#     player_id = level.set_player(
#         params=PlayerObjectInfoParams(
#             pos = (0,0),
#             sprite_id = player_sprite_id,
#
#             max_speed_x = 10*16,
#             max_speed_y = 20*16,
#             ground_friction_x = 3,
#             air_friction_x = 0.05,
#             air_friction_y = 0,
#             gravitate = True,
#             velocity_x = 0,
#             velocity_y = 0,
#
#             lives = 5
#         ),
#         physics = True,
#         physics_type = 'Stoppable',
#         layer = 1,
#         force_active = True
#     )
#
#     mario_sprite_id = level.add_sprite("assets/character/mario.png")
#     #mario1
#     mario_id = level.add_object(
#         params= MovingObjectInfoParams(
#             pos = (30, 1080-70-70-70-70-35),
#             sprite_id = mario_sprite_id,
#             max_speed_x= 5*16,
#             max_speed_y=20*16,
#             gravitate= True,
#             velocity_x=0,
#             velocity_y=0,
#             ground_friction_x = 3,
#             air_friction_x = 0.05,
#             air_friction_y = 0
#         ),
#         physics = True,
#         physics_type = 'Stoppable',
#         layer=1,
#         force_active=False,
#         class_type= 'Moving'
#     )
#
#     #mario2
#     mario2_id = level.add_object(
#         params=MovingObjectInfoParams(
#             pos=(1500, 1080 - 70 - 70 - 70),
#             sprite_id=mario_sprite_id,
#             max_speed_x=10 * 16,
#             max_speed_y=20 * 16,
#             gravitate=True,
#             velocity_x=0,
#             velocity_y=0,
#             ground_friction_x=3,
#             air_friction_x=0.05,
#             air_friction_y=0
#         ),
#         physics=True,
#         physics_type='Stoppable',
#         layer=1,
#         force_active=False,
#         class_type='Moving'
#     )
#
#     background_sprite_id = level.add_sprite("assets/background/background.png",)
#
#     #background
#     level.add_object(
#         class_type="Static",
#         physics=False,
#         layer=0,
#         need_hitbox= False,
#         params=StaticObjectInfoParams(
#             pos=(0, 0),
#             sprite_id=background_sprite_id
#         )
#
#     )
#
#     brick_sprite_id = level.add_sprite("assets/test/brick.png")
#
#     #ground
#     for i in range(73):
#         level.add_object(
#             class_type = "Static",
#             physics = True,
#             physics_type = "Static",
#             layer = 1,
#             params = StaticObjectInfoParams(
#                 pos = (i * 70, 1080-35),
#                 sprite_id = brick_sprite_id
#             )
#         )
#
#     #platform
#     for i in range(100, 5000, 70):
#         for j in range(0, 1080 - 35 * 3, 35):
#             if random.randint(0, 100) % 100 == 0:
#                 level.add_object(
#                     class_type="Static",
#                     physics=True,
#                     physics_type="Static",
#                     layer=1,
#                     params=StaticObjectInfoParams(
#                         pos=(i,j),
#                         sprite_id = brick_sprite_id
#                     )
#                 )
#
#     #the_flying_brick
#     level.add_object(
#         class_type = "Moving",
#         physics = True,
#         physics_type = "Unstoppable",
#         layer=1,
#         params= MovingObjectInfoParams
#         (
#             pos = (-200, 1080-70-70-70-70-35),
#             sprite_id= brick_sprite_id,
#
#             max_speed_x = 5*16,
#             max_speed_y = 5*16,
#             gravitate = False,
#             velocity_x = 25,
#             velocity_y = -5,
#             ground_friction_x=0,
#             air_friction_x=0,
#             air_friction_y=0
#         )
#     )
#
#     #cam_boxes
#     level.add_cam_box(
#         hitbox= HitboxParams(
#             pos = (0,0),
#             size = (5000-1920,0)
#         )
#     )
#
#     flag_sprite_id = level.add_sprite('assets/test/flagbox.png')
#
#     #flag
#     flag_id = level.add_object(
#         class_type = "Static",
#         physics = False,
#         force_active = False,
#         layer = None,
#         need_hitbox= True,
#         params= StaticObjectInfoParams(
#             pos = (70,1080-500),
#             sprite_id = flag_sprite_id
#         )
#     )
#
#     jump_sound_path = 'assets/test_level/sound/jump.mp3'
#     zombie_path = "assets/test_level/sound/zombie.mp3"
#
#     anim_name = 'rotate'
#
#     anim_sprite_id1 = level.add_sprite("assets/character/char0.png", size=(100,100))
#     anim_sprite_id2 = level.add_sprite("assets/character/char1.png", size=(100,100))
#
#     level.add_animation(
#         object_id=player_id,
#         name=anim_name,
#         delay=2,
#         frames_ids=[anim_sprite_id1, anim_sprite_id2],
#         change_hitboxes= True
#     )
#
#     level.add_sound('sound', jump_sound_path,0.1)
#     level.add_sound('sound', zombie_path, 0.3)
#
#     level.add_script(LogInfoParams(player_id))
#     level.add_script(MarioChaseInfoParams(mario_id,player_id))
#     level.add_script(PatrolInfoParams(mario2_id, [(1500,970),[2000,970]]))
#
#     zombie_sound_id = level.add_script(PlaySoundInfoParams(zombie_path))
#     anim_change_id = level.add_script(ChangeAnimInfoParams(target_id= player_id, animation_name = anim_name))
#
#
#     switcher_id = level.add_script(ScriptSwitcherInfoParams(scripts_switch_ids=[anim_change_id], scripts_toggle_on_ids=[zombie_sound_id], enabled= True))
#     level.add_script(FlagSwitchInfoParams(flag_obj_id= flag_id, target_obj_id= player_id,switcher_id = switcher_id, enabled = True))
#
#
#
#     m_l_id = level.add_script(MoveLeftInfoParams(player_id, 500, 50, 10 * 16))
#     m_r_id = level.add_script(MoveRightInfoParams(player_id, 500, 50, 10 * 16))
#     #j_id = level.add_script(JumpInfoParams(player_id,20*16))
#
#     level.add_binds('press', pygame.K_a, m_l_id)
#     level.add_binds('release', pygame.K_a, m_l_id)
#     level.add_binds('press', pygame.K_d, m_r_id)
#     level.add_binds('release', pygame.K_d, m_r_id)
#     #level.add_binds('hold', pygame.K_w, j_id)
#     #level.add_binds('hold', pygame.K_SPACE, j_id)
#     #level.add_binds('mouse_hold', pygame.BUTTON_LEFT, j_id)
#     return level