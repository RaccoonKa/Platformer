import pygame

class Player(object):
    def __init__(self, sprite_name : str, speed_ : int, hitbox_size : tuple[int,int] = None) -> None:
        self.sprite = pygame.image.load(sprite_name)
        self.pos = [0,0]
        self.hitbox = None
        self.speed = speed_

    @property
    def sprite(self) -> pygame.sprite.Sprite:
        return self._sprite

    @sprite.setter
    def sprite(self, obj : pygame.sprite.Sprite) -> None:
        self._sprite = obj

    @property
    def pos(self) -> list[float,float]:
        return self._pos

    @pos.setter
    def pos(self, pos : list[float,float]):
        self._pos = pos

    @property
    def speed(self) -> int:
        return self._speed

    @speed.setter
    def speed(self, value : int) -> None:
        self._speed = value

    def draw(self, screen):
        screen.blit(self.sprite, self.pos)

    def update(self):
        ...