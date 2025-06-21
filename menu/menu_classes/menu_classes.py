import pygame


# Menu
class MenuItem:
    def __init__(self, font_path, font_size, text, position,
                 text_color=(255, 255, 255),
                 bg_color=(50, 50, 150, 180),
                 bg_padding=10):
        self.text = Text(
            font_path=font_path,
            font_size=font_size,
            text=text,
            color=text_color,
            position=position,
            alpha=0
        )

        text_rect = self.text.rect
        self.bg_rect = pygame.Rect(
            text_rect.left - bg_padding,
            text_rect.top - bg_padding // 2,
            text_rect.width + bg_padding * 2,
            text_rect.height + bg_padding
        )

        self.bg_surface = pygame.Surface((self.bg_rect.width, self.bg_rect.height), pygame.SRCALPHA)
        self.bg_surface.fill(bg_color)
        self.bg_alpha = 0

    def set_alpha(self, alpha):
        self.text.set_alpha(alpha)
        self.bg_alpha = alpha

    def draw(self, surface):
        if self.bg_alpha > 0:
            bg_copy = self.bg_surface.copy()
            bg_copy.set_alpha(self.bg_alpha)
            surface.blit(bg_copy, self.bg_rect)
        self.text.draw(surface)

    def set_active(self, active):
        if active:
            self.bg_surface.fill((100, 100, 200, 220))
        else:
            self.bg_surface.fill((0, 0, 0, 0))
