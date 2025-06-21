import pygame


# Smooth appearance and disappearance
class FadeAnimation:
    def __init__(self, screen):
        self.screen = screen

    def fade_in(self, surface, duration=2, pos = None):
        if pos is None:
            pos = (self.screen.get_width() // 2 - surface.get_width() // 2,
                   self.screen.get_height() // 2 - surface.get_height() // 2)

        for alpha in range(0, 256, 5):
            surface.set_alpha(alpha)
            self.screen.fill((0, 0, 0))
            self.screen.blit(surface, pos)
            pygame.display.flip()
            pygame.time.delay(int(duration * 1000 / 51))

    def fade_out(self, surface, duration = 2, pos = None):
        if pos is None:
            pos = (self.screen.get_width() // 2 - surface.get_width() // 2,
                   self.screen.get_height() // 2 - surface.get_height() // 2)

        for alpha in range(255, -1, -5):
            surface.set_alpha(alpha)
            self.screen.fill((0, 0, 0))
            self.screen.blit(surface, pos)
            pygame.display.flip()
            pygame.time.delay(int(duration * 1000 / 51))
