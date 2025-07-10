import pygame

from game.subsystems.ui_scripts import ButtonScript, ToggleButtonScript
from game.engine.control import InputHandler
from game.engine.objects import StaticObject
from game.subsystems.control_commands import PressCommand, ReleaseCommand, HoldCommand
from game.engine.script_system import Script, ScriptingSystem

from game.engine.objects import Button, TextButton, TextObject, Text

class Mode:
    def __init__(self, name : str):
        self.name : str = name
        self.buttons : list[Button] = list()
        self.button_scripts : list[ButtonScript | ToggleButtonScript] = list()
        self.texts : list[TextObject] = list()
        self.decorations : list[StaticObject] = list()
        self.scripts : list[Script] = list()

    def add_button(self, pos : tuple[float,float], sprite_press : pygame.Surface, sprite_unpress : pygame.Surface, script : Script,  input_handler : InputHandler, name : Text = None,):
        if name:
            button = TextButton(pos= pos, unpressed_sprite = sprite_unpress, pressed_sprite= sprite_press, text = name)
        else:
            button = Button(pos= pos, unpressed_sprite = sprite_unpress, pressed_sprite= sprite_press)

        exec_script = ButtonScript(button= button, script= script, input_handler= input_handler, enabled = False)

        input_handler.bind_mouse_button(button=pygame.BUTTON_LEFT, event_type="press", command=PressCommand(exec_script))
        input_handler.bind_mouse_button(button=pygame.BUTTON_LEFT, event_type="hold", command=HoldCommand(exec_script))
        input_handler.bind_mouse_button(button=pygame.BUTTON_LEFT, event_type="release", command=ReleaseCommand(exec_script))


        self.buttons.append(button)
        self.button_scripts.append(exec_script)
        self.scripts.append(script)

    def add_text_obj(self, text_obj : TextObject):
        self.texts.append(text_obj)

    def remove_text_obj(self, text_obj : TextObject):
        self.texts.remove(text_obj)

    def add_decorations(self, static_obj : StaticObject):
        self.decorations.append(static_obj)

    def remove_decoration(self, static_obj : StaticObject):
        self.decorations.remove(static_obj)

    def turn_on(self) -> None:
        for button_script in self.button_scripts:
            button_script.start()
        for script in self.scripts:
            script.start()

    def turn_off(self) -> None:
        for button_script in self.button_scripts:
            button_script.stop()
        for script in self.scripts:
            script.stop()

    def draw(self, screen : pygame.Surface) -> None:
        for obj in self.decorations:
            obj.draw_on(screen= screen)

        for text_obj in self.texts:
            text_obj.draw_on(screen= screen)

        for button in self.buttons:
            button.draw_on(screen=screen)

    def update(self):
        pass

class UI:
    def __init__(self, input_handler : InputHandler):
        self.modes : list[Mode] = list()
        self.current_mode : Mode = Mode("null")
        self.input_handler : InputHandler = input_handler
        self.script_system : ScriptingSystem = ScriptingSystem()

    def add_mode(self, mode : Mode):
        self.modes.append(mode)

    def switch_mode(self, name : str):
        self.current_mode.turn_off()

        self.current_mode = self._find_mode_by_name(name = name)

        self.current_mode.turn_on()

    def _find_mode_by_name(self, name : str) -> Mode:
        for mode in self.modes:
            if mode.name == name:
                return mode
        raise ValueError("[UI] Mode with this name not found")

    def update(self, dt : float):
        self.script_system.update(dt)

        self.current_mode.update()

    def draw(self, screen : pygame.Surface):
        self.current_mode.draw(screen=screen)