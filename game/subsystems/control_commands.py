from game.engine.control import Command
from game.engine.objects import Player, Hitbox
from game.engine.sound import SoundEngine


class MoveLeftCommand(Command):
    def __init__(self, player : Player) -> None:
        self.player = player

    def execute(self) -> None:
        if self.player.is_grounded:
            self.player.velocity_x = -self.player.max_speed_x
        else:
            self.player.velocity_x = max(
                self.player.velocity_x - 0.01 * self.player.max_speed_x,
                -self.player.max_speed_x
            )


class MoveRightCommand(Command):
    def __init__(self, player : Player) -> None:
        self.player = player

    def execute(self) -> None:
        if self.player.is_grounded:
            self.player.velocity_x = self.player.max_speed_x
        else:
            self.player.velocity_x = min(
                self.player.velocity_x + 0.01 * self.player.max_speed_x,
                self.player.max_speed_x
            )


class JumpCommand(Command):
    def __init__(self, player : Player, sound_engine : SoundEngine) -> None:
        self.player = player
        self.has_jumped = False
        self.sound_engine = sound_engine

    def execute(self) -> None:
        if self.player.is_grounded and not self.has_jumped:
            self.player.velocity_y = -self.player.max_speed_y

            self.sound_engine.play_sound('jump')
            self.has_jumped = True
        elif not self.player.is_grounded:
            self.has_jumped = False


class MousePositionCommand(Command):
    def __init__(self, handler) -> None:
        self.handler = handler

    def execute(self) -> None:
        print(f"Mouse position: {self.handler.get_mouse_position()}")

class MouseButtonCommand(Command):
    def __init__(self, handler, target : Hitbox) -> None:
        self.handler = handler
        self.target = target

    def execute(self) -> None:
        hb2 = Hitbox((self.handler.get_mouse_position()[0]+5,self.handler.get_mouse_position()[1]-5),(10,10))

        if Hitbox.collide_detect(self.target,hb2):
            print("Зачем кликнул, йоу?")
