from __future__ import annotations
from game.engine.script_system import ScriptParams, ScriptInfoParams, Script, CommandScript

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
            print("game time:", self.game_time)
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
                 teleport : bool = False, reach_distance : float = 5):
        super().__init__()
        self.enabled = True
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

    def start(self):
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

    def start(self):
        self.running = True
        #print("Побежал влево")
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
    def __init__(self, obj_id : int, jump_speed : float, jump_sound : str):
        super().__init__()
        self.enabled = False
        self.type = 'JumpCommand'

        self.systems['sound_engine'] = True

        self.objects.append(obj_id)

        self.other = {
            'jump_speed' : jump_speed,
            'jump_sound' : jump_sound
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

    def start(self) -> None:
        if self.obj.is_grounded:
            self.obj.velocity_y = max(-self.jump_speed, -self.obj.max_speed_y)

            self.sound_engine.play_sound(self.jump_sound)

            self.obj.is_grounded = False
            self.enabled = True


    def on_execute(self, dt : float, press : bool = False,hold : bool = False, release : bool = False) -> None:
        if hold:
            self.start()

    def update(self, dt: float) -> None:
        if self.obj.is_grounded:
            self.stop()

    def stop(self) -> None:
        self.enabled = False

    def destroy(self) -> None:
        self.kill = True


class ScriptSwitcherInfoParams(ScriptInfoParams):
    def __init__(self, scripts_switch_ids : list[int] = None,
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
            "toggle_off" : len(scripts_toggle_off_ids) if scripts_toggle_off_ids else 0
        }

class ScriptSwitcher(Script):
    def __init__(self, params : ScriptParams):
        super().__init__(params)

        all_scripts = params['scripts']
        other = params['other']

        self.scripts_switch : list[Script] = all_scripts[0:other['switch']]
        self.scripts_toggle_on : list[Script] = all_scripts[other['switch']:other['switch']+other['toggle_on']]
        self.scripts_toggle_off : list[Script] = all_scripts[other['switch']+other['toggle_on'] : other['switch']+other['toggle_on'] + other['toggle_off']]

        self.need_switch = False

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
        collide = self.flag_obj.hitbox.is_collide(self.target_obj)

        if collide and not self.target_in_zone:
            self.target_in_zone = True
            self.switcher.need_switch = True
        if not collide and self.target_in_zone:
            self.target_in_zone = False


class ClickSwitchScript(Script):
    ...

class TimeSwitchScript(Script):
    ...

class TimeFlagSwitchScript(Script):
    ...


class PlaySoundInfoParams(ScriptInfoParams):
    def __init__(self, sound : str, loops : int = 0 , volume : float = None):
        super().__init__()
        self.type = "PlaySound"
        self.systems['sound_engine'] = True

        self.other = {
            'sound' : sound,
            'loops' : loops,
            'volume' : volume
        }

class PlaySoundScript(Script):
    def __init__(self, params : ScriptParams):
        super().__init__(params)

        self.sound_engine = params['systems']['sound_engine']

        other = params['other']
        self.sound = other['sound']
        self.loops = other['loops']
        self.volume = other['volume']

    def destroy(self) -> None:
        self.kill = True

    def start(self) -> None:
        self.enabled = True

    def stop(self) -> None:
        self.enabled = False

    def update(self, dt: float) -> None:
        self.sound_engine.play_sound(name = self.sound, loops = self.loops, volume = self.volume)
        self.stop()


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
# params:
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