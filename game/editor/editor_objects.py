import pygame
from game.engine.objects import StaticObject

class Text:
    def __init__(self, text : str, font : pygame.font.Font, color : tuple[int,int,int] =(0,0,0), antialias : bool = True, bg_color : tuple[int,int,int] = None):
        self.text = text
        self.font = font
        self.color = color
        self.background_color = bg_color
        self.antialias = antialias
        self.bg_color = bg_color

        self.surface = self.font.render(self.text, self.antialias, self.color, self.background_color)

    def switch(self, text : str = None, font : pygame.font.Font = None, color : tuple[int,int,int] =(0,0,0), antialias : bool = True, bg_color : tuple[int,int,int] | int = -1):
        if text:
            self.text = text
        if font:
            self.font = font
        if color:
            self.color = color
        if antialias:
            self.antialias = antialias
        if not isinstance(bg_color, int):
            self.bg_color = bg_color

        self.surface = self.font.render(self.text, self.antialias, self.color)

    def draw_on(self, pos : tuple[float,float], screen : pygame.Surface)-> None:
        screen.blit(self.surface, pos)

class TextObject(StaticObject):
    def __init__(self, pos: tuple[float, float], text : Text, sprite: pygame.Surface = None, generate_hitbox : bool = False, centre_text : bool = False):
        super().__init__(pos=pos, sprite=sprite, generate_hitbox = generate_hitbox)
        self.text = text
        self.text_offset = (0,0)

        if centre_text:
            self._centre_text()

    def _centre_text(self):
        #todo
        ...

    def draw_on(self, screen : pygame.Surface) -> None:
        if self.sprite:
            screen.blit(self.sprite, (self.x, self.y))
        self.text.draw_on(pos= (self.x + self.text_offset[0], self.y + self.text_offset[1]), screen= screen)


class Button(TextObject):
    def __init__(self, pos : tuple[float,float],text : Text, unpressed_sprite : pygame.Surface, pressed_sprite : pygame.Surface):
        super().__init__(pos = pos, sprite=unpressed_sprite, generate_hitbox= True, text = text)
        self.pressed_sprite : pygame.Surface = pressed_sprite
        self.unpressed_sprite : pygame.Surface = unpressed_sprite

        self.pressed : bool = False

    def switch_sprite(self, press : bool) -> None:
        if press:
            self.sprite = self.pressed_sprite
            self.pressed = True
        else:
            self.sprite = self.unpressed_sprite
            self.pressed = False

    def check_mouse(self, mouse_position) -> bool:
        if  (self.hitbox.x < mouse_position[0] < self.hitbox.x+self.hitbox.size[0] and
            self.hitbox.y < mouse_position[1] < self.hitbox.y + self.hitbox.size[1]):
            return True
        return False

class Grid(StaticObject):
    def __init__(self, grid_size : tuple[int,int], square_size : int , pos : tuple[float,float] = (0,0) ):
        super().__init__(pos= pos, size=grid_size)
        self.square_size = square_size

        self.match()

    def match(self, square_size : int = None):
        if square_size:
            self.square_size = square_size

        ...
