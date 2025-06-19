from __future__ import annotations
import pygame
from game.engine.objects import StaticObject, MovingObject

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

    # с пивом покатит(нет)
    def check_collide(self, other : Hitbox) -> Hitbox | None:
        if self == other:
            return None
        if (self.x < other.x + other.size[0] and
                self.x + self.size[0] > other.x and
                self.y < other.y + other.size[1] and
                self.y + self.size[1] > other.y):
                return other
        return


class PhysicEngine:
    def __init__(self, fps : float, g : float = 9.8):
        self.static_objects : list[tuple[StaticObject,Hitbox]] = []
        self.moving_objects : list[tuple[MovingObject,Hitbox]] = []
        self.fps = fps
        self.g = g

    def add_static_object(self, obj : StaticObject, hitbox : Hitbox = None)-> None:
        if obj not in self.static_objects:
            if hitbox:
                self.static_objects.append((obj,hitbox))
            else:
                self.static_objects.append((obj,Hitbox.from_obj(obj)))

    def add_moving_object(self, obj : MovingObject, hitbox : Hitbox = None)-> None:
        if obj not in self.static_objects:
            if hitbox:
                self.moving_objects.append((obj,hitbox))
            else:
                self.moving_objects.append((obj,Hitbox.from_obj(obj)))

    def get_hitboxes(self) -> list[Hitbox]:
        return [h1[1] for h1 in self.static_objects] + [h1[1] for h1 in self.moving_objects]

    def update(self):
        #расчёт перемещений и коллизий
        for obj in self.moving_objects:
            if obj[0].is_gravitate:
                if self.fps != 0: obj[0].velocity_y += self.g/self.fps
                if abs(obj[0].velocity_y) > obj[0].max_speed_y:
                    obj[0].velocity_y = obj[0].max_speed_y

            obj[1].x = obj[0].x + obj[0].velocity_x
            obj[1].y = obj[0].y + obj[0].velocity_y
            collide_hitboxes = list()
            for other in self.get_hitboxes():
                col = obj[1].check_collide(other)
                if col:
                    collide_hitboxes.append(col)

            if collide_hitboxes: print("collide")
            if len(collide_hitboxes) == 0:
                obj[0].x += obj[0].velocity_x
                obj[0].y += obj[0].velocity_y

            else:
                obj[0].velocity_x *= -0.05
                obj[0].velocity_y *= -0.05

                obj[1].x = obj[0].x
                obj[1].y = obj[0].y
        #надо переделать