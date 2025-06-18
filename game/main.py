import pygame
import sys

from objects import StaticObject, MovingObject, Player


#Eсли будет не впадлу
class Keyboard:
    ...


class PhysicEngine:
    def __init__(self):
        ...

    def update(self):
        ...


class AnimationEngine:
    def __init__(self):
        ...

    def update(self):
        ...


class SoundEngine:
    def __init__(self):
        ...

    def update(self):
        ...


class Surface:
    def __init__(self):
        ...

    def update(self):
        ...


class MainSurface:
    def __init__(self):
        self.tmp = None

    def update(self):
        ...

    def get_surface(self) -> pygame.Surface:
        return self.tmp

class Camera:
    def __init__(self, target : MovingObject, output_screen : pygame.Surface, screen_size : tuple[int,int], main_surface : MainSurface, pos : tuple[int,int] = (0,0)):
        self.x = pos[0]
        self.y = pos[1]
        self.screen_size = screen_size
        self.target = target
        self.main_surface = main_surface
        self.screen = output_screen

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

    def draw(self):
        self.screen.fill('black')
        self.screen.blit(self.main_surface.get_surface(),(-self.x,-self.y))

def main() -> None:
    screen_size = (1920,1080)
    fps = 60

    #Базовые настройки
    pygame.init()
    screen = pygame.display.set_mode(size = screen_size, vsync = fps) #Разрешение
    pygame.display.set_caption("Окно так называется, йоу") #Название окна

    icon = pygame.image.load("assets/icon.png")
    pygame.display.set_icon(icon)

    clock = pygame.time.Clock()
    # флаги
    full_exit = False

    #tmp
    tmp = MainSurface()
    tmp.tmp = pygame.Surface((5000,1080))
    tmp.tmp.fill('gray')



    #Загрузка базовых объектов
    player = Player((0,0),10,10,pygame.image.load("assets/character/char0.png"))
    camera = Camera(player,screen,screen_size,tmp)

    #Основной цикл
    while not full_exit:
        # Обработка клавиатуры

        #tmp
        keys = pygame.key.get_pressed()
        if keys[pygame.K_s]:
            player.y += player.max_speed_y
        if keys[pygame.K_w]:
            player.y -= player.max_speed_y
        if keys[pygame.K_a]:
            player.x -= player.max_speed_x
        if keys[pygame.K_d]:
            player.x += player.max_speed_x

        # какие-то взаимодействия с чем-то

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                full_exit = True

        # Работа физики

        # Работа движка анимаций

        # Работа наложения поверхностей
        tmp.tmp.fill('gray')
        player.draw_on(tmp.tmp)

        # Работа камеры
        camera.update()
        camera.draw()
        #screen.blit(tmp.tmp,(0, 0))


        pygame.display.update()

        clock.tick(fps)

    if full_exit:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()