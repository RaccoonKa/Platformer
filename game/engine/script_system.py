from abc import ABC, abstractmethod
from typing import List, Optional

class Script(ABC):
    def __init__(self) -> None:
        self.enabled: bool = True

    @abstractmethod
    def start(self) -> None:
        pass

    @abstractmethod
    def stop(self) -> None:
        self.enabled = False

    @abstractmethod
    def update(self, dt: float) -> None:
        pass


class ScriptingSystem:
    def __init__(self):
        self.scripts: List[Script] = []  # Список всех активных скриптов

    def add_script(self, script: Script) -> None:
        if script not in self.scripts:
            self.scripts.append(script)
            script.start()

    def remove_script(self, script: Script) -> None:
        if script in self.scripts:
            self.scripts.remove(script)

    def update(self, dt: float) -> None:
        for script in self.scripts[:]:
            if script.enabled:
                script.update(dt)

    def clear(self) -> None:
        self.scripts.clear()

    def find_script(self, predicate) -> Optional[Script]:
        for script in self.scripts:
            if predicate(script):
                return script
        return None