from __future__ import annotations

from game.engine.control import InputHandler
from game.engine.script_system import ScriptParams, Script, CommandScript
from game.editor.editor_objects import Button

class ButtonScript(CommandScript):
    def __init__(self, button : Button, script : Script, input_handler : InputHandler, enabled : bool = False):
        super().__init__(ScriptParams(enabled = enabled, systems=dict(),objects= list(),scripts=list()))
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

class PrintScript(Script):
    def __init__(self, enabled : bool = False):
        super().__init__(ScriptParams(enabled=enabled, systems=dict(), objects=list(), scripts=list()))

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

class ChangeMode(Script):
    def __init__(self, ui , mode_name : str, enabled: bool = False):
        super().__init__(ScriptParams(enabled=enabled, systems=dict(), objects=list(), scripts=list()))
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
        print(f"switched to {self.mode_name}")
        self.stop()
