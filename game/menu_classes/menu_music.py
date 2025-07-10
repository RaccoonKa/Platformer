import threading
import pygame


# Music
class Music:
    def __init__(self, volume : float = 0.5):
        pygame.mixer.init()
        self.tracks = [
            "assets/audio/menu/main_music/town.mp3",
            "assets/audio/menu/main_music/shadow.mp3"
        ]
        self.current_index = 0
        self.volume = volume
        self._running = False
        self._thread = None

    def _play_loop(self):
        while self._running:
            try:
                pygame.mixer.music.load(self.tracks[self.current_index])
                pygame.mixer.music.set_volume(self.volume)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy() and self._running:
                    pygame.time.delay(100)
                self.current_index = (self.current_index + 1) % len(self.tracks)
            except pygame.error as e:
                print(f"Error to load music: {e}")
                break

    def play_loop(self, track_name = None):
        if not self._running:
            self._running = True
            self._thread = threading.Thread(target=self._play_loop, daemon=True)
            self._thread.start()

    def stop(self):
        self._running = False
        pygame.mixer.music.stop()

    def set_volume(self, volume):
        self.volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.volume)


# Slider music
class Slider:
    def __init__(self, x, y, width, height, min_val, max_val, initial_val, label,
                 font_path=None, font_size=36, font_color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.knob_radius = int(height * 1.5)
        self.min_val = min_val
        self.max_val = max_val
        self.val = initial_val
        self.label = label
        self.dragging = False
        self.knob_x = x + (initial_val - min_val) / (max_val - min_val) * width
        self.alpha = 255
        self.active = False

        try:
            if font_path:
                self.font = pygame.font.Font(font_path, font_size)
            else:
                self.font = pygame.font.Font(None, font_size)
        except:
            self.font = pygame.font.Font(None, font_size)

    def set_alpha(self, alpha):
        self.alpha = alpha

    def set_active(self, active):
        self.active = active

    def draw(self, surface):
        text_surface = self.font.render(f"{self.label}: {self.val:.0%}", True, (255, 255, 255))
        text_surface.set_alpha(self.alpha)
        surface.blit(text_surface, (self.rect.x, self.rect.y - 40))
        bg_surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        bg_surf.fill((100, 100, 200, int(220 * (self.alpha / 255))))
        surface.blit(bg_surf, self.rect)
        fill_width = max(0, self.knob_x - self.rect.left)
        if fill_width > 0:
            fill_surf = pygame.Surface((fill_width, self.rect.height), pygame.SRCALPHA)
            fill_surf.fill((100, 100, 200, int(220 * (self.alpha / 255))))
            surface.blit(fill_surf, self.rect)
        knob_surface = pygame.Surface((2 * self.knob_radius, 2 * self.knob_radius), pygame.SRCALPHA)
        pygame.draw.circle(knob_surface, (150, 150, 150, self.alpha),
                           (self.knob_radius, self.knob_radius), self.knob_radius)
        inner_color = (255, 77, 0) if self.active else (200, 200, 200)
        pygame.draw.circle(knob_surface, (*inner_color, self.alpha),
                           (self.knob_radius, self.knob_radius), self.knob_radius - 2)
        circle_pos = (self.knob_x - self.knob_radius, self.rect.centery - self.knob_radius)
        surface.blit(knob_surface, circle_pos)

    def handle_event(self, event, game_pos):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                knob_rect = pygame.Rect(self.knob_x - self.knob_radius,
                                        self.rect.centery - self.knob_radius,
                                        self.knob_radius * 2,
                                        self.knob_radius * 2)
                if knob_rect.collidepoint(game_pos) or self.rect.collidepoint(game_pos):
                    self.dragging = True
                    self.knob_x = max(self.rect.left, min(game_pos[0], self.rect.right))
                    self.val = self.min_val + (self.knob_x - self.rect.left) / self.rect.width * (
                                self.max_val - self.min_val)

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.knob_x = max(self.rect.left, min(game_pos[0], self.rect.right))
            self.val = self.min_val + (self.knob_x - self.rect.left) / self.rect.width * (self.max_val - self.min_val)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False

    def get_value(self):
        return self.val
