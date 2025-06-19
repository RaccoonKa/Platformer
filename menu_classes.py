import pygame
import threading
import time
import os


# Smooth appearance and disappearance
class FadeAnimation:
    def __init__(self, screen):
        self.screen = screen

    def fade_in(self, surface, duration=2, pos=None):
        if pos is None:
            pos = (self.screen.get_width() // 2 - surface.get_width() // 2,
                   self.screen.get_height() // 2 - surface.get_height() // 2)

        for alpha in range(0, 256, 5):
            surface.set_alpha(alpha)
            self.screen.fill((0, 0, 0))
            self.screen.blit(surface, pos)
            pygame.display.flip()
            pygame.time.delay(int(duration * 1000 / 51))

    def fade_out(self, surface, duration=2, pos=None):
        if pos is None:
            pos = (self.screen.get_width() // 2 - surface.get_width() // 2,
                   self.screen.get_height() // 2 - surface.get_height() // 2)

        for alpha in range(255, -1, -5):
            surface.set_alpha(alpha)
            self.screen.fill((0, 0, 0))
            self.screen.blit(surface, pos)
            pygame.display.flip()
            pygame.time.delay(int(duration * 1000 / 51))


# Change Background
class Background:
    def __init__(self, screen, image_paths=None, folder_path="assets(menu)/pictures/background", change_interval=1.0):
        self.screen = screen
        self.change_interval = change_interval
        self.backgrounds = []
        self.current_index = 0
        self._running = False
        self._thread = None
        self.current_background = None

        if image_paths:
            self._load_from_list(image_paths)
        else:
            self._load_from_folder(folder_path)

        if not self.backgrounds:
            self._create_fallback()

    def _load_from_list(self, image_paths):
        for path in image_paths:
            try:
                image = pygame.image.load(path).convert()
                self.backgrounds.append(image)
            except (pygame.error, FileNotFoundError) as e:
                print(f"Error loading background {path}: {e}")
                self._add_fallback_image()

    def _load_from_folder(self, folder_path):
        try:
            files = sorted(os.listdir(folder_path))
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    path = os.path.join(folder_path, file)
                    try:
                        image = pygame.image.load(path).convert()
                        self.backgrounds.append(image)
                    except pygame.error as e:
                        print(f"Error loading background {file}: {e}")
                        self._add_fallback_image()
        except OSError as e:
            print(f"Error accessing background folder: {e}")
            self._create_fallback()

    def _add_fallback_image(self):
        fallback = pygame.Surface((1920, 1080))
        fallback.fill((0, 0, 0))
        self.backgrounds.append(fallback)

    def _create_fallback(self):
        print("No backgrounds loaded - creating fallback")
        self._add_fallback_image()

    def set_custom_order(self, new_order):
        if len(new_order) == len(self.backgrounds):
            self.backgrounds = [self.backgrounds[i] for i in new_order]
            self.current_index = 0
        else:
            print("Error: New order length doesn't match backgrounds count")

    def _change_background(self):
        while self._running:
            self.current_index = (self.current_index + 1) % len(self.backgrounds)
            self.current_background = self.backgrounds[self.current_index]
            time.sleep(self.change_interval)

    def start(self):
        if not self._running and len(self.backgrounds) > 0:
            self._running = True
            self.current_background = self.backgrounds[self.current_index]
            self._thread = threading.Thread(target=self._change_background, daemon=True)
            self._thread.start()

    def stop(self):
        self._running = False

    def get_current_background(self):
        return self.current_background

# Objects
class InteractiveObject:
    def __init__(self, x, y, width, height, sound_path=None, hover_sound_path=None):
        self.logical_rect = pygame.Rect(x, y, width, height)
        self.sound = None
        self.hover_sound = None
        self.is_hovered = False

        if sound_path and os.path.exists(sound_path):
            self.sound = pygame.mixer.Sound(sound_path)

        if hover_sound_path and os.path.exists(hover_sound_path):
            self.hover_sound = pygame.mixer.Sound(hover_sound_path)

    def check_hover(self, mouse_pos, scale_x, scale_y):
        scaled_rect = pygame.Rect(
            self.logical_rect.x * scale_x,
            self.logical_rect.y * scale_y,
            self.logical_rect.width * scale_x,
            self.logical_rect.height * scale_y
        )

        was_hovered = self.is_hovered
        self.is_hovered = scaled_rect.collidepoint(mouse_pos)

        if self.hover_sound and self.is_hovered and not was_hovered:
            self.hover_sound.play()

        return self.is_hovered

    def handle_click(self):
        if self.sound and self.is_hovered:
            self.sound.play()
            return True
        return False

    def draw_debug(self, surface, scale_x, scale_y, color=(255, 0, 0)):
        scaled_rect = pygame.Rect(
            self.logical_rect.x * scale_x,
            self.logical_rect.y * scale_y,
            self.logical_rect.width * scale_x,
            self.logical_rect.height * scale_y
        )
        pygame.draw.rect(surface, color, scaled_rect, 2)


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

    def play_loop(self, track_name=None):
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
