from __future__ import annotations
import pygame
import json
import os
from typing import TypedDict, NotRequired, Optional

from game.engine.objects import GameObject, StaticObject, MovingObject, Player, Hitbox
from game.engine.render import Camera, CameraManager, Layer, LayerSystem, ActivityManager
from game.engine.physics import PhysicEngine
from game.engine.animation import AnimationEngine, AnimationContainer
from game.engine.control import InputHandler, Command
from game.engine.script_system import ScriptingSystem, Script
from game.engine.sound import SoundEngine

from game.subsystems.control_commands import MoveLeftCommand, MoveRightCommand, JumpCommand, MousePositionCommand, \
    ExampleMouseButtonCommand
from game.subsystems.scripts import MarioChaseScript, Patrol, LogScript

class HitboxParams(TypedDict):
    pos : tuple[float,float]
    size : tuple[float,float]

class ObjectParams(TypedDict):
    force_active : bool
    pos : tuple[float,float]
    sprite_path : str
    generate_hitbox : bool
    hitbox : NotRequired[HitboxParams]

    max_speed_x : NotRequired[float]
    max_speed_y : NotRequired[float]
    velocity_x : NotRequired[float]
    velocity_y : NotRequired[float]
    ground_friction_x : NotRequired[float]
    air_friction_x : NotRequired[float]
    air_friction_y : NotRequired[float]
    gravitate : NotRequired[bool]

    lives : NotRequired[int]


class ObjectData(TypedDict):
    id : int
    class_type : str
    physics : bool
    physic_type : NotRequired[str]
    layer : int
    params : ObjectParams


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

        self.objects : list[ObjectData] = list()
        self.animations : list[AnimationData] = list()
        self.sounds : list[SoundData] = list()
        self.scripts : list[ScriptData] = list()
        self.binds : list[BindData] = list()
        self.cam_boxes : list[CamBoxData] = list()

    def add_object(self, class_type : str, physics : bool, params : ObjectParams , layer : int = None, physics_type : str = None) -> int:
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
            physic_type = physics_type
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

    def _convert_positions(self, data: dict) -> None:
        if 'pos' in data:
            data['pos'] = tuple(data['pos'])
        if 'size' in data:
            data['size'] = tuple(data['size'])

class Game:
    def __init__(self):
        ...

    def load_level(self, level : Level):
        ...

    def game_loop(self):
        ...

