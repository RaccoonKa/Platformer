import pygame
import os
from typing import Optional

from game.engine.control import InputHandler
from game.engine.objects import StaticObject, MovingObject
from game.engine.render import LayerSystem, Camera, ActivityManager
from game.engine.script_system import ScriptingSystem, Script
from game.subsystems.levels import Level

from game.engine.objects import StaticObjectInfoParams, MovingObjectInfoParams, PlayerObjectInfoParams
from game.subsystems.levels import SpriteData, ObjectData, BindData, ScriptData, AnimationData, HitboxData, SoundData, CamBoxData

class UI:
    def __init__(self):
        ...

    def update(self):
        ...

class Editor:
    def __init__(self,screen : pygame.Surface ,screen_size : tuple[int,int], max_fps : int, max_level_size : tuple[int,int], clock : pygame.time.Clock):
        self.screen_size = screen_size
        self.max_fps = max_fps
        self.screen = screen
        self.clock = clock

        self.editor_objects : list[tuple[StaticObject, ObjectData]] = []
        self.editor_scripts : list[Script] = list()

        self.cam_obj = MovingObject(pos=(0,0),speed_x= 1000,speed_y=1000)
        self.camera = Camera(target = self.cam_obj, screen_size= self.screen_size)

        self.layer_system = LayerSystem(size= max_level_size, screen = screen)
        self.input_manager = InputHandler(camera = self.camera)
        self.activity_manager = ActivityManager(camera = self.camera, activation_distance=2500)
        self.script_system = ScriptingSystem()
        self.ui = UI()

        self.hitboxes : list[HitboxData] = list()
        self.sprites : list[SpriteData] = list()
        self.objects : list[ObjectData] = list()
        self.cam_boxes : list[CamBoxData] = list()
        self.animations : list[AnimationData] = list()
        self.sounds : list[SoundData] = list()
        self.music : list[SoundData] = list()
        self.scripts : list[ScriptData] = list()
        self.binds : list[BindData] = list()

        self.exit = False
        self.full_exit = False

    def load_level(self, level : Level):
        self._load_hitboxes(level)

        self._load_sprites(level)

        self._load_objects(level)

        self._load_cam_boxes(level)

        self._load_animations(level)

        self._load_sounds(level)

        self._load_scripts(level)

        self._load_binds(level)

    def _load_hitboxes(self, level : Level):
        for data in level.hitboxes:
            self.hitboxes.append(data)

    def _load_sprites(self, level : Level):
        for data in level.scripts:
            self.sprites.append(data)

    def _load_objects(self, level : Level):
        for data in level.objects:
            self.objects.append(data)

    def _load_cam_boxes(self, level : Level):
        for data in level.cam_boxes:
            self.cam_boxes.append(data)

    def _load_animations(self, level : Level):
        for data in level.animations:
            self.animations.append(data)

    def _load_sounds(self, level : Level):
        for data in level.sounds:
            if data['type'] == 'sound':
                self.sounds.append(data)
            elif data['type'] == 'music':
                self.sounds.append(data)

    def _load_scripts(self, level : Level):
        for data in level.scripts:
            self.scripts.append(data)

    def _load_binds(self, level : Level):
        for data in level.binds:
            self.binds.append(data)

    #todo
    def _check_level(self)-> bool:
        return True

    #todo
    def save_level(self):
        if self._check_level():
            ...

    #todo
    def _start(self):
        # Скрипты, объекты, интерфейс
        pass

    def editor_loop(self):
        self._start()

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


            self.input_manager.update(dt)

            self.script_system.update(dt)

            self.layer_system.update(self.activity_manager)

            self.layer_system.draw_by_camera(self.screen, self.camera)

            self.ui.update()

            pygame.display.update()

            self.clock.tick_busy_loop(self.max_fps)

def main():
    screen_size = (1920,1080)
    max_fps = 60

    pygame.init()
    screen = pygame.display.set_mode(size = screen_size, vsync = max_fps)
    clock = pygame.time.Clock()

    pygame.display.set_caption("Level editor")

    icon = pygame.image.load("../assets/editor/icon.png")
    pygame.display.set_icon(icon)

    editor_size = (100000,10000)

    level_directory = "../saves/level1/level1.json"
    level = Level()
    level.load_from_file(level_directory)


    editor = Editor(
        screen_size= screen_size,
        max_fps= max_fps,
        screen= screen,
        max_level_size= editor_size,
        clock=clock
    )
    editor.load_level(level)

    editor.editor_loop()

if __name__ == "__main__":
    main()