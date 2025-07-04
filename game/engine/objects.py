from __future__ import annotations
import pygame
from dataclasses import dataclass
from typing import TypedDict, NotRequired


class HitboxParams(TypedDict):
    pos : tuple[float,float]
    size : tuple[int,int]


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

    def is_collide(self, other : Hitbox):
        if not other:
            return False
        return (self.x < other.x + other.size[0] and
                self.x + self.size[0] > other.x and
                self.y < other.y + other.size[1] and
                self.y + self.size[1] > other.y)

    @staticmethod
    def collide_detect(hb1: Hitbox, hb2: Hitbox) -> bool:
        if not hb1 or not hb2:
            return False

        return (hb1.x < hb2.x + hb2.size[0] and
                hb1.x + hb1.size[0] > hb2.x and
                hb1.y < hb2.y + hb2.size[1] and
                hb1.y + hb1.size[1] > hb2.y)
    @staticmethod
    def from_params(params : HitboxParams) -> Hitbox:
        return Hitbox(
            pos = params['pos'],
            size = params['size']
        )

    def change_size(self, to_size: tuple[int, int], obj: StaticObject) -> None:
        offset_x = self.x - obj.x
        offset_y = self.y - obj.y

        scale_x = to_size[0] / obj.size[0] if obj.size[0] != 0 else 1
        scale_y = to_size[1] / obj.size[1] if obj.size[1] != 0 else 1

        self.x = obj.x + offset_x * scale_x
        self.y = obj.y + offset_y * scale_y

        new_width = self.size[0] * scale_x
        new_height = self.size[1] * scale_y
        self.size = (int(new_width), int(new_height))

class GameObject:
    def __init__(self)-> None:
        self.is_active = True
        self.force_active = False

    def set_force_active(self, force_active: bool) -> None:
        self.force_active = force_active
        self.is_active = force_active or self.is_active

    def get_centre(self) -> tuple[float, float]:
        raise NotImplementedError


class StaticObjectParams(TypedDict):
    pos : tuple[float,float]
    sprite_path : NotRequired[str]
    generate_hitbox : NotRequired[bool]
    hitbox : NotRequired[HitboxParams]
    size : NotRequired[tuple[int,int]]


class StaticObject(GameObject):
    def __init__(self, pos : tuple[float,float], sprite : pygame.Surface = None, generate_hitbox : bool = False, size : tuple[int,int] = None, hitbox : Hitbox = None):
        super().__init__()
        self.x = pos[0]
        self.y = pos[1]

        if size:
            self.size = size
        if sprite:
            if size:
                self.sprite = pygame.transform.scale(sprite,self.size)
            else:
                self.sprite = sprite
                self.size = sprite.get_size()

        if generate_hitbox:
            self.hitbox = Hitbox.from_obj(self)
        elif hitbox:
            self.hitbox = hitbox
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
    def sprite(self, sprite : pygame.Surface) -> None:
        self._sprite = sprite

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

    def change_size(self, size : tuple[int,int]):
        if self.hitbox:
            self.hitbox.change_size(size,self)
        self.size = size
        if self.sprite:
            self.sprite = pygame.transform.scale(self.sprite,size)

    def change_sprite(self, sprite : pygame.Surface, change_size : bool = True):
        ...

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

    @staticmethod
    def from_params(params : StaticObjectParams, sprite : pygame.Surface | None = None) -> StaticObject:
        return StaticObject(
            pos = params['pos'],
            sprite = sprite,
            generate_hitbox = params['generate_hitbox'] if params.get('generate_hitbox') else False,
            hitbox = Hitbox.from_params(params['hitbox']) if params.get('hitbox') else None,
            size = params['size'] if params.get('size') else None
        )

class MovingObjectParams(StaticObjectParams):
    max_speed_x : float
    max_speed_y : float
    velocity_x : NotRequired[float]
    velocity_y : NotRequired[float]
    ground_friction_x : float
    air_friction_x : NotRequired[float]
    air_friction_y : NotRequired[float]
    gravitate : bool


class MovingObject(StaticObject):
    def __init__(self, pos : tuple[float, float], speed_x : float, speed_y : float, sprite : pygame.Surface = None, gravitation : bool = False, generate_hitbox : bool = False, hitbox : Hitbox = None, ground_friction_x : float = 0, air_friction_x : float = 0, air_friction_y : float = 0, velocity_x : float = 0, velocity_y : float = 0, size : tuple[int,int] = None):
        super().__init__(pos = pos,sprite= sprite, generate_hitbox= generate_hitbox, hitbox = hitbox, size = size)
        self.max_speed_x = speed_x
        self.max_speed_y = speed_y

        self.velocity_x = velocity_x
        self.velocity_y = velocity_y

        self.ground_friction_x = ground_friction_x
        self.air_friction_x = air_friction_x
        self.air_friction_y = air_friction_y

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
    def ground_friction_x(self) -> float:
        return self._ground_friction_x

    @ground_friction_x.setter
    def ground_friction_x(self, value: float) -> None:
        self._ground_friction_x = value

    @property
    def air_friction_x(self) -> float:
        return self._air_friction_x

    @air_friction_x.setter
    def air_friction_x(self, value: float) -> None:
        self._air_friction_x = value

    @property
    def air_friction_y(self) -> float:
        return self._air_friction_y

    @air_friction_y.setter
    def air_friction_y(self, value: float) -> None:
        self._air_friction_y = value

    @staticmethod
    def from_params(params : MovingObjectParams, sprite : pygame.Surface | None = None) -> MovingObject:
        return MovingObject(
            pos = params['pos'],
            sprite = sprite,
            generate_hitbox = params['generate_hitbox'] if params.get('generate_hitbox') else False,
            hitbox = Hitbox.from_params(params['hitbox']) if params.get('hitbox') else None,
            size = params['size'] if params.get('size') else None,

            speed_x = params['max_speed_x'],
            speed_y = params['max_speed_y'],

            velocity_x = params['velocity_x'] if params.get('velocity_x') else 0,
            velocity_y = params['velocity_y'] if params.get('velocity_y') else 0,

            ground_friction_x = params['ground_friction_x'] if params.get('ground_friction_x') else 0,
            air_friction_x = params['air_friction_x'] if params.get('air_friction_x') else 0,
            air_friction_y = params['air_friction_y'] if params.get('air_friction_y') else 0,

            gravitation = params['gravitate'] if params.get('gravitate') else False
        )

class PlayerObjectParams(MovingObjectParams):
    lives : int


class Player(MovingObject):
    def __init__(self, pos : tuple[float, float], speed_x : float, speed_y : float, ground_friction_x : float, air_friction_x : float, air_friction_y : float = 0, sprite : pygame.Surface = None, lives_count = 5, generate_hitbox : bool = False, hitbox : Hitbox = None, velocity_x : float = 0, velocity_y : float = 0, gravitation : bool = True, size : tuple[int,int] = None):
        super().__init__(pos = pos, speed_x= speed_x, speed_y= speed_y, sprite = sprite, gravitation = gravitation, generate_hitbox= generate_hitbox, hitbox = hitbox, ground_friction_x = ground_friction_x, air_friction_x = air_friction_x, air_friction_y = air_friction_y, velocity_x = velocity_x, velocity_y = velocity_y, size=size)

        self.lives = lives_count

    @property
    def lives(self) -> int:
        return self._lives

    @lives.setter
    def lives(self, value: int) -> None:
        self._lives = value

    @staticmethod
    def from_params(params : PlayerObjectParams, sprite : pygame.Surface | None = None) -> Player:
        return Player(
            pos=params['pos'],
            sprite=sprite,
            generate_hitbox=params['generate_hitbox'] if params.get('generate_hitbox') else False,
            hitbox=Hitbox.from_params(params['hitbox']) if params.get('hitbox') else None,
            size=params['size'] if params.get('size') else None,

            speed_x=params['max_speed_x'],
            speed_y=params['max_speed_y'],

            velocity_x=params['velocity_x'] if params.get('velocity_x') else 0,
            velocity_y=params['velocity_y'] if params.get('velocity_y') else 0,

            ground_friction_x=params['ground_friction_x'] if params.get('ground_friction_x') else 0,
            air_friction_x=params['air_friction_x'] if params.get('air_friction_x') else 0,
            air_friction_y=params['air_friction_y'] if params.get('air_friction_y') else 0,

            gravitation=params['gravitate'] if params.get('gravitate') else True,

            lives_count = params['lives']
        )

@dataclass
class ObjectsContainer:
    def __init__(self):
        self.static_objects : list[StaticObject] = []
        self.moving_objects : list[MovingObject] = []

#для params нужно сделать NotRequired, и чтобы создание учитывало это.