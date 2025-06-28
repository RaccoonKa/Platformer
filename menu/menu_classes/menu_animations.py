import pygame
import random

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


# The glitch effect
class GlitchEffect:
    def __init__(self, screen, base_surface, duration=1.0):
        self.screen = screen
        self.base_surface = base_surface
        self.duration = duration
        self.start_time = pygame.time.get_ticks()
        self.glitch_frames = self.generate_glitch_frames()

    def generate_glitch_frames(self):
        frames = []
        width, height = self.base_surface.get_size()

        for _ in range(10):
            frame = self.base_surface.copy()
            strip_height = 5
            for y in range(0, height, strip_height):
                if random.random() < 0.2:
                    shift = random.randint(-20, 20)
                    strip = frame.subsurface((0, y, width, strip_height)).copy()
                    frame.blit(strip, (shift, y))

            noise_surface = pygame.Surface((width, height), pygame.SRCALPHA)
            for _ in range(100):
                x = random.randint(0, width - 1)
                y = random.randint(0, height - 1)
                color = (random.randint(200, 255), random.randint(200, 255), random.randint(200, 255))
                pygame.draw.rect(noise_surface, color, (x, y, 1, 1))
            frame.blit(noise_surface, (0, 0))

            if random.random() < 0.3:
                stripe_height = random.randint(10, 50)
                stripe_y = random.randint(0, height - stripe_height)
                stripe = frame.subsurface((0, stripe_y, width, stripe_height)).copy()
                inverted = pygame.Surface((width, stripe_height))
                inverted.fill((255, 255, 255))
                inverted.blit(stripe, (0, 0), special_flags=pygame.BLEND_SUB)
                frame.blit(inverted, (0, stripe_y))

            frames.append(frame)

        return frames

    def update(self):
        elapsed = (pygame.time.get_ticks() - self.start_time) / 2000
        progress = min(elapsed / self.duration, 1.0)
        frame_index = int(progress * len(self.glitch_frames) * 2) % len(self.glitch_frames)
        return self.glitch_frames[frame_index], progress >= 1.0
