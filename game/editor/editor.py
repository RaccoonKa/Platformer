import pygame
import os
from typing import Optional

from game.engine.control import InputHandler
from game.engine.objects import StaticObject, MovingObject
from game.engine.render import LayerSystem, Layer, Camera, ActivityManager
from game.engine.script_system import ScriptingSystem, Script
from game.subsystems.levels import Level

from game.engine.objects import StaticObjectInfoParams, MovingObjectInfoParams, PlayerObjectInfoParams
from game.subsystems.levels import SpriteData, ObjectData, BindData, ScriptData, AnimationData, HitboxData, SoundData, CamBoxData

from game.editor.ui import UI, Mode
from game.editor.editor_objects import Button, TextObject, Text
from game.editor.editor_scripts import ButtonScript, PrintScript, ChangeMode


class Editor:
    def __init__(self,screen : pygame.Surface ,screen_size : tuple[int,int], max_fps : int, max_level_size : tuple[int,int], clock : pygame.time.Clock):
        self.screen_size = screen_size
        self.max_fps = max_fps
        self.screen = screen
        self.clock = clock

        self.max_level_size = max_level_size

        self.editor_objects : list[tuple[StaticObject, ObjectData]] = []
        self.editor_scripts : list[Script] = list()

        self.cam_obj = MovingObject(pos=(0,0),speed_x= 1000,speed_y=1000)
        self.camera = Camera(target = self.cam_obj, screen_size= self.screen_size)

        self.layer_system = LayerSystem(size= max_level_size, screen = screen)
        self.input_manager = InputHandler(camera = self.camera)
        self.activity_manager = ActivityManager(camera = self.camera, activation_distance=2500)
        self.script_system = ScriptingSystem()
        self.ui = UI(input_handler = self.input_manager)

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
        ...

    #todo
    def save_level(self):
        if self._check_level():
            ...

    #todo
    def _start(self):
        layer0 = Layer()

        #фон
        back = StaticObject(pos=(0,0))
        sprite = pygame.Surface(size=self.max_level_size)
        sprite.fill(color=(45, 40, 50))
        back.sprite = sprite
        back.size = self.max_level_size

        self.activity_manager.add_object(back)
        layer0.objects.append(back)
        self.layer_system.layers.append(layer0)



        # Скрипты, объекты, интерфейс
        self._generate_ui()

        pass

    def _generate_ui(self):
        font30 = pygame.font.Font(None,30)
        font50 = pygame.font.Font(None,50)


        directory = "../assets/editor/"

        test_script = PrintScript(False)
        self.script_system.add_script(test_script)

        change_sprite_mode = ChangeMode(self.ui, "sprite_change")
        self.script_system.add_script(change_sprite_mode)

        to_base_script = ChangeMode(self.ui, "base")
        self.script_system.add_script(to_base_script)

        # Добавление спрайта(с указанием хитбокса для него) в хранилище
        # Добавление объектов
        # Добавление анимаций (для объекта по указанным спрайтам) в хранилище
        # Добавление звуков в хранилище
        # Добавление скриптов с разметкой
        # Добавление биндов

        # base
        #

        base_mode = Mode("base")

        button0 = (pygame.image.load(directory + "button/button0press.png"),pygame.image.load(directory + "button/button0unpress.png"))
        button1 = (pygame.image.load(directory + "button/button1press.png"),pygame.image.load(directory + "button/button1unpress.png"))
        button2 = (pygame.image.load(directory + "button/button2press.png"),pygame.image.load(directory + "button/button2unpress.png"))

        left_bar = StaticObject(pos = (0,0),sprite=pygame.image.load(directory + "decor/left_bar.png"))
        base_mode.add_decorations(left_bar)

        base_mode.add_button(
            name= Text(
                text = "Save",
                font = font30
            ),
            pos = (0,0),
            sprite_press= button1[0],
            sprite_unpress=button1[1],
            script= test_script, #todo
            input_handler = self.input_manager
                             )

        base_mode.add_button(
            name=Text(
                text="Load",
                font=font30
            ),
            pos=(75, 0),
            sprite_press=button1[0],
            sprite_unpress=button1[1],
            script=test_script, #todo
            input_handler=self.input_manager
        )

        base_mode.add_button(
            name=Text(
                text="Sprite",
                font=font30
            ),
            pos=(0, 50),
            sprite_press=button0[0],
            sprite_unpress=button0[1],
            script = change_sprite_mode,
            input_handler=self.input_manager
        )

        base_mode.add_button(
            name=Text(
                text="Object",
                font=font30
            ),
            pos=(0, 100),
            sprite_press=button0[0],
            sprite_unpress=button0[1],
            script=test_script, #todo
            input_handler=self.input_manager
        )

        base_mode.add_button(
            name=Text(
                text="Animation",
                font=font30
            ),
            pos=(0, 150),
            sprite_press=button0[0],
            sprite_unpress=button0[1],
            script=test_script, #todo
            input_handler=self.input_manager
        )

        base_mode.add_button(
            name=Text(
                text="Sound",
                font=font30
            ),
            pos=(0, 200),
            sprite_press=button0[0],
            sprite_unpress=button0[1],
            script=test_script, #todo
            input_handler=self.input_manager
        )

        base_mode.add_button(
            name=Text(
                text="Script",
                font=font30
            ),
            pos=(0, 250),
            sprite_press=button0[0],
            sprite_unpress=button0[1],
            script=test_script, #todo
            input_handler=self.input_manager
        )

        base_mode.add_button(
            name=Text(
                text="Bind",
                font=font30
            ),
            pos=(0, 300),
            sprite_press=button0[0],
            sprite_unpress=button0[1],
            script=test_script, #todo
            input_handler=self.input_manager
        )

        base_mode.add_button(
            name=Text(
                text="To base",
                font=font30
            ),
            pos=(0, 1030),
            sprite_press=button0[0],
            sprite_unpress=button0[1],
            script=to_base_script,
            input_handler=self.input_manager
        )

        self.ui.add_mode(base_mode)
        self.ui.switch_mode("base")

        # sprite_change
        #

        sprites_mode = Mode("sprite_change")

        sprites_mode.add_button(
            name=Text(
                text="To base",
                font=font30
            ),
            pos=(0, 1030),
            sprite_press=button0[0],
            sprite_unpress=button0[1],
            script=to_base_script,
            input_handler=self.input_manager
        )

        sprites_mode.add_decorations(StaticObject(pos = (360,90),sprite=pygame.image.load(directory + "/decor/sprite_change/spritebar.png")))
        sprites_mode.add_decorations(StaticObject(pos = (660, 90), sprite=pygame.image.load(directory + "/decor/sprite_change/spritebox.png")))
        sprites_mode.add_text_obj(TextObject(pos = (360+3,90+1),text = Text("see size",font= font50),sprite = None))

        sprites_mode.add_button(
            name=Text(
                text="+",
                font=font50
            ),
            pos=(360+50, 90+30),
            sprite_press=button2[0],
            sprite_unpress=button2[1],
            script=test_script,#todo
            input_handler=self.input_manager
        )

        sprites_mode.add_button(
            name=Text(
                text="-",
                font=font50
            ),
            pos=(360+50+50+10, 90+30),
            sprite_press=button2[0],
            sprite_unpress=button2[1],
            script=test_script,  # todo
            input_handler=self.input_manager
        )

        self.ui.add_mode(sprites_mode)


    def editor_loop(self):
        self._start()

        self.exit = False
        self.full_exit = False

        #tmp
        delay = 0
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

            self.ui.draw(screen=self.screen)

            pygame.display.update()

            self.clock.tick_busy_loop(self.max_fps)

            delay += dt
            if delay > 5:
                delay = 0
                print(f"fps: {self.clock.get_fps()}")


def main():
    screen_size = (1920,1080)
    max_fps = 0

    pygame.init()
    screen = pygame.display.set_mode(size = screen_size, vsync = max_fps)
    clock = pygame.time.Clock()

    pygame.display.set_caption("Level editor")

    icon = pygame.image.load("../assets/editor/icon.png")
    pygame.display.set_icon(icon)

    editor_size = (35000,2000)

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