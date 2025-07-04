from __future__ import annotations

import pygame
import json

from typing import TypedDict, NotRequired, Optional, Any

from game.engine.objects import StaticObject, MovingObject, Player, Hitbox
from game.engine.objects import StaticObjectParams, MovingObjectParams, PlayerObjectParams, HitboxParams
from game.engine.objects import StaticObjectInfoParams, MovingObjectInfoParams, PlayerObjectInfoParams
from game.engine.render import Camera, CameraManager, Layer, LayerSystem, ActivityManager
from game.engine.physics import PhysicEngine
from game.engine.animation import AnimationEngine
from game.engine.control import InputHandler, Command
from game.engine.script_system import ScriptingSystem, ScriptParams, ScriptInfoParams, Script
from game.engine.sound import SoundEngine
from game.subsystems.scripts import script_fabric_method
from game.subsystems.control_commands import PressCommand, HoldCommand, ReleaseCommand


class GameEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, tuple):
            return {'__tuple__': True, 'items': list(obj)}

        if hasattr(obj, '__dict__'):
            return {
                '__class__': obj.__class__.__name__,
                'module': obj.__class__.__module__,
                'data': obj.__dict__
            }

        return super().default(obj)


def game_hook(obj: dict) -> Any:
    if '__tuple__' in obj:
        return tuple(obj['items'])

    if '__class__' in obj:
        class_name = obj['__class__']
        module_name = obj['module']

        try:
            module = __import__(module_name, fromlist=[class_name])
            klass = getattr(module, class_name)
            instance = klass.__new__(klass)
            instance.__dict__.update(obj['data'])
            return instance
        except (ImportError, AttributeError):
            return obj

    return obj


class ObjectData(TypedDict):
    id : int
    class_type : str
    physics : bool
    physic_type : NotRequired[str]
    layer : NotRequired[int]
    force_active: bool
    need_hitbox : bool
    params : Optional[StaticObjectInfoParams, MovingObjectInfoParams, PlayerObjectInfoParams]


class AnimationData(TypedDict):
    object_id: int
    name: str
    delay: float
    frames: list[int]  # ID спрайтов
    change_hitboxes : bool


class SoundData(TypedDict):
    id : int
    type : str #music, sound
    filename : str
    volume : float


class ScriptData(TypedDict):
    id : int
    info_params : ScriptInfoParams


class BindData(TypedDict):
    id : int
    type : str #press, hold, release
    key : int
    command_script_id : int


class CamBoxData(TypedDict):
    id : int
    hitbox : HitboxParams


class HitboxData(TypedDict):
    id : int
    hitbox : HitboxParams


class SpriteData(TypedDict):
    id : int
    sprite_path : str
    sprite_size : tuple[int,int]
    hitbox_id : int


class Level:
    def __init__(self, size : tuple[int,int] = (0,0), g : float = 9.8*16):
        self.size : tuple[int,int] = size
        self.g : float = g

        self.sprites : list[SpriteData] = list()
        self.hitboxes : list[HitboxData] = list()

        self.objects : list[ObjectData | None] = list()
        self.objects.append(None)

        self.cam_boxes: list[CamBoxData] = list()
        self.animations : list[AnimationData] = list()
        self.sounds : list[SoundData] = list()
        self.scripts : list[ScriptData] = list()
        self.binds : list[BindData] = list()

    def _add_hitbox(self, size : tuple[int,int], pos : tuple[float,float] = None, offset : tuple[float,float] = (0,0)) -> int:
        params = HitboxParams(
                pos = pos,
                size = size,
                offset = offset
            )

        for id_ in range(len(self.hitboxes)):
            if self.hitboxes[id_]['hitbox'] == params:
                return id_

        used_ids = {obj['id'] for obj in self.hitboxes}
        new_id = 0
        while new_id in used_ids:
            new_id += 1

        data = HitboxData(
            id = new_id,
            hitbox = params
        )

        self.hitboxes.append(data)
        return new_id

    def _remove_hitbox(self, id_ : int) -> None:
        self.hitboxes = [hb for hb in self.hitboxes if hb['id'] != id_]

    def add_sprite(self, path : str, size : tuple[int, int] = None, hb_size : tuple[int, int] = None, hb_offset : tuple[float,float] = (0,0)) -> int:
        used_ids = {obj['id'] for obj in self.sprites}
        new_id = 0
        while new_id in used_ids:
            new_id += 1

        if not size:
            sprite = pygame.image.load(path)
            size = sprite.get_size()

        hb_id = self._add_hitbox(size = hb_size if hb_size else size, offset = hb_offset)

        data = SpriteData(
            id = new_id,
            sprite_path = path,
            sprite_size = size,
            hitbox_id = hb_id
        )

        self.sprites.append(data)
        return new_id

    def remove_sprite(self, id_ : int) -> None:
        self.sprites = [sprite for sprite in self.sprites if sprite['id'] != id_]

    def set_player(self, params : PlayerObjectInfoParams, layer : int = None, physics : bool = True, physics_type : str = 'Stoppable', force_active : bool = True, need_hitbox = True) -> int:
        data = ObjectData(
            id = 0,
            class_type = 'Player',
            physics = physics,
            params = params,
            layer = layer,
            physic_type = physics_type,
            force_active = force_active,
            need_hitbox= need_hitbox
        )
        self.objects[0] = data
        return 0

    def remove_player(self) -> None:
        self.objects[0] = None

    def add_object(self, class_type : str, physics : bool, params : Optional[StaticObjectInfoParams, MovingObjectInfoParams], layer : int = None, physics_type : str = None, force_active : bool = False, need_hitbox : bool = True) -> int:
        used_ids = {obj['id'] for obj in self.objects}
        new_id = 0
        while new_id in used_ids:
            new_id += 1

        data = ObjectData(
            id = new_id,
            class_type = class_type,
            physics = physics,
            params = params,
            layer = layer,
            physic_type = physics_type,
            force_active = force_active,
            need_hitbox= need_hitbox
        )

        self.objects.append(data)

        return new_id

    def remove_object(self, id_ : int) -> None:
        self.objects = [obj for obj in self.objects if obj['id'] != id_]

    def add_animation(self, object_id : int, name : str, delay : float, frames_ids : list[int], change_hitboxes : bool = True):
        self.animations.append(
            AnimationData(
                object_id = object_id,
                name = name,
                delay = delay,
                frames= frames_ids,
                change_hitboxes = change_hitboxes
            )
        )

    def remove_animation(self, object_id : int, name : str):
        self.animations = [anim for anim in self.animations
                           if not (anim['object_id'] == object_id and anim['name'] == name)]

    def add_sound(self, type_: str, filename: str, volume: float) -> int:
        used_ids = {sound['id'] for sound in self.sounds}
        new_id = 0
        while new_id in used_ids:
            new_id += 1

        sound = SoundData(
            id = new_id,
            type = type_,
            filename = filename,
            volume = volume)

        self.sounds.append(sound)

        return new_id

    def remove_sound(self, id_: int) -> None:
        self.sounds = [sound for sound in self.sounds if sound['id'] != id_]

    def add_script(self, info_params: ScriptInfoParams) -> int:
        used_ids = {script['id'] for script in self.scripts}
        new_id = 0
        while new_id in used_ids:
            new_id += 1

        script = ScriptData(
            id = new_id,
            info_params = info_params
        )

        self.scripts.append(script)

        return new_id

    def remove_script(self, id_: int) -> None:
        self.scripts = [script for script in self.scripts if script['id'] != id_]

    def add_binds(self, type_: str, key : int,command_script_id : int) -> int:
        used_ids = {bind['id'] for bind in self.binds}
        new_id = 0
        while new_id in used_ids:
            new_id += 1

        bind = BindData(
            id=new_id,
            type=type_,
            key = key,
            command_script_id = command_script_id
        )

        self.binds.append(bind)

        return new_id

    def remove_binds(self, id_: int) -> None:
        self.binds = [bind for bind in self.binds if bind['id'] != id_]

    def add_cam_box(self, hitbox: HitboxParams) -> int:
        used_ids = {box['id'] for box in self.cam_boxes}
        new_id = 0
        while new_id in used_ids:
            new_id += 1

        box = CamBoxData(
            id=new_id,
            hitbox=hitbox
        )

        self.cam_boxes.append(box)

        return new_id

    def remove_cam_box(self, id_: int) -> None:
        self.cam_boxes = [box for box in self.cam_boxes if box['id'] != id_]

    def save_to_file(self, filename: str) -> None:
        data = {
            'size': self.size,
            'g': self.g,
            'sprites': self.sprites,
            'hitboxes': self.hitboxes,
            'objects': self.objects,
            'animations': self.animations,
            'sounds': self.sounds,
            'scripts': self.scripts,
            'binds': self.binds,
            'cam_boxes': self.cam_boxes
        }

        with open(filename, 'w') as f:
            json.dump(data, f, indent=4, cls=GameEncoder)

    def load_from_file(self, filename: str) -> None:
        with open(filename, 'r') as f:
            data = json.load(f, object_hook=game_hook)

        self.size = data['size']
        self.g = data['g']
        self.sprites = data.get('sprites', [])
        self.hitboxes = data.get('hitboxes', [])
        self.objects = data.get('objects', [])
        self.cam_boxes = data.get('cam_boxes', [])
        self.animations = data.get('animations', [])
        self.sounds = data.get('sounds', [])
        self.scripts = data.get('scripts', [])
        self.binds = data.get('binds', [])

class Game:
    def __init__(self, screen : pygame.Surface, screen_size : tuple[int,int], clock : pygame.time.Clock, max_fps : float = 0):
        self.screen : pygame.Surface = screen
        self.screen_size : tuple[int,int] = screen_size
        self.max_fps : float = max_fps
        self.clock = clock

        self.camera : Camera | None = None
        self.player : Player | None = None

        self.layer_system : LayerSystem | None = None
        self.camera_manager : CameraManager | None = None
        self.activity_manager : ActivityManager | None = None
        self.physic_engine : PhysicEngine | None = None
        self.animation_engine : AnimationEngine | None = None
        self.sound_engine : SoundEngine | None = None
        self.input_manager : InputHandler | None = None
        self.script_system : ScriptingSystem | None = None

        self.objects : dict[int : Optional[StaticObject,MovingObject,Player]] = dict()
        self.layers : dict[int : Layer] = dict()
        self.scripts: dict[int : Script] = dict()
        self.binds : dict[int : Command] = dict()

        self.sprites : dict[int : tuple[pygame.Surface, HitboxParams]] = dict()

        self.sounds : dict[int : str] = dict()

        self.cam_boxes : dict[int, Hitbox] = dict()

        self.exit = False
        self.full_exit = False

    def load_level(self, level : Level):
        self.layer_system = LayerSystem(size = level.size, screen = self.screen)
        self.physic_engine = PhysicEngine(g = level.g)
        self.animation_engine = AnimationEngine()
        self.sound_engine = SoundEngine()
        self.script_system = ScriptingSystem()

        self._load_sprites(level)

        self._load_player_and_managers(level)

        self._load_objects(level)

        for layer_id in sorted(self.layers.keys()):
            self.layer_system.layers.append(self.layers[layer_id])

        self._load_cam_boxes(level)

        self._load_animations(level)

        self._load_sounds(level)

        self._load_scripts(level)

        self._load_binds(level)

    def _load_sprites(self, level : Level):
        for data in level.sprites:
            sprite = pygame.image.load(data['sprite_path'])
            sprite = pygame.transform.scale(sprite,data['sprite_size'])

            hb_params = level.hitboxes[data['hitbox_id']]['hitbox']

            self.sprites[data['id']] = (sprite, hb_params)

    def _load_player_and_managers(self, level : Level):
        player_data = level.objects[0]
        if not player_data:
            raise ValueError("Player data is missing in level configuration")
        print(player_data)
        self.player = self._object_from_data(class_type = 'Player', info_params = player_data["params"], need_hitbox= player_data['need_hitbox'])

        self.camera = Camera(target= self.player, screen_size = self.screen_size)

        self.camera_manager = CameraManager(camera = self.camera)

        self.activity_manager = ActivityManager(camera = self.camera)

        self.input_manager = InputHandler(camera = self.camera)

        self.objects[player_data['id']] = self.player
        if player_data['physics']:
            if player_data['physic_type'] == "Stoppable":
                self.physic_engine.add_stoppable_object(self.player)
            elif player_data['physic_type'] == 'Unstoppable':
                self.physic_engine.add_unstoppable_object(self.player)
            else:
                self.physic_engine.add_static_object(self.player)

        if player_data['layer']:
            if player_data['layer'] not in self.layers.keys():
                self.layers[player_data['layer']] = Layer()
            self.layers[player_data['layer']].objects.append(self.player)

        self.activity_manager.add_object(self.player)
        if player_data['force_active']:
            self.activity_manager.set_force_active(self.player)

    def _load_objects(self, level : Level):
        for data in level.objects[1:]:
            obj = self._object_from_data(class_type = data['class_type'], info_params= data['params'], need_hitbox = data['need_hitbox'])
            print(data)
            self.objects[data['id']] = obj
            if data['physics']:
                if data['physic_type'] == "Stoppable":
                    self.physic_engine.add_stoppable_object(obj)
                elif data['physic_type'] == 'Unstoppable':
                    self.physic_engine.add_unstoppable_object(obj)
                elif data['physic_type'] == 'Static':
                    self.physic_engine.add_static_object(obj)

            if data['layer'] or data['layer'] == 0:
                if not data['layer'] in self.layers.keys():
                    self.layers[data['layer']] = Layer()
                self.layers[data['layer']].objects.append(obj)

            self.activity_manager.add_object(obj)
            if data['force_active']:
                self.activity_manager.set_force_active(obj)

    def _load_cam_boxes(self,level : Level):
        for data in level.cam_boxes:
            hitbox = Hitbox.from_params(data['hitbox'])
            self.camera_manager.add_cam_box(hitbox)
            self.cam_boxes[data['id']] = hitbox

    def _load_animations(self, level: Level) -> None:
        for anim_data in level.animations:
            obj = self.objects[anim_data['object_id']]

            frames = [self._get_sprite(id_) for id_ in anim_data['frames']]

            if anim_data['change_hitboxes']:
                hitboxes = [self.sprites[id_][1] for id_ in anim_data['frames']]
                frames_list = [(frames[i],hitboxes[i]) for i in range(len(frames))]
            else:
                frames_list = [(item, None) for item in frames]


            self.animation_engine.add_anim(obj= obj, animation_name= anim_data['name'], anim_delay = anim_data['delay'], frames_list = frames_list)
            print(frames_list)

    def _load_sounds(self,level : Level):
        for data in level.sounds:
            if data['type'] == 'sound':
                self.sounds[data['id']] = data['filename']
            self.sound_engine.load_sound(data['filename'],data['filename'],data['volume'])

    def _load_scripts(self,level : Level):
        for data in level.scripts:
            script = self._script_from_data(data['info_params'])
            self.scripts[data['id']] = script
            self.script_system.add_script(script)

    def _load_binds(self,level : Level):
        for data in level.binds:
            script = self.scripts[data['command_script_id']]
            mouse = False
            if data['type'] == 'press':
                command = PressCommand(script)
            elif data['type'] == 'release':
                command = ReleaseCommand(script)
            elif data['type'] == 'hold':
                command = HoldCommand(script)
            elif data['type'] == 'mouse_press':
                command = PressCommand(script)
                mouse = True
            elif data['type'] == 'mouse_release':
                command = ReleaseCommand(script)
                mouse = True
            elif data['type'] == 'mouse_hold':
                command = HoldCommand(script)
                mouse = True
            else:
                raise ValueError('bind data wrong type')

            self.binds[data['id']] = command
            if mouse:
                self.input_manager.bind_mouse_button(button = data['key'],command= command, event_type = data['type'].replace('mouse_',''))
            else:
                self.input_manager.bind_key(key= data['key'], command = command, event_type = data['type'])

    def _object_from_data(self, class_type : str, need_hitbox : bool, info_params : Optional[StaticObjectInfoParams, MovingObjectInfoParams, PlayerObjectInfoParams]) -> Optional[StaticObject, MovingObject, Player]:
        if info_params.get('sprite_id') == 0 or info_params.get('sprite_id'):
            sprite = self._get_sprite(sprite_id= info_params['sprite_id'])
        else:
            sprite = None

        if need_hitbox:
            hitbox = self._get_hitbox(sprite_id = info_params['sprite_id'], obj_pos = info_params['pos'])
        else:
            hitbox = None

        if class_type == "Static":
            return StaticObject.from_params(
                StaticObjectParams(
                    pos = info_params['pos'],
                    sprite = sprite,
                    hitbox = hitbox,
                    size=sprite.get_size() if sprite else (0,0)
                )
            )
        elif class_type == "Moving":
            return MovingObject.from_params(
                MovingObjectParams(
                    pos=info_params['pos'],
                    sprite=sprite,
                    hitbox=hitbox,
                    size=sprite.get_size() if sprite else (0,0),

                    max_speed_x=info_params['max_speed_x'],
                    max_speed_y=info_params['max_speed_y'],
                    velocity_x=info_params['velocity_x'],
                    velocity_y=info_params['velocity_y'],
                    ground_friction_x=info_params['ground_friction_x'],
                    air_friction_x=info_params['air_friction_x'],
                    air_friction_y=info_params['air_friction_y'],
                    gravitate=info_params['gravitate']
                )
            )
        elif class_type == "Player":
            return Player.from_params(
                PlayerObjectParams(
                    pos=info_params['pos'],
                    sprite=sprite,
                    hitbox=hitbox,
                    size=sprite.get_size() if sprite else (0,0),

                    max_speed_x=info_params['max_speed_x'],
                    max_speed_y=info_params['max_speed_y'],
                    velocity_x=info_params['velocity_x'],
                    velocity_y=info_params['velocity_y'],
                    ground_friction_x=info_params['ground_friction_x'],
                    air_friction_x=info_params['air_friction_x'],
                    air_friction_y=info_params['air_friction_y'],
                    gravitate=info_params['gravitate'],

                    lives=info_params['lives']
                )
            )

    def _get_sprite(self, sprite_id : int) -> pygame.Surface:
        return self.sprites[sprite_id][0]

    def _get_hitbox(self, sprite_id : str, obj_pos : tuple[float,float]) -> Hitbox:
        hb_params = self.sprites[sprite_id][1]
        hb_pos = (obj_pos[0]+ hb_params['offset'][0], obj_pos[1]+hb_params['offset'][1])

        return Hitbox(pos = hb_pos, size = hb_params['size'])

    def _script_from_data(self, script_info : ScriptInfoParams) -> Script:
        script_params = ScriptParams(
            enabled = script_info.enabled,
            systems = {
                'layer_system': self.layer_system if script_info.systems['layer_system'] else None,
                'camera_manager': self.camera_manager if script_info.systems['camera_manager'] else None,
                'activity_manager': self.activity_manager if script_info.systems['activity_manager'] else None,
                'physic_engine': self.physic_engine if script_info.systems['physic_engine'] else None,
                'animation_engine': self.animation_engine if script_info.systems['animation_engine'] else None,
                'sound_engine': self.sound_engine if script_info.systems['sound_engine'] else None,
                'input_manager': self.input_manager if script_info.systems['input_manager'] else None,
                'script_system': self.script_system if script_info.systems['script_system'] else None
            },

            objects = [
                self.objects[id_] for id_ in script_info.objects
            ],

            scripts = [
                self.scripts[id_] for id_ in script_info.scripts
            ],
            camera = self.camera,
            clock = self.clock,
            other = script_info.other
        )
        return script_fabric_method(script_info.type, script_params)

    def game_loop(self):
        self.exit = False
        self.full_exit = False

        while not self.exit:
            fps = self.clock.get_fps()
            dt = 1 / fps if fps != 0 else 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True
                    self.full_exit = True
                self.input_manager.handle_event(event)

            self.activity_manager.update()

            self.input_manager.update(dt)

            self.script_system.update(dt)

            self.physic_engine.update(dt, self.activity_manager)

            self.animation_engine.update(dt, self.activity_manager)

            self.camera_manager.update()

            self.layer_system.update(self.activity_manager)

            self.layer_system.draw_by_camera(self.screen, self.camera)

            pygame.display.update()

            self.clock.tick_busy_loop(self.max_fps)
