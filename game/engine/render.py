import pygame
from game.engine.objects import StaticObject, MovingObject

# Отвечает за камеру; как будто нужно сделать cum zone
class Camera:
    def __init__(self, target : MovingObject, screen_size : tuple[int,int], pos : tuple[int,int] = (0,0)):
        self.x = pos[0]
        self.y = pos[1]
        self.screen_size = screen_size
        self.target = target
        #self.main_surface = main_surface
        #self.screen = output_screen

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

class Layer:
    def __init__(self):
        self.objects : list[StaticObject] = []

    def update(self):
        ...

class MainSurface:
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

    def update(self):
        for layer in self.layers:
            #layer.update()
            for obj in layer.objects:
                self.main_surface.blit(obj.sprite,(obj.x,obj.y))

    def draw_by_camera(self,output_screen : pygame.surface.Surface, camera : Camera):
        output_screen.fill('black')
        output_screen.blit(self.main_surface,(-camera.x,-camera.y))