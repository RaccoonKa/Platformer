from __future__ import annotations
from game.engine.script_system import ScriptParams, Script, CommandScript

class ButtonScript(CommandScript):
    def __init__(self, params : ScriptParams):
        super().__init__(params)

    def destroy(self) -> None:
        ...

    def stop(self) -> None:
        ...

    def update(self, dt: float) -> None:
        ...

    def on_execute(self, dt : float, press : bool = False,hold : bool = False, release : bool = False) -> None:
        ...