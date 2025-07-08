from __future__ import annotations

import pygame.mixer

from game.engine.script_system import ScriptParams, ScriptInfoParams, Script, CommandScript
from game.engine.objects import Hitbox


def script_fabric_method(type_ : str, params : ScriptParams) -> Script:
    match type_:
        case 'Log':
            return LogScript(params)
        case 'MarioChase':
            return MarioChaseScript(params)
        case 'Patrol':
            return Patrol(params)
        case 'MoveRightCommand':
            return MoveRightScript(params)
        case 'MoveLeftCommand':
            return MoveLeftScript(params)
        case 'JumpCommand':
            return JumpScript(params)
        case 'ScriptSwitcher':
            return ScriptSwitcher(params)
        case 'FlagSwitch':
            return FlagSwitchScript(params)
        case 'PlaySound':
            return PlaySoundScript(params)
        case 'ChangeAnim':
            return ChangeAnim(params)
        case 'MovementSystem':
            return MovementSystemScript(params)
        case "MousePosition":
            return MousePosition(params)
        case "AppearedObject":
            return AppearedObject(params)
        case 'PlatformAppearSystem':
            return PlatformAppearSystem(params)
        case 'ZoneSwitch':
            return ZoneSwitchScript(params)
        case 'MovementSwitcher':
            return MovementSwitcher(params)
        case 'MouseTeleport':
            return MouseTeleport(params)
        case 'MusicPlayer':
            return MusicPlayer(params)
        case 'ChangeLevel':
            return ChangeLevel(params)
        case _:
            return Script(params)


class LogInfoParams(ScriptInfoParams):
    def __init__(self, object_id : int):
        super().__init__()
        self.enabled = True
        self.type = 'Log'
        self.camera = True
        self.clock = True
        self.objects.append(object_id)
        self.systems['activity_manager'] = True

class LogScript(Script):
    def __init__(self, params : ScriptParams):
        super().__init__(params)
        self.camera = params['camera']
        self.clock = params['clock']
        self.player = params['objects'][0]
        self.activity_manager = params['systems']['activity_manager']

        self.game_time = 0
        self.log_delay = 0

    def start(self) -> None:
        self.enabled = True
        print("LogScript start working")

    def stop(self) -> None:
        self.enabled = False

    def destroy(self) -> None:
        self.kill = True

    def update(self, dt: float) -> None:
        self.game_time += dt
        self.log_delay += dt
        if self.log_delay > 5:
            print("активных объектов:", len(self.activity_manager.get_active_objects()))
            print(
                f"camera: {self.camera.x, self.camera.y}, player: {self.player.x, self.player.y}, fps: {self.clock.get_fps()}, frame_time: {dt}")
            print("game time:", self.game_time, "player lives:",self.player.lives)
            self.log_delay = 0


class MarioChaseInfoParams(ScriptInfoParams):
    def __init__(self, chase_object_id : int, target_id : int):
        super().__init__()
        self.type = 'MarioChase'
        self.enabled = True
        self.objects = [chase_object_id, target_id]

class MarioChaseScript(Script):
    def __init__(self, params : ScriptParams) -> None:
        super().__init__(params)
        self.chase_object = params['objects'][0]
        self.target = params['objects'][1]

    def start(self) -> None:
        self.enabled = True
        print("Марио вышел на охоту")

    def stop(self) -> None:
        self.enabled = False

    def destroy(self) -> None:
        print("и устал")
        self.kill = True

    def update(self, dt) -> None:
        c1 = self.chase_object.get_centre()
        c2 = self.target.get_centre()
        dx = c2[0]-c1[0]
        dy = c2[1]-c1[1]
        if (dx**2 + dy**2)**0.5 < 100:
            print("Догнал", end = '')
            self.destroy()
            return

        if self.chase_object.is_grounded:
            if self.chase_object.is_grounded:
                if abs(dy) > abs(dx) and abs(dx) < 200:
                    self.chase_object.velocity_y = -self.chase_object.max_speed_y
                    self.chase_object.is_grounded = False

                self.chase_object.velocity_x = dx
        else:
            if dx>0:
                self.chase_object.velocity_x += 0.005*self.chase_object.max_speed_x
            if dx<0:
                self.chase_object.velocity_x +=-  0.005*self.chase_object.max_speed_x

        if self.chase_object.velocity_x > self.chase_object.max_speed_x:
            self.chase_object.velocity_x = self.chase_object.max_speed_x
        elif self.chase_object.velocity_x < - self.chase_object.max_speed_x:
            self.chase_object.velocity_x = - self.chase_object.max_speed_x


class PatrolInfoParams(ScriptInfoParams):
    def __init__(self, patrol_obj_id : int, points : list[tuple[float,float]],
                 speed_x : float = 100, speed_y : float = -1, cyclic : bool = True,
                 teleport : bool = False, reach_distance : float = 5, enabled : bool = True):
        super().__init__()
        self.enabled = enabled
        self.type = 'Patrol'
        self.objects.append(patrol_obj_id)
        self.other = {
            'points' : points,
            'speed_x' : speed_x,
            'speed_y' : speed_y,
            'cyclic' : cyclic,
            'teleport' : teleport,
            'reach_distance' : reach_distance
        }

class Patrol(Script):
    def __init__(self, params : ScriptParams) -> None:
        super().__init__(params)
        self.obj = params['objects'][0]
        other = params['other']
        self.points = other['points']
        self.speed_x = other['speed_x']
        self.speed_y = other['speed_y']
        self.cyclic = other['cyclic']
        self.teleport = other['teleport']
        self.arrival_threshold = other['reach_distance']

        self.current_point_index = 0
        self.is_moving = True

    def start(self) -> None:
        self.enabled = True
        if self.points and self.teleport:
            self.obj.x, self.obj.y = self.points[0]
        print(f"Patrol started with {len(self.points)} points")

    def stop(self) -> None:
        self.enabled = False
        self.obj.velocity_x = 0
        self.obj.velocity_y = 0

    def destroy(self) -> None:
        self.kill = True

    def update(self, dt: float) -> None:
        if not self.enabled or not self.is_moving or not self.points or not self.obj.is_active:
            return

        current_target = self.points[self.current_point_index]
        obj_pos = (self.obj.x, self.obj.y)

        dx = current_target[0] - obj_pos[0]
        dy = current_target[1] - obj_pos[1]

        x_reached = self.speed_x == -1 or abs(dx) <= self.arrival_threshold
        y_reached = self.speed_y == -1 or abs(dy) <= self.arrival_threshold

        if x_reached and y_reached:
            if self.speed_x != -1:
                self.obj.x = current_target[0]
            if self.speed_y != -1:
                self.obj.y = current_target[1]
            self.next_point()
            return

        direction_x = 0
        direction_y = 0
        distance = (dx ** 2 + dy ** 2) ** 0.5

        if distance > 0:
            direction_x = dx / distance
            direction_y = dy / distance

        if self.speed_x != -1:
            self.obj.velocity_x = direction_x * self.speed_x

        if self.speed_y != -1:
            self.obj.velocity_y = direction_y * self.speed_y

    def next_point(self) -> None:
        self.current_point_index += 1

        if self.current_point_index >= len(self.points):
            if self.cyclic:
                self.current_point_index = 0
            else:
                self.is_moving = False
                self.obj.velocity_x = 0
                self.obj.velocity_y = 0
                self.stop()

    def resume(self) -> None:
        self.is_moving = True

    def pause(self) -> None:
        self.is_moving = False

    def set_speed_x(self, speed: float) -> None:
        self.speed_x = speed

    def set_speed_y(self, speed: float) -> None:
        self.speed_y = speed

    def add_point(self, point: tuple[float, float]) -> None:
        self.points.append(point)

    def skip_to_point(self, index: int) -> None:
        if 0 <= index < len(self.points):
            self.current_point_index = index


class MoveRightInfoParams(ScriptInfoParams):
    def __init__(self, obj_id : int, ground_acceleration : float, air_acceleration : float, max_speed : float):
        super().__init__()
        self.enabled = False
        self.type = 'MoveRightCommand'
        self.objects.append(obj_id)
        self.other = {
            'ground_acceleration' : ground_acceleration,
            'air_acceleration' : air_acceleration,
            'max_speed' : max_speed
        }

class MoveRightScript(CommandScript):
    def __init__(self, params : ScriptParams):
        super().__init__(params)
        self.obj = params['objects'][0]

        other = params['other']
        self.ground_acceleration = other['ground_acceleration']
        self.air_acceleration = other['air_acceleration']
        self.max_speed = other['max_speed']

        self.running = False

        self.first_time = True

        self.block = False

    def start(self):
        if not self.block:
            self.running = True
        #print("Побежал вправо")
        # анимация бега вправо

    def on_execute(self, dt : float, press : bool = False, hold : bool = False, release : bool = False) -> None:
        if self.first_time :
            self.enabled = True
            self.first_time = False

        if press:
            self.start()
            return
        if release:
            self.stop()
            return

    def update(self, dt: float) -> None:
        if self.running:
            if self.obj.is_grounded:
                self.obj.velocity_x = min(self.max_speed, self.obj.velocity_x + dt*self.ground_acceleration)
            else:
                self.obj.velocity_x = min(self.max_speed, self.obj.velocity_x + dt*self.air_acceleration)

    def stop(self):
        self.running = False
        #print("Постоял")
        # отмена анимации(мб остановка)

    def destroy(self) -> None:
        self.kill = True


class MoveLeftInfoParams(ScriptInfoParams):
    def __init__(self, obj_id : int, ground_acceleration : float, air_acceleration : float, max_speed : float):
        super().__init__()
        self.enabled = False
        self.type = 'MoveLeftCommand'
        self.objects.append(obj_id)
        self.other = {
            'ground_acceleration' : ground_acceleration,
            'air_acceleration' : air_acceleration,
            'max_speed' : max_speed
        }

class MoveLeftScript(CommandScript):
    def __init__(self, params : ScriptParams):
        super().__init__(params)
        self.obj = params['objects'][0]

        other = params['other']
        self.ground_acceleration = other['ground_acceleration']
        self.air_acceleration = other['air_acceleration']
        self.max_speed = other['max_speed']

        self.running = False

        self.first_time = True

        self.block = False

    def start(self):
        if not self.block:
            self.running = True
        #print("Побежал влево")
        # анимация бега вправо

    def on_execute(self, dt : float, press : bool = False, hold : bool = False, release : bool = False) -> None:
        if self.first_time:
            self.enabled = True
            self.first_time = False

        if press:
            self.start()
            return
        if release:
            self.stop()
            return

    def update(self, dt: float) -> None:
        if self.running:
            if self.obj.is_grounded:
                self.obj.velocity_x = max(-self.max_speed, self.obj.velocity_x - dt * self.ground_acceleration)
            else:
                self.obj.velocity_x = max(-self.max_speed, self.obj.velocity_x - dt * self.air_acceleration)

    def stop(self):
        self.running = False
        #print("Постоял")
        # отмена анимации(мб остановка)

    def destroy(self) -> None:
        self.kill = True


class JumpInfoParams(ScriptInfoParams):
    def __init__(self, obj_id : int, jump_speed : float, jump_sound : str, land_sound : str):
        super().__init__()
        self.enabled = False
        self.type = 'JumpCommand'

        self.systems['sound_engine'] = True

        self.objects.append(obj_id)

        self.other = {
            'jump_speed' : jump_speed,
            'jump_sound' : jump_sound,
            'land_sound' : land_sound
        }
        #self.other['jump_anim'] = jump_anim

class JumpScript(CommandScript):
    def __init__(self, params : ScriptParams):
        super().__init__(params)

        self.obj = params['objects'][0]
        self.sound_engine = params['systems']['sound_engine']


        other = params['other']
        self.jump_sound = other['jump_sound']
        self.jump_speed = other['jump_speed']
        self.land_sound = other['land_sound']

        self.block = False

    def start(self) -> None:
        if self.obj.is_grounded and not self.block:
            self.obj.velocity_y = max(-self.jump_speed, -self.obj.max_speed_y)

            self.sound_engine.play_sound(self.jump_sound)

            self.obj.is_grounded = False
            self.enabled = True


    def on_execute(self, dt : float, press : bool = False,hold : bool = False, release : bool = False) -> None:
        if press:
            self.start()
        elif release:
            self.start()
        elif hold:
            self.start()

    def update(self, dt: float) -> None:
        if self.obj.is_grounded:
            self.stop()

    def stop(self) -> None:
        self.enabled = False

    def destroy(self) -> None:
        self.kill = True


class ScriptSwitcherInfoParams(ScriptInfoParams):
    def __init__(self,max_switches : int = -1, scripts_switch_ids : list[int] = None,
                 scripts_toggle_on_ids : list[int] = None, scripts_toggle_off_ids : list[int] = None, enabled : bool = True):
        super().__init__()
        self.type = 'ScriptSwitcher'
        self.enabled = enabled


        if scripts_switch_ids:
            self.scripts += scripts_switch_ids
        if scripts_toggle_on_ids:
            self.scripts += scripts_toggle_on_ids
        if scripts_toggle_off_ids:
            self.scripts += scripts_toggle_off_ids

        self.other = {
            "switch" : len(scripts_switch_ids) if scripts_switch_ids else 0,
            "toggle_on" : len(scripts_toggle_on_ids) if scripts_toggle_on_ids else 0,
            "toggle_off" : len(scripts_toggle_off_ids) if scripts_toggle_off_ids else 0,
            "switches" : max_switches
        }

class ScriptSwitcher(Script):
    def __init__(self, params : ScriptParams):
        super().__init__(params)

        all_scripts = params['scripts']
        other = params['other']

        self.scripts_switch : list[Script] = all_scripts[0:other['switch']]
        self.scripts_toggle_on : list[Script] = all_scripts[other['switch']:other['switch']+other['toggle_on']]
        self.scripts_toggle_off : list[Script] = all_scripts[other['switch']+other['toggle_on'] : other['switch']+other['toggle_on'] + other['toggle_off']]
        self.max_switches = other['switches']

        self.need_switch = False

        self.switches = 0


    def destroy(self) -> None:
        self.kill = True

    def stop(self) -> None:
        self.enabled = False

    def start(self) -> None:
        self.enabled = True

    def update(self, dt: float) -> None:
        if self.need_switch:
            self.switch()
            self.need_switch = False

    def switch(self):
        for script in self.scripts_switch:
            if script.enabled:
                script.stop()
            else:
                script.start()
        for script in self.scripts_toggle_on:
            script.start()
        for script in self.scripts_toggle_off:
            script.stop()
        self.switches += 1
        if self.switches == self.max_switches and self.max_switches != -1:
            self.destroy()


class FlagSwitchInfoParams(ScriptInfoParams):
    def __init__(self, flag_obj_id : int, target_obj_id : int, switcher_id : int, enabled : bool = True):
        super().__init__()
        self.enabled = enabled
        self.type = "FlagSwitch"

        self.objects = [flag_obj_id, target_obj_id]
        self.scripts = [switcher_id]

class FlagSwitchScript(Script):
    def __init__(self, params: ScriptParams) -> None:
        super().__init__(params)

        self.flag_obj = params['objects'][0]
        self.target_obj = params['objects'][1]

        self.switcher = params['scripts'][0]

        self.target_in_zone = False

    def destroy(self) -> None:
        self.kill = True

    def stop(self) -> None:
        self.enabled = False

    def start(self) -> None:
        self.enabled = True

    def update(self, dt: float) -> None:
        collide = self.flag_obj.hitbox.is_collide(self.target_obj.hitbox)

        if collide and not self.target_in_zone:
            self.target_in_zone = True
            self.switcher.need_switch = True
        if not collide and self.target_in_zone:
            self.target_in_zone = False


class PlaySoundInfoParams(ScriptInfoParams):
    def __init__(self, sound : str, loops : int = 0, volume : float = None , enabled : bool = False):
        super().__init__()
        self.type = "PlaySound"
        self.enabled = enabled

        self.systems['sound_engine'] = True

        self.other = {
            'sound' : sound,
            'loops' : loops,
            'volume' : volume
        }

class PlaySoundScript(Script):
    def __init__(self, params: ScriptParams) -> None:
        super().__init__(params)
        self.sound_engine = params['systems']['sound_engine']

        other = params['other']
        self.sound = other['sound']
        self.loops = other['loops']
        self.volume = other['volume']

    def destroy(self) -> None:
        self.kill = True

    def start(self) -> None:
        self.play()
        self.enabled = True

    def play(self):
        self.sound_engine.play_sound(name = self.sound, loops = self.loops, volume= self.volume)

    def stop(self) -> None:
        self.enabled = False

    def update(self, dt: float) -> None:
        pass


class ChangeAnimInfoParams(ScriptInfoParams):
    def __init__(self, target_id : int, animation_name : str, cycle : bool = True, enabled = False):
        super().__init__()
        self.enabled = enabled
        self.type = 'ChangeAnim'

        self.systems['animation_engine'] = True

        self.objects.append(target_id)
        self.other = {
            'name' : animation_name,
            'cycle' : cycle
        }

class ChangeAnim(Script):
    def __init__(self, params : ScriptParams):
        super().__init__(params)

        self.animation_engine = params['systems']['animation_engine']

        self.target = params['objects'][0]

        other = params['other']
        self.anim_name = other['name']
        self.cycle = other['cycle']

    def start(self) -> None:
        self.animation_engine.switch_anim(obj= self.target, animation_name= self.anim_name, play_now= True, cycle = self.cycle)
        self.enabled = True

    def stop(self) -> None:
        self.animation_engine.turn_off(obj = self.target)
        self.enabled = False

    def update(self, dt: float) -> None:
        pass

    def destroy(self) -> None:
        self.kill = True


class MovementSystemInfoParams(ScriptInfoParams):
    def __init__(self, target_id : int, m_l_scr_id : int, m_r_scr_id : int, j_scr_id : int, fall_sound : str = None,
                 land_sound : str = None, walk_sound : str = None, damage_sound : str = None, fall_damage_threshold : int = 500, enabled : bool = True):
        super().__init__()
        self.enabled = enabled
        self.type = 'MovementSystem'

        self.systems['animation_engine'] = True
        self.systems['sound_engine'] = True

        self.scripts = [m_l_scr_id, m_r_scr_id, j_scr_id]
        self.objects = [target_id]

        self.other = {
            'land_sound': land_sound,
            'fall_sound': fall_sound,
            'walk_sound': walk_sound,
            'damage_sound' : damage_sound,
            'fall_damage_threshold' : fall_damage_threshold
        }

class MovementSystemScript(Script):
    def __init__(self, params: ScriptParams) -> None:
        super().__init__(params)
        self.animation_engine = params['systems']['animation_engine']
        self.sound_engine = params['systems']['sound_engine']

        self.m_l_script = params['scripts'][0]
        self.m_r_script = params['scripts'][1]
        self.j_script = params['scripts'][2]

        self.target = params['objects'][0]

        other = params['other']
        self.land_sound = other.get('land_sound')
        self.fall_sound = other.get('fall_sound')
        self.walk_sound = other.get('walk_sound')
        self.damage_sound = other.get('damage_sound')

        self.moving_left = False
        self.moving_right = False

        self.last_direction = "right"
        self.current_anim = None

        self.was_falling = False
        self.is_walk_sound_playing = False

        self.fall_damage_threshold = other.get('fall_damage_threshold')
        self.fall_start_y = 0
        self.is_falling = False
        self.max_fall_speed = 0

    def destroy(self) -> None:
        self.kill = True

    def start(self) -> None:
        self.enabled = True

    def stop(self) -> None:
        self.enabled = False

    def update(self, dt: float) -> None:
        is_falling = not self.target.is_grounded and self.target.velocity_y > 0

        if is_falling:
            if not self.is_falling:
                self.is_falling = True
                self.fall_start_y = self.target.y
                self.max_fall_speed = 0
            else:
                if self.target.velocity_y > self.max_fall_speed:
                    self.max_fall_speed = self.target.velocity_y
        elif self.target.is_grounded and self.is_falling:
            self.is_falling = False
            fall_height = self.target.y - self.fall_start_y

            if (fall_height > self.fall_damage_threshold or
                    self.max_fall_speed > self.target.max_speed_y * 0.8):
                if hasattr(self.target, 'lives'):
                    self.target.lives -= 1
                    if self.damage_sound: self.sound_engine.play_sound(self.damage_sound)

        if not self.was_falling and is_falling and self.fall_sound:
            self.sound_engine.play_sound(self.fall_sound)

        if self.was_falling and self.target.is_grounded and self.land_sound:
            self.sound_engine.play_sound(self.land_sound)
            self.sound_engine.stop_sound(self.fall_sound)

        self.was_falling = is_falling

        self.moving_left = self.m_l_script.running
        self.moving_right = self.m_r_script.running

        is_walking = (self.moving_left or self.moving_right) and self.target.is_grounded

        if is_walking:
            if not self.is_walk_sound_playing and self.walk_sound:
                self.sound_engine.play_sound(
                    name=self.walk_sound,
                    loops=-1
                )
                self.is_walk_sound_playing = True
        else:
            if self.is_walk_sound_playing and self.walk_sound:
                self.sound_engine.stop_sound(self.walk_sound)
                self.is_walk_sound_playing = False

        if self.moving_left:
            self.last_direction = "left"
        elif self.moving_right:
            self.last_direction = "right"

        new_anim = None

        if not self.target.is_grounded:
            if self.target.velocity_y < 0:  # Движение вверх
                new_anim = f"jump_{self.last_direction}"
            else:
                new_anim = f"fall_{self.last_direction}"
        else:
            if self.moving_left and not self.moving_right:
                new_anim = "walk_left"
            elif self.moving_right and not self.moving_left:
                new_anim = "walk_right"
            else:
                new_anim = f"stay_{self.last_direction}"

        if new_anim != self.current_anim:
            self.animation_engine.switch_anim(
                obj=self.target,
                animation_name=new_anim,
                play_now=True,
                cycle=True
            )
            self.current_anim = new_anim


class MousePositionInfoParams(ScriptInfoParams):
    def __init__(self, enabled : bool = True):
        super().__init__()
        self.type = "MousePosition"
        self.enabled =  enabled
        self.systems['input_manager'] = True

class MousePosition(CommandScript):
    def __init__(self, params: ScriptParams) -> None:
        super().__init__(params)

        self.input_handler = params['systems']['input_manager']

    def destroy(self) -> None:
        self.kill = True

    def stop(self) -> None:
        self.enabled = False

    def start(self) -> None:
        self.enabled = True

    def update(self, dt: float) -> None:
        pass

    def on_execute(self, dt: float, press: bool = False, hold: bool = False, release: bool = False) -> None:
        if press:
            print(f"Мышь: (x,y) = {self.input_handler.get_mouse_position()}")


class AppearedObjectInfoParams(ScriptInfoParams):
    def __init__(self, target_id : int, appear_sound : str = None, volume : float = 0.1, appear_anim : str = None):
        super().__init__()
        self.type = "AppearedObject"
        self.enabled = False
        self.objects = [target_id]

        self.other['appear_sound'] = (appear_sound, volume)
        self.other['appear_anim'] = appear_anim

class AppearedObject(Script):
    def __init__(self, params: ScriptParams) -> None:
        super().__init__(params)

        self.target = params['objects'][0]

        self.sound_engine = params['systems']['sound_engine']
        self.animation_engine = params['systems']['animation_engine']

        self.appear_sound = params['other']['appear_sound']
        self.appear_anim = params['other']['appear_anim']

        self.original_position = (self.target.x, self.target.y)

        self.target.move_to((-1000,-1000))

    def destroy(self) -> None:
        self.kill = True

    def start(self) -> None:
        if self.enabled:
            pass
        else:
            self.target.move_to(self.original_position)

            if self.appear_sound[0]:
                self.sound_engine.play_sound(name = self.appear_sound[0], volume= self.appear_sound[1])
            if self.appear_anim:
                self.animation_engine.switch_anim(animation_name= self.appear_anim, cycle= False)

            self.enabled = True

    def stop(self) -> None:
        pass

    def update(self, dt: float) -> None:
        pass


class PlatformAppearSystemInfoParams(ScriptInfoParams):
    def __init__(self, target_id : int, platforms_ids : list[int], flag_size : tuple[int,int] = (-1,-1),
                 appear_sounds: list[tuple[str, float] | None] = None,
                 appear_anims: list[str | None] = None, enabled : bool = True):
        super().__init__()
        self.enabled = enabled
        self.type = "PlatformAppearSystem"

        self.objects = [target_id] + platforms_ids

        self.other['flag_size'] = flag_size
        self.other['appear_sounds'] = appear_sounds or [None] * len(platforms_ids)
        self.other['appear_anims'] = appear_anims or [None] * len(platforms_ids)

        self.systems['animation_engine'] = True
        self.systems['sound_engine'] = True

class PlatformAppearSystem(Script):
    def __init__(self, params: ScriptParams):
        super().__init__(params)

        self.animation_engine = params['systems']['animation_engine']
        self.sound_engine = params['systems']['sound_engine']

        self.target = params['objects'][0]
        self.platforms = params['objects'][1:]
        self.orig_pos = [(i.x,i.y) for i in self.platforms]

        other = params['other']
        self.flag_size = other['flag_size']
        self.appear_sounds = other['appear_sounds']
        self.appear_anims = other['appear_anims']

        self.sound_engine = params['systems']['sound_engine']
        self.animation_engine = params['systems']['animation_engine']

        self.flag_size = (
            self.platforms[0].size[0] if self.flag_size[0] == -1 else self.flag_size[0],
            10
        )
        self.flags = self.create_flags()
        self.current_flag = None
        self.current_platform = 0

        for i in self.platforms:
            i.move_to((-10000,-10000))

    def destroy(self) -> None:
        self.kill = True

    def start(self) -> None:
        self.enabled = True
        self.platforms[0].move_to(self.orig_pos[0])
        self.play_sound_and_anim()
        self.current_flag = self.flags[0]

    def stop(self) -> None:
        self.enabled = False

    def update(self, dt: float) -> None:
        if self.current_flag:
            if self.current_platform == len(self.platforms) - 1:
                self.current_flag = None
            if self.target.hitbox.is_collide(self.current_flag):
                self.play_sound_and_anim()
                self.current_platform += 1
                self.platforms[self.current_platform].move_to(self.orig_pos[self.current_platform])
                self.current_flag = self.flags[self.current_platform]
        else:
            self.destroy()

    def play_sound_and_anim(self):
        sound_info = self.appear_sounds[self.current_platform]
        if sound_info:
            sound, volume = sound_info
            if volume == -1:
                self.sound_engine.play_sound(sound)
            else:
                self.sound_engine.play_sound(sound, volume=volume)

        anim_name = self.appear_anims[self.current_platform]
        if anim_name:
            self.animation_engine.switch_anim(
                obj = self.platforms[self.current_platform],
                animation_name=anim_name,
                play_now=True,
                cycle=False
            )

    def create_flags(self) -> list[Hitbox]:
        flags = []
        for platform in self.platforms:
            flags.append(
                Hitbox(
                    pos = ((platform.size[0] - self.flag_size[0])/2 + platform.hitbox.x, platform.hitbox.y - self.flag_size[1]),
                    size = self.flag_size
                )
            )
        return flags


class ZoneSwitchInfoParams(ScriptInfoParams):
    def __init__(self, zone_pos : tuple[float,float], zone_size : tuple[int,int], target_obj_id : int, switcher_id : int, enabled : bool = True):
        super().__init__()
        self.enabled = enabled
        self.type = "ZoneSwitch"

        self.objects = [target_obj_id]
        self.scripts = [switcher_id]

        self.other['zone_pos'] = zone_pos
        self.other['zone_size'] = zone_size

class ZoneSwitchScript(Script):
    def __init__(self, params: ScriptParams) -> None:
        super().__init__(params)

        self.target_obj = params['objects'][0]

        self.switcher = params['scripts'][0]

        other = params['other']
        self.hitbox = Hitbox(pos = other['zone_pos'], size=other['zone_size'])

        self.target_in_zone = False

    def destroy(self) -> None:
        self.kill = True

    def stop(self) -> None:
        self.enabled = False

    def start(self) -> None:
        self.enabled = True

    def update(self, dt: float) -> None:
        if self.switcher.kill:
            self.destroy()

        collide = self.hitbox.is_collide(self.target_obj.hitbox)

        if collide and not self.target_in_zone:
            self.target_in_zone = True
            self.switcher.need_switch = True
        if not collide and self.target_in_zone:
            self.target_in_zone = False


class MovementSwitcherInfoParams(ScriptInfoParams):
    def __init__(self, max_switches : int = -1, scripts_block_switch_ids : list[int] = None,
                 scripts_to_unblock_ids : list[int] = None, scripts_to_block_ids : list[int] = None, enabled : bool = True):
        super().__init__()
        self.type = 'MovementSwitcher'
        self.enabled = enabled


        if scripts_block_switch_ids:
            self.scripts += scripts_block_switch_ids
        if scripts_to_unblock_ids:
            self.scripts += scripts_to_unblock_ids
        if scripts_to_block_ids:
            self.scripts += scripts_to_block_ids

        self.other = {
            "switch" : len(scripts_block_switch_ids) if scripts_block_switch_ids else 0,
            "toggle_on" : len(scripts_to_unblock_ids) if scripts_to_unblock_ids else 0,
            "toggle_off" : len(scripts_to_block_ids) if scripts_to_block_ids else 0,
            "switches" : max_switches
        }

class MovementSwitcher(Script):
    def __init__(self, params : ScriptParams):
        super().__init__(params)

        all_scripts = params['scripts']
        other = params['other']

        self.scripts_switch : list[Script] = all_scripts[0:other['switch']]
        self.scripts_toggle_on : list[Script] = all_scripts[other['switch']:other['switch']+other['toggle_on']]
        self.scripts_toggle_off : list[Script] = all_scripts[other['switch']+other['toggle_on'] : other['switch']+other['toggle_on'] + other['toggle_off']]
        self.max_switches = other['switches']

        self.need_switch = False

        self.switches = 0

    def destroy(self) -> None:
        self.kill = True

    def stop(self) -> None:
        self.enabled = False

    def start(self) -> None:
        self.enabled = True

    def update(self, dt: float) -> None:
        if self.need_switch:
            self.switch()
            self.need_switch = False

    def switch(self):
        for script in self.scripts_switch:
            script.block = not script.block
        for script in self.scripts_toggle_on:
            script.block = False
        for script in self.scripts_toggle_off:
            script.block = True
            script.stop()
        self.switches += 1
        if self.switches == self.max_switches and self.max_switches != -1:
            self.destroy()


class MouseTeleportInfoParams(ScriptInfoParams):
    def __init__(self, target_id : int, enabled : bool = True):
        super().__init__()
        self.type = "MouseTeleport"
        self.enabled =  enabled
        self.systems['input_manager'] = True
        self.objects = [target_id]

class MouseTeleport(CommandScript):
    def __init__(self, params: ScriptParams) -> None:
        super().__init__(params)

        self.target = params['objects'][0]

        self.input_handler = params['systems']['input_manager']

    def destroy(self) -> None:
        self.kill = True

    def stop(self) -> None:
        self.enabled = False

    def start(self) -> None:
        self.enabled = True

    def update(self, dt: float) -> None:
        pass

    def on_execute(self, dt: float, press: bool = False, hold: bool = False, release: bool = False) -> None:
        if press:
            self.target.move_to(self.input_handler.get_mouse_position())


class MusicPlayerInfoParams(ScriptInfoParams):
    def __init__(self, playlist : list[tuple[str,float]], enabled : bool = False):
        super().__init__()
        self.type = "MusicPlayer"
        self.enabled = enabled

        self.systems['sound_engine'] = True

        self.other['playlist'] = playlist

class MusicPlayer(Script):
    def __init__(self, params: ScriptParams) -> None:
        super().__init__(params)
        self.sound_engine = params['systems']['sound_engine']

        self.playlist = params['other']['playlist']

        self.current_play = None

    def destroy(self) -> None:
        self.kill = True

    def start(self) -> None:
        self.play()
        self.enabled = True

    def play(self):
        self.current_play = self.playlist[0]
        if len(self.playlist) > 1:
            self.playlist = self.playlist[1:] + self.playlist[0]

        self.sound_engine.play_music(file_path=self.current_play[0], volume= self.current_play[1])


    def stop(self) -> None:
        self.enabled = False

    def update(self, dt: float) -> None:
        if not pygame.mixer.music.get_busy():
            self.play()
        pass


class ChangeLevelInfoParams(ScriptInfoParams):
    def __init__(self, to_num : int):
        super().__init__()
        self.type = 'ChangeLevel'
        self.enabled = False

        self.systems['game'] = True

        self.other['num'] = to_num

class ChangeLevel(Script):
    def __init__(self, params: ScriptParams) -> None:
        super().__init__(params)

        self.game = params['systems']['game']

        self.num = params['other']['num']
        
    def destroy(self) -> None:
        self.kill = True

    def start(self) -> None:
        self.enabled = True

        self.game.exit = True
        self.game.change_level = (True, self.num)

        self.destroy()

    def stop(self) -> None:
        self.enabled = False

    def update(self, dt: float) -> None:
        pass

#
# layer_system
# camera_manager
# activity_manager
# physic_engine
# animation_engine
# sound_engine
# input_manager
# script_system
#
# list[object]
#
# list[script]
#
# camera
#
# clock
#
# other parameters(not objects)
# ex. list[sound_path]
# ex. list[names of animations]
# ex. speed

# info_params
# systems : list[system : str] - системы которые нужны
# objects : list[object_id : int] - ид объектов которые нужны
# scripts : list[script_id : int] - ид скриптов которые нужны
#
# camera : bool
# clock : bool
#
# other parameters(not objects)