# levels.py
from __future__ import annotations
from typing import TypedDict, NotRequired
import pygame
import json
import os

from game.engine.objects import StaticObject, MovingObject, Player, Hitbox
from game.engine.render import Camera, CameraManager, Layer, LayerSystem, ActivityManager
from game.engine.physics import PhysicEngine
from game.engine.animation import AnimationEngine, AnimationContainer
from game.engine.control import InputHandler, Command
from game.engine.script_system import ScriptingSystem, Script
from game.engine.sound import SoundEngine

from game.subsystems.control_commands import MoveLeftCommand, MoveRightCommand, JumpCommand, MousePositionCommand, \
    ExampleMouseButtonCommand
from game.subsystems.scripts import MarioChaseScript, Patrol, LogScript


class Level:
    ...

class Game:
    ...