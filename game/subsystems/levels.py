from __future__ import annotations
import pygame
import json
import os
from typing import TypedDict, NotRequired, Optional

from game.engine.objects import StaticObject, MovingObject, Player, Hitbox
from game.engine.objects import StaticObjectParams, MovingObjectParams, PlayerObjectParams, HitboxParams
from game.engine.render import Camera, CameraManager, Layer, LayerSystem, ActivityManager
from game.engine.physics import PhysicEngine
from game.engine.animation import AnimationEngine
from game.engine.control import InputHandler, Command
from game.engine.script_system import ScriptingSystem, Script
from game.engine.sound import SoundEngine

from game.subsystems.control_commands import MoveLeftCommand, MoveRightCommand, JumpCommand, MousePositionCommand, \
    ExampleMouseButtonCommand
from game.subsystems.scripts import MarioChaseScript, Patrol, LogScript


class ObjectData(TypedDict):
    id : int
    class_type : str
    physics : bool
    physic_type : NotRequired[str]
    layer : int
    params : Optional[StaticObjectParams, MovingObjectParams, PlayerObjectParams]
    force_active: bool


class AnimationData(TypedDict):
    object_id : int
    name : str
    delay : float
    frames : list[str] #list[sprite_path]


class SoundData(TypedDict):
    id : int
    type : str #music, sound
    filename : str
    volume : float


class ScriptData(TypedDict):
    id : int
    type : str
    params : dict


class BindData(TypedDict):
    id : int
    type : str
    params : dict


class CamBoxData(TypedDict):
    id : int
    hitbox : HitboxParams


class Level:
    def __init__(self, size : tuple[int,int] = (0,0), g : float = 9.8*16):
        self.size : tuple[int,int] = size
        self.g : float = g

        self.objects : list[ObjectData] = list() #list[ObjectData | None] = list()
        self.objects.append(None)

        self.cam_boxes: list[CamBoxData] = list()
        self.animations : list[AnimationData] = list()
        self.sounds : list[SoundData] = list()
        self.scripts : list[ScriptData] = list()
        self.binds : list[BindData] = list()

    def set_player(self, params : PlayerObjectParams, layer : int, physics : bool = True, physics_type : str = 'Stoppable', force_active : bool = True) -> int:
        data = ObjectData(
            id = 0,
            class_type = 'player',
            physics = physics,
            params = params,
            layer = layer,
            physic_type = physics_type,
            force_active = force_active
        )
        self.objects[0] = data

        return 0

    def remove_player(self) -> None:
        self.objects[0] = None

    def add_object(self, class_type : str, physics : bool, params : Optional[StaticObjectParams, MovingObjectParams], layer : int = None, physics_type : str = None, force_active : bool = False) -> int:
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
            force_active = force_active
        )

        self.objects.append(data)

        return new_id

    def remove_object(self, id_ : int) -> None:
        self.objects = [obj for obj in self.objects if obj['id'] != id_]

    def add_animation(self, object_id : int, name : str, delay : float, frames : list[str]):
        data = AnimationData(
            object_id = object_id,
            name = name,
            delay = delay,
            frames = frames
        )

        self.animations.append(data)

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

    def add_script(self, type_: str, params: dict) -> int:
        used_ids = {script['id'] for script in self.scripts}
        new_id = 0
        while new_id in used_ids:
            new_id += 1

        script = ScriptData(
            id = new_id,
            type=type_,
            params=params
        )

        self.scripts.append(script)

        return new_id

    def remove_script(self, id_: int) -> None:
        self.scripts = [script for script in self.scripts if script['id'] != id_]

    def add_binds(self, type_: str, params: dict) -> int:
        used_ids = {bind['id'] for bind in self.binds}
        new_id = 0
        while new_id in used_ids:
            new_id += 1

        bind = BindData(
            id=new_id,
            type=type_,
            params=params
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
            'size': list(self.size),
            'g': self.g,
            'objects': self.objects,
            'animations': self.animations,
            'sounds': self.sounds,
            'scripts': self.scripts,
            'binds': self.binds,
            'cam_boxes': self.cam_boxes
        }

        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    def load_from_file(self, filename: str) -> None:
        with open(filename, 'r') as f:
            data = json.load(f)

        self.size = tuple(data['size'])
        self.g = data['g']

        self.objects = []
        for obj in data.get('objects', []):
            params = obj['params']
            self._convert_positions(params)
            self.objects.append(obj)

        self.cam_boxes = []
        for box in data.get('cam_boxes', []):
            self._convert_positions(box['hitbox'])
            self.cam_boxes.append(box)

        self.animations = data.get('animations', [])
        self.sounds = data.get('sounds', [])
        self.scripts = data.get('scripts', [])
        self.binds = data.get('binds', [])

    @staticmethod
    def _convert_positions(data: dict) -> None:
        if 'pos' in data:
            data['pos'] = tuple(data['pos'])
        if 'size' in data:
            data['size'] = tuple(data['size'])

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

        self.sprites : dict[str : pygame.Surface, None : None] = dict()
        self.sprites[None] = None

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

        self._load_player_and_managers(level)

        self._load_objects(level)

        for layer_id in sorted(self.layers.keys()):
            self.layer_system.layers.append(self.layers[layer_id])

        self._load_cam_boxes(level)

        self._load_animations(level)

        self._load_sounds(level)

        self._load_scripts(level)

        self._load_binds(level)

    def _load_player_and_managers(self, level : Level):
        player_data = level.objects[0]
        if not player_data:
            raise ValueError("Player data is missing in level configuration")
        self.player = self._object_from_data(class_type = 'Player', params = player_data["params"])

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

        if not player_data['layer'] in self.layers.keys():
            self.layers[player_data['layer']] = Layer()
        self.layers[player_data['layer']].objects.append(self.player)

        self.activity_manager.add_object(self.player)
        if player_data['force_active']:
            self.activity_manager.set_force_active(self.player)

    def _load_objects(self, level : Level):
        for data in level.objects[1:]:
            obj = self._object_from_data(data['class_type'], data['params'])

            self.objects[data['id']] = obj
            if data['physics']:
                if data['physic_type'] == "Stoppable":
                    self.physic_engine.add_stoppable_object(obj)
                elif data['physic_type'] == 'Unstoppable':
                    self.physic_engine.add_unstoppable_object(obj)
                elif data['physic_type'] == 'Static':
                    self.physic_engine.add_static_object(obj)

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

    def _load_animations(self,level : Level):
        for data in level.animations:
            frames = list()

            for frame_path in data['frames']:
                frames.append(self._get_sprite(frame_path))

            self.animation_engine.add_anim(self.objects[data['object_id']],data['name'],data['delay'],frames)

    def _load_sounds(self,level : Level):
        for data in level.sounds:
            if data['type'] == 'sound':
                self.sounds[data['id']] = data['filename']
            self.sound_engine.load_sound(data['filename'],data['filename'],data['volume'])

    def _load_scripts(self,level : Level):
        ...

    def _load_binds(self,level : Level):
        ...

    def _object_from_data(self, class_type : str, params : Optional[StaticObjectParams, MovingObjectParams, PlayerObjectParams]) -> Optional[StaticObject, MovingObject, Player]:
        sprite = self._get_sprite(params['sprite_path'])
        if class_type == "Static":
            return StaticObject.from_params(params, sprite)
        elif class_type == "Moving":
            return MovingObject.from_params(params, sprite)
        elif class_type == "Player":
            return Player.from_params(params, sprite)

    def _get_sprite(self, sprite_path : str | None) -> pygame.Surface | None:
        if sprite_path not in self.sprites.keys():
            self.sprites[sprite_path] = pygame.image.load(sprite_path)

        return self.sprites[sprite_path]


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

# словари...