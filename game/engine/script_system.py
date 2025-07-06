from __future__ import annotations
from typing import List
from abc import ABC, abstractmethod
from typing import Optional, NotRequired, TypedDict
import pygame.time

from game.engine.objects import StaticObject, MovingObject, Player
from game.engine.render import Camera, CameraManager, LayerSystem, ActivityManager
from game.engine.physics import PhysicEngine
from game.engine.animation import AnimationEngine
from game.engine.control import InputHandler
from game.engine.sound import SoundEngine


class ScriptInfoParams:
    def __init__(self):
        self.type = 'Script'
        self.enabled : bool = False

        self.systems : dict[str, bool] = {
            'layer_system' : False,
            'camera_manager' : False,
            'activity_manager' : False,
            'physic_engine' : False,
            'animation_engine' : False,
            'sound_engine' : False,
            'input_manager' : False,
            'script_system' : False
        }
        self.objects : list[int] = list()
        self.scripts : list[int] = list()

        self.camera : bool = False
        self.clock : bool = False

        self.other : dict = dict()


class ScriptParams(TypedDict):
    enabled: NotRequired[bool]

    systems : dict[str, Optional[CameraManager, LayerSystem, ActivityManager, PhysicEngine, AnimationEngine, InputHandler, SoundEngine]]
    objects : list[Optional[StaticObject, MovingObject, Player]]
    scripts : list[Script]

    camera : NotRequired[Camera]
    clock : NotRequired[pygame.time.Clock]

    other : NotRequired[dict]


class Script(ABC):
    def __init__(self, params: ScriptParams) -> None:
        self.kill: bool = False
        self.enabled = params['enabled'] if params.get('enabled') else False

    @abstractmethod
    def destroy(self) -> None:
        self.kill = True

    @abstractmethod
    def start(self) -> None:
        self.enabled = True

    @abstractmethod
    def stop(self) -> None:
        self.enabled = False

    @abstractmethod
    def update(self, dt: float) -> None:
        pass


class CommandScript(Script):
    def __init__(self, params: ScriptParams) -> None:
        super().__init__(params)
        
    def destroy(self) -> None:
        self.kill = True

    def stop(self) -> None:
        self.enabled = False

    def start(self) -> None:
        self.enabled = True

    def update(self, dt: float) -> None:
        pass

    def on_execute(self, dt : float, press : bool = False,hold : bool = False, release : bool = False) -> None:
        pass


class ScriptingSystem:
    def __init__(self):
        self.scripts: List[Script] = []  # Список всех активных скриптов

    def add_script(self, script: Script) -> None:
        if script not in self.scripts:
            self.scripts.append(script)
            if script.enabled:
                script.start()

    def remove_script(self, script: Script) -> None:
        if script in self.scripts:
            self.scripts.remove(script)

    def update(self, dt: float) -> None:
        for script in self.scripts[:]:
            if script.kill:
                self.remove_script(script)
                continue
            if script.enabled:
                script.update(dt)

    def clear(self) -> None:
        self.scripts.clear()

    def find_script(self, predicate) -> Optional[Script]:
        for script in self.scripts:
            if predicate(script):
                return script
        return None

    def start_script(self, script: Script) -> None:
        if script in self.scripts:
            script.start()