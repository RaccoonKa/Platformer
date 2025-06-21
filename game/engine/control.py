import pygame
from abc import ABC, abstractmethod
from game.engine.render import Camera

class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass


class InputHandler:
    def __init__(self, camera : Camera):
        self.key_bindings = {}
        self.mouse_bindings = {}
        self.key_states = {}
        self.mouse_states = {}
        self.mouse_position = (0, 0)
        self.camera = camera

    def bind_key(self, key: int, command: Command) -> None:
        self.key_bindings[key] = command

    def bind_mouse_button(self, button: int, command: Command) -> None:
        self.mouse_bindings[button] = command

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEMOTION:
            self.mouse_position = event.pos

        if event.type == pygame.KEYDOWN:
            self.key_states[event.key] = True
        elif event.type == pygame.KEYUP:
            self.key_states[event.key] = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_states[event.button] = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.mouse_states[event.button] = False

    def update(self) -> None:
        for key, command in self.key_bindings.items():
            if self.key_states.get(key, False):
                command.execute()

        for button, command in self.mouse_bindings.items():
            if self.mouse_states.get(button, False):
                command.execute()

    def get_mouse_position(self) -> tuple[float,float]:
        return self.mouse_position[0]+self.camera.x, self.mouse_position[1] + self.camera.y
