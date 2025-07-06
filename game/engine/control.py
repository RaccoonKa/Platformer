import pygame
from abc import ABC, abstractmethod
from game.engine.render import Camera
from typing import Dict, List, Tuple, Set


class Command(ABC):
    @abstractmethod
    def __init__(self):
        pass

    def execute(self, dt: float) -> None:
        pass


class InputHandler:
    def __init__(self, camera: Camera):
        self.key_bindings: List[Dict] = []
        self.mouse_bindings: List[Dict] = []

        self.key_states: Dict[int, bool] = {}
        self.mouse_states: Dict[int, bool] = {}
        self.mouse_position = (0, 0)
        self.camera = camera

        self.key_events: List[Tuple[str, int]] = []
        self.mouse_events: List[Tuple[str, int]] = []

        self.processed_events: Set[Tuple[str, int]] = set()

    def bind_key(self, key: int, command: Command, event_type: str = "hold") -> None:
        self.key_bindings.append({
            "key": key,
            "command": command,
            "type": event_type
        })

    def bind_mouse_button(self, button: int, command: Command, event_type: str = "hold") -> None:
        self.mouse_bindings.append({
            "button": button,
            "command": command,
            "type": event_type
        })

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEMOTION:
            self.mouse_position = event.pos

        elif event.type == pygame.KEYDOWN:
            self.key_states[event.key] = True
            self.key_events.append(("press", event.key))

        elif event.type == pygame.KEYUP:
            self.key_states[event.key] = False
            self.key_events.append(("release", event.key))

        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_states[event.button] = True
            self.mouse_events.append(("press", event.button))

        elif event.type == pygame.MOUSEBUTTONUP:
            self.mouse_states[event.button] = False
            self.mouse_events.append(("release", event.button))

    def update(self, dt: float) -> None:
        for event_type, key in self.key_events:
            event_id = (event_type, key)
            if event_id in self.processed_events:
                continue

            self.processed_events.add(event_id)

            for binding in self.key_bindings:
                if binding["key"] == key and binding["type"] == event_type:
                    binding["command"].execute(dt)

        for event_type, button in self.mouse_events:
            event_id = (event_type, button)
            if event_id in self.processed_events:
                continue

            self.processed_events.add(event_id)

            for binding in self.mouse_bindings:
                if binding["button"] == button and binding["type"] == event_type:
                    binding["command"].execute(dt)

        for binding in self.key_bindings:
            if binding["type"] == "hold" and self.key_states.get(binding["key"], False):
                binding["command"].execute(dt)

        for binding in self.mouse_bindings:
            if binding["type"] == "hold" and self.mouse_states.get(binding["button"], False):
                binding["command"].execute(dt)

        self.key_events.clear()
        self.mouse_events.clear()
        self.processed_events.clear()

    def get_mouse_position(self) -> Tuple[float, float]:
        return self.mouse_position[0] + self.camera.x, self.mouse_position[1] + self.camera.y

    def get_mouse_position_on_screen(self) -> Tuple[float,float]:
        return  self.mouse_position