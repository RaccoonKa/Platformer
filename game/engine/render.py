import pygame
from typing import List, Set
from game.engine.objects import GameObject, StaticObject, MovingObject

# Отвечает за камеру; как будто нужно сделать cum zone
class Camera:
    def __init__(self, target : MovingObject, screen_size : tuple[int,int], pos : tuple[int,int] = (0,0)):
        self.x = pos[0]
        self.y = pos[1]
        self.screen_size = screen_size
        self.target = target

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

    def update(self) -> None:
        centre = self.target.get_centre()

        self.x = centre[0] - self.screen_size[0]/2
        self.y = centre[1] - self.screen_size[1]/2

class ActivityManager:
    def __init__(self, camera: Camera, activation_distance: float = 2000) -> None:
        self.camera = camera
        self.activation_distance = activation_distance
        self.objects: List[GameObject] = []
        self.force_active_objects: Set[GameObject] = set()
        self.active_objects: Set[GameObject] = set()

    def add_object(self, obj: GameObject) -> None:
        if obj not in self.objects:
            self.objects.append(obj)
            self.active_objects.add(obj)

    def remove_object(self, obj: GameObject) -> None:
        if obj in self.objects:
            self.objects.remove(obj)
        if obj in self.active_objects:
            self.active_objects.remove(obj)
        if obj in self.force_active_objects:
            self.force_active_objects.remove(obj)

    def set_force_active(self, obj: GameObject, force_active: bool = True) -> None:
        if force_active:
            self.force_active_objects.add(obj)
            self.active_objects.add(obj)
        elif obj in self.force_active_objects:
            self.force_active_objects.remove(obj)

    def update(self) -> None:
        cam_x = self.camera.x + self.camera.screen_size[0] / 2
        cam_y = self.camera.y + self.camera.screen_size[1] / 2

        for obj in self.objects:
            if obj in self.force_active_objects:
                continue

            obj_center = obj.get_centre()
            if obj_center[0] - cam_x < self.activation_distance and obj_center[1] - cam_y < self.activation_distance:
                self.active_objects.add(obj)
            elif obj in self.active_objects:
                self.active_objects.remove(obj)

            #distance = ((obj_center[0] - cam_x) ** 2 +
            #            (obj_center[1] - cam_y) ** 2) ** 0.5
            #if distance <= self.activation_distance:
            #   self.active_objects.add(obj)...

    def get_active_objects(self) -> Set[GameObject]:
        return self.active_objects

class Layer:
    def __init__(self):
        self.objects : list[StaticObject] = []

class LayerSystem:
    def __init__(self, size : tuple[int, int], screen : pygame.Surface):
        self.size = size
        self.layers : list[Layer] = []

        self.screen = screen
        self.main_surface = pygame.Surface(size)

    @property
    def size(self) -> tuple[int,int]:
        return self._size

    @size.setter
    def size(self, size : tuple[int,int]) -> None:
        self._size = size

    def update(self, activity_manager: ActivityManager) -> None:
        active_objects = activity_manager.get_active_objects()

        for layer in self.layers:
            for obj in layer.objects:
                if obj not in active_objects:
                    continue
                self.main_surface.blit(obj.sprite,(obj.x,obj.y))

    def draw_by_camera(self,output_screen : pygame.surface.Surface, camera : Camera):
        output_screen.fill('black')
        output_screen.blit(self.main_surface,(-camera.x,-camera.y))

