import pygame
from dataclasses import dataclass


class StaticObject:
    def __init__(self, pos : tuple[float,float], sprite : pygame.Surface = None):
        self.x = pos[0]
        self.y = pos[1]
        self.size = (0, 0)
        self.sprite = sprite

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

    def load_sprite(self, sprite_filename : str):
        self.sprite = pygame.image.load(sprite_filename)
        self.size = self.sprite.get_size()

    def draw_on(self, screen : pygame.Surface) -> None:
        screen.blit(self.sprite,(self.x,self.y))

    def get_centre(self) -> tuple[float,float]:
        return self.size[0]/2+self.x, self.size[1]/2+self.y


class MovingObject(StaticObject):
    def __init__(self, pos : tuple[float, float], speed_x : float, speed_y : float, sprite : pygame.Surface = None):
        StaticObject.__init__(self,pos, sprite)
        self.max_speed_x = speed_x
        self.max_speed_y = speed_y
        self.velocity_x = 0
        self.velocity_y = 0

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


class Player(MovingObject):
    def __init__(self, pos : tuple[float, float], speed_x : float, speed_y : float, sprite : pygame.Surface = None, lives_count = 5):
        MovingObject.__init__(self,pos, speed_x, speed_y, sprite)
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