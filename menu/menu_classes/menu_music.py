import threading
import pygame


# Music
class Music:
    def __init__(self):
        pygame.mixer.init()
        self.tracks = [
            "assets(menu)/audio/main_music/town.mp3",
            "assets(menu)/audio/main_music/shadow.mp3"
        ]
        self.current_index = 0
        self.volume = 0.5
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
    def __init__(self, x, y, width, height, min_val, max_val, initial_val, label):
        self.rect = pygame.Rect(x, y, width, height)
        self.knob_radius = height * 1.5
        self.min_val = min_val
        self.max_val = max_val
        self.val = initial_val
        self.label = label
        self.dragging = False
        self.knob_x = x + (initial_val - min_val) / (max_val - min_val) * width
        self.font = pygame.font.Font(None, 36)

    def draw(self, surface):
        pygame.draw.rect(surface, (100, 100, 100), self.rect)
        pygame.draw.rect(surface, (200, 200, 200),
                         (self.rect.x, self.rect.y,
                          self.knob_x - self.rect.x,
                          self.rect.height))
        pygame.draw.circle(surface, (150, 150, 150),
                           (int(self.knob_x), self.rect.centery),
                           int(self.knob_radius))
        pygame.draw.circle(surface, (200, 200, 200),
                           (int(self.knob_x), self.rect.centery),
                           int(self.knob_radius - 2))
        text = self.font.render(f"{self.label}: {self.val:.0%}", True, (255, 255, 255))
        surface.blit(text, (self.rect.x, self.rect.y - 40))

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
