from game.engine.control import Command
from game.engine.script_system import CommandScript


class PressCommand(Command):
    def __init__(self, script : CommandScript):
        self.script = script

    def execute(self, dt: float) -> None:
        self.script.on_execute(press = True, dt = dt)

class HoldCommand(Command):
    def __init__(self, script : CommandScript):
        self.script = script

    def execute(self, dt: float) -> None:
        self.script.on_execute(hold = True, dt = dt)

class ReleaseCommand(Command):
    def __init__(self, script : CommandScript):
        self.script = script

    def execute(self, dt: float) -> None:
        self.script.on_execute(release = True, dt = dt)

# class MoveLeftCommand(Command):
#     def __init__(self, player: Player, ground_acceleration: float, air_acceleration, max_speed: float) -> None:
#         self.player = player
#         self.ground_acceleration = ground_acceleration
#         self.air_acceleration = air_acceleration
#         self.max_speed = min(player.max_speed_x, max_speed)
#
#     def execute(self, dt: float) -> None:
#         if self.player.is_grounded:
#             self.player.velocity_x = max(-self.max_speed, self.player.velocity_x - dt * self.ground_acceleration)
#         else:
#             self.player.velocity_x = max(-self.max_speed, self.player.velocity_x - dt * self.air_acceleration)


# class MoveRightCommand(Command):
#     def __init__(self, player : Player, ground_acceleration : float, air_acceleration, max_speed : float) -> None:
#         self.player = player
#         self.ground_acceleration = ground_acceleration
#         self.air_acceleration = air_acceleration
#         self.max_speed = min(player.max_speed_x,max_speed)
#
#     def execute(self, dt : float) -> None:
#         if self.player.is_grounded:
#             self.player.velocity_x = min(self.max_speed, self.player.velocity_x + dt*self.ground_acceleration)
#         else:
#             self.player.velocity_x = min(self.max_speed, self.player.velocity_x + dt*self.air_acceleration)
#
#
# class JumpCommand(Command):
#     def __init__(self, player : Player, sound_engine : SoundEngine, jump_speed : float) -> None:
#         self.player = player
#         self.has_jumped = False
#         self.sound_engine = sound_engine
#         self.jump_speed = jump_speed
#
#     def execute(self, dt : float) -> None:
#         if self.player.is_grounded and not self.has_jumped:
#             self.player.velocity_y = - min(self.player.max_speed_y, self.jump_speed)
#
#             self.sound_engine.play_sound('jump')
#             self.has_jumped = True
#         elif not self.player.is_grounded:
#             self.has_jumped = False
#
#
# class MousePositionCommand(Command):
#     def __init__(self, handler) -> None:
#         self.handler = handler
#
#     def execute(self, dt : float) -> None:
#         print(f"Mouse position: {self.handler.get_mouse_position()}")
#
# class ExampleMouseButtonCommand(Command):
#     def __init__(self, handler, target : Hitbox) -> None:
#         self.handler = handler
#         self.target = target
#
#     def execute(self, dt : float) -> None:
#         hb2 = Hitbox((self.handler.get_mouse_position()[0]+5,self.handler.get_mouse_position()[1]-5),(10,10))
#
#         if Hitbox.collide_detect(self.target,hb2):
#             print("Зачем кликнул, йоу?")

# class BoolSwitchCommand(Command):
#     def __init__(self, target : bool):
#         self.target = target
#
#     def execute(self, dt : float) -> None:
#         self.target = not self.target