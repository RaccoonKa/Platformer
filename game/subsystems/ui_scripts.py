import pygame

from game.engine.control import InputHandler
from game.engine.script_system import Script, CommandScript

from game.engine.objects import StaticObject, Player, TextButton, Button


class LivesChecker(Script):
    def __init__(self, player : Player, normal_mode, screen_size : tuple[int,int], enabled : bool = False) -> None:
        super().__init__(None)

        self.player = player
        self.mode = normal_mode

        self.enabled = enabled

        self.hearts = list()

        self.heart_size = (int(38 * screen_size[0]/1920), int(34 * screen_size[1]/1080))

        self.current_lives = 0

    def destroy(self) -> None:
        self.kill = True

    def start(self) -> None:
        self.enabled = True

    def stop(self) -> None:
        self.enabled = False

    def update(self, dt: float) -> None:
        if self.current_lives == self.player.lives:
            return
        if self.player.lives < 0:
            return
        if self.current_lives < self.player.lives:
            self.add_heart()
        else:
            self.remove_heart()

    def remove_heart(self):
        self.mode.remove_decoration(self.hearts[-1])

        self.hearts.remove(self.hearts[-1])

        self.current_lives-=1

    def add_heart(self):
        heart = StaticObject(
            pos = (5 + len(self.hearts) * (self.heart_size[0]+2), 5),
            sprite = pygame.image.load("assets/pictures/game/things/heart.png")
        )
        heart.change_size(self.heart_size)
        self.mode.add_decorations(static_obj= heart)
        self.hearts.append(heart)

        self.current_lives+=1


class ButtonScript(CommandScript):
    def __init__(self, button : TextButton | Button, script : Script, input_handler : InputHandler, enabled : bool = False):
        super().__init__(None)
        self.enabled = enabled
        self.button = button
        self.script = script
        self.input_handler = input_handler

    def destroy(self) -> None:
        self.kill = True

    def start(self) -> None:
        self.enabled = True

    def stop(self) -> None:
        self.enabled = False

    def update(self, dt: float) -> None:
        pass

    def on_execute(self, dt : float, press : bool = False,hold : bool = False, release : bool = False) -> None:
        if not self.enabled:
            return
        if self.button.check_mouse(self.input_handler.get_mouse_position_on_screen()):
            if press:
                self.button.switch_sprite(press = True)
            if hold:
                if not self.button.pressed:
                    self.button.switch_sprite(press = True)
            if release:
                self.button.switch_sprite(press = False)
                if not self.script.enabled:
                    self.script.start()
                else:
                    self.script.stop()
        else:
            self.button.switch_sprite(press = False)


class ToggleButtonScript(CommandScript):
    def __init__(self, button: Button | TextButton, script: Script, input_handler: InputHandler, current_state: bool,
                 enabled: bool = False):
        super().__init__(None)
        self.enabled = enabled
        self.button = button
        self.script = script
        self.input_handler = input_handler
        self.state = current_state

        self.button.switch_sprite(press=self.state)

    def on_execute(self, dt: float, press: bool = False, hold: bool = False, release: bool = False) -> None:
        if not self.enabled:
            return

        mouse_pos = self.input_handler.get_mouse_position_on_screen()
        is_mouse_over = self.button.check_mouse(mouse_pos)

        if press and is_mouse_over:
            self.state = not self.state
            self.button.switch_sprite(press=self.state)

            if self.state:
                self.script.start()
            else:
                self.script.stop()

    def destroy(self) -> None:
        self.kill = True

    def start(self) -> None:
        self.enabled = True

    def stop(self) -> None:
        self.enabled = False

    def update(self, dt: float) -> None:
        pass


class ChangeMode(Script):
    def __init__(self, ui, mode_name : str, enabled: bool = False):
        super().__init__(None)
        self.enabled = enabled
        self.mode_name = mode_name
        self.ui = ui

    def destroy(self) -> None:
        self.kill = True

    def start(self) -> None:
        self.enabled = True

    def stop(self) -> None:
        self.enabled = False

    def update(self, dt: float) -> None:
        self.ui.switch_mode(name=self.mode_name)
        #print(f"switched to {self.mode_name}")
        self.stop()


class SwitchModeCommand(CommandScript):
    def __init__(self, ui, mode_name : str, enabled: bool = False):
        super().__init__(None)
        self.enabled = enabled
        self.mode_name = mode_name
        self.ui = ui
        self.from_mode = None

    def destroy(self) -> None:
        self.kill = True

    def start(self) -> None:
        self.enabled = True

    def stop(self) -> None:
        self.enabled = False

    def update(self, dt: float) -> None:
        pass

    def switch(self):
        if self.ui.current_mode.name == self.mode_name:
            self.ui.switch_mode(self.from_mode)
        else:
            self.from_mode = self.ui.current_mode.name
            self.ui.switch_mode(self.mode_name)

    def on_execute(self, dt : float, press : bool = False,hold : bool = False, release : bool = False) -> None:
        if press:
            self.switch()

        if release:
            self.switch()

        if hold:
            pass


class VolumeSwitcher(Script):
    def __init__(self, enabled : bool = False) -> None:
        super().__init__(None)
        self.enabled = enabled

    def destroy(self) -> None:
        self.kill = True

    def start(self) -> None:
        self.enabled = True

    def stop(self) -> None:
        self.enabled = False

    def update(self, dt: float) -> None:
        pass


class PrintScript(Script):
    def __init__(self, enabled : bool = False):
        super().__init__(None)
        self.enabled = enabled

    def destroy(self) -> None:
        self.kill = True

    def start(self) -> None:
        print("start")
        self.enabled = True

    def stop(self) -> None:
        print("stop")
        self.enabled = False

    def update(self, dt: float) -> None:
        print("example")
        self.stop()