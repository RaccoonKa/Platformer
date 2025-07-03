from game.engine.control import Command
from game.engine.script_system import CommandScript


class PressCommand(Command):
    def __init__(self, script : CommandScript):
        self.script = script

    def execute(self, dt: float) -> None:
        #print('press')
        self.script.on_execute(press = True, dt = dt)

class HoldCommand(Command):
    def __init__(self, script : CommandScript):
        self.script = script

    def execute(self, dt: float) -> None:
        #print('hold')
        self.script.on_execute(hold = True, dt = dt)

class ReleaseCommand(Command):
    def __init__(self, script : CommandScript):
        self.script = script

    def execute(self, dt: float) -> None:
        #print('release')
        self.script.on_execute(release = True, dt = dt)