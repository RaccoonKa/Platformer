from __future__ import annotations
import pygame
from dataclasses import dataclass

#Rectangle пока
class Hitbox:
    def __init__(self, pos : tuple[float, float], size : tuple[int, int]):
        self.x = pos[0]
        self.y = pos[1]
        self.size = size

    @staticmethod
    def from_obj(obj : StaticObject) -> Hitbox:
        return Hitbox((obj.x,obj.y),obj.size)

    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, value: float) -> None:
        self._x = value

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, value: float) -> None:
        self._y = value

class StaticObject:
    def __init__(self, pos : tuple[float,float], sprite : pygame.Surface = None, generate_hitbox : bool = False, hitbox : Hitbox = None):
        self.x = pos[0]
        self.y = pos[1]
        self.size = (0, 0)
        self.sprite = sprite
        if hitbox:
            self.hitbox = hitbox
        elif generate_hitbox:
            self.hitbox = Hitbox.from_obj(self)
        else:
            self.hitbox = None

    @property
    def x(self)->float:
        return self._x

    @x.setter
    def x(self, value : float)->None:
        self._x = value

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, value: float) -> None:
        self._y = value

    @property
    def sprite(self)-> pygame.Surface:
        return self._sprite

    @sprite.setter
    def sprite(self, sprite : pygame.Surface, change_size : bool = True) -> None:
        self._sprite = sprite
        if change_size and sprite:
            self.size = self.sprite.get_size()

    @property
    def size(self) -> tuple[int,int]:
        return self._size

    @size.setter
    def size(self, size : tuple[int,int]) -> None:
        self._size = size

    @property
    def hitbox(self) -> Hitbox:
        return self._hitbox

    @hitbox.setter
    def hitbox(self, hitbox : Hitbox) -> None:
        self._hitbox = hitbox

    def __int__(self) -> int:
        return int(self.x)

    def __lt__(self, other : StaticObject) -> bool:
        return self.x < other.x

    def get_pos(self) -> tuple[float,float]:
        return self.x, self.y

    def load_sprite(self, sprite_filename : str):
        self.sprite = pygame.image.load(sprite_filename)
        self.size = self.sprite.get_size()

    def draw_on(self, screen : pygame.Surface) -> None:
        screen.blit(self.sprite,(self.x,self.y))

    def get_centre(self) -> tuple[float,float]:
        return self.size[0]/2+self.x, self.size[1]/2+self.y

    def generate_hitbox(self):
        self.hitbox = Hitbox.from_obj(self)


class MovingObject(StaticObject):
    def __init__(self, pos : tuple[float, float], speed_x : float, speed_y : float, sprite : pygame.Surface = None, gravitation : bool = False, generate_hitbox : bool = False, hitbox : Hitbox = None, friction_x : float = 0, friction_y : float = 0):
        StaticObject.__init__(self, pos = pos,sprite= sprite, generate_hitbox= generate_hitbox, hitbox = hitbox)
        self.max_speed_x = speed_x
        self.max_speed_y = speed_y
        self.velocity_x = 0
        self.velocity_y = 0
        self.friction_x = friction_x
        self.friction_y = friction_y
        self.is_gravitate = gravitation
        self.is_grounded = False

    @property
    def max_speed_x(self) -> float:
        return self._max_speed_x

    @max_speed_x.setter
    def max_speed_x(self, value: float) -> None:
        self._max_speed_x = value

    @property
    def max_speed_y(self) -> float:
        return self._max_speed_y

    @max_speed_y.setter
    def max_speed_y(self, value: float) -> None:
        self._max_speed_y = value

    @property
    def velocity_x(self) -> float:
        return self._velocity_x

    @velocity_x.setter
    def velocity_x(self, value: float) -> None:
        self._velocity_x = value

    @property
    def velocity_y(self) -> float:
        return self._velocity_y

    @velocity_y.setter
    def velocity_y(self, value: float) -> None:
        self._velocity_y = value

    @property
    def friction_x(self) -> float:
        return self._friction_x

    @friction_x.setter
    def friction_x(self, value: float) -> None:
        self._friction_x = value

    @property
    def friction_y(self) -> float:
        return self._friction_y

    @friction_y.setter
    def friction_y(self, value: float) -> None:
        self._friction_y = value


class Player(MovingObject):
    def __init__(self, pos : tuple[float, float], speed_x : float, speed_y : float, friction_x : float, sprite : pygame.Surface = None, lives_count = 5, generate_hitbox : bool = False, hitbox : Hitbox = None):
        MovingObject.__init__(self, pos = pos, speed_x= speed_x, speed_y= speed_y, sprite = sprite, gravitation = True, generate_hitbox= generate_hitbox, hitbox = hitbox, friction_x = friction_x)
        self.lives = lives_count

    @property
    def lives(self) -> int:
        return self._lives

    @lives.setter
    def lives(self, value: int) -> None:
        self._lives = value

@dataclass
class ObjectsContainer:
    def __init__(self):
        self.static_objects : list[StaticObject] = []
        self.moving_objects : list[MovingObject] = []