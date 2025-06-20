import pygame
import threading
import time
import os


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


# Change Background
class Background:
    def __init__(self, screen, image_paths = None, folder_path="assets(menu)/pictures/background", change_interval = 1.0):
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


# Methods for objects
class InteractiveObject:
    def __init__(self, x, y, image = None, shape = None, width = 100, height = 100,
                 color = (0, 0, 0), alpha = 0, angle = 0, sound_path = None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.alpha = alpha
        self.angle = angle
        self.shape = shape
        self.sound = None
        self.original_image = None
        self.image = None
        self.rect = None
        self.mask = None
        self.is_active = True

        if image:
            self.original_image = image.convert_alpha()
        elif shape:
            self._create_shape_surface()

        self._update_image()

        if sound_path:
            try:
                self.sound = pygame.mixer.Sound(sound_path)
            except pygame.error as e:
                print(f"Error loading sound: {e}")

    def _create_shape_surface(self):
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        if self.shape == "rect":
            pygame.draw.rect(surface, (*self.color, self.alpha), (0, 0, self.width, self.height))
        elif self.shape == "circle":
            pygame.draw.circle(surface, (*self.color, self.alpha),
                               (self.width // 2, self.height // 2), min(self.width, self.height) // 2)
        elif self.shape == "triangle":
            points = [
                (self.width // 2, 0),
                (0, self.height),
                (self.width, self.height)
            ]
            pygame.draw.polygon(surface, (*self.color, self.alpha), points)

        self.original_image = surface

    def _update_image(self):
        if not self.original_image:
            return

        mask_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        if self.shape == "rect":
            pygame.draw.rect(mask_surface, (255, 255, 255, 255), (0, 0, self.width, self.height))
        elif self.shape == "circle":
            pygame.draw.circle(mask_surface, (255, 255, 255, 255),
                               (self.width // 2, self.height // 2), min(self.width, self.height) // 2)
        elif self.shape == "triangle":
            points = [
                (self.width // 2, 0),
                (0, self.height),
                (self.width, self.height)
            ]
            pygame.draw.polygon(mask_surface, (255, 255, 255, 255), points)
        else:
            mask_surface = self.original_image.copy()

        if self.angle:
            mask_surface = pygame.transform.rotate(mask_surface, self.angle)
        self.mask = pygame.mask.from_surface(mask_surface)

        if self.angle:
            self.image = pygame.transform.rotate(self.original_image, self.angle)
        else:
            self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center = (self.x, self.y))

    def set_color(self, color):
        self.color = color
        if self.shape:
            self._create_shape_surface()
            self._update_image()

    def set_alpha(self, alpha):
        self.alpha = alpha
        if self.shape:
            self._create_shape_surface()
        self._update_image()

    def set_rotation(self, angle):
        self.angle = angle
        self._update_image()

    def resize(self, width, height):
        self.width = width
        self.height = height
        if self.shape:
            self._create_shape_surface()
        self._update_image()

    def draw(self, surface):
        if self.image and self.rect and self.is_active:
            surface.blit(self.image, self.rect)

    def is_clicked(self, pos):
        if not self.is_active or not self.rect or not self.mask:
            return False

        if self.rect.collidepoint(pos):
            x_local = pos[0] - self.rect.left
            y_local = pos[1] - self.rect.top
            try:
                return self.mask.get_at((x_local, y_local))
            except IndexError:
                return False
        return False

    def play_sound(self):
        if self.sound and self.is_active:
            self.sound.play()


# Storage & Add objects
class Objects:
    def __init__(self):
        self.objects = []
        self.hovered_object = None
        self.special_counter = 0
        self.special_objects = []
        self.special_sound = None

    def add(self, obj):
        self.objects.append(obj)

    def add_special(self, obj, sound_path):
        self.special_objects.append(obj)
        try:
            self.special_sound = pygame.mixer.Sound(sound_path)
        except pygame.error as e:
            print(f"Error loading special sound: {e}")

    def draw(self, surface):
        for obj in self.objects:
            obj.draw(surface)

    def handle_event(self, event, game_pos):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for obj in reversed(self.objects):
                if obj.is_clicked(game_pos):
                    if obj in self.special_objects:
                        self.special_counter += 1
                        if self.special_counter >= 6:
                            if self.special_sound:
                                self.special_sound.play()
                            self.special_counter = 0
                            return
                    obj.play_sound()
                    return


# Text
class Text:
    def __init__(self, font_path, font_size = 24, text = "", color = (255, 255, 255), position = (0, 0), alpha = 255, angle = 0):
        self.font_path = font_path
        self.font_size = font_size
        self.text = text
        self.color = color
        self.position = position
        self.alpha = alpha
        self.angle = angle
        self.rotation = 0
        self.scale = 1.0
        self.antialias = True
        self.shadow = False
        self.shadow_color = (0, 0, 0)
        self.shadow_offset = (2, 2)
        self._load_font()
        self.update_surface()

    def _load_font(self):
        try:
            self.font = pygame.font.Font(self.font_path, self.font_size)
        except IOError:
            print(f"Error loading font from {self.font_path}. Using default font.")
            self.font = pygame.font.SysFont(None, self.font_size)

    def update_surface(self):
        text_surface = self.font.render(self.text, self.antialias, self.color)
        if self.alpha < 255:
            text_surface = text_surface.convert_alpha()
            text_surface.fill((255, 255, 255, self.alpha), special_flags=pygame.BLEND_RGBA_MULT)
        if self.scale != 1.0:
            new_size = (int(text_surface.get_width() * self.scale),
                        int(text_surface.get_height() * self.scale))
            text_surface = pygame.transform.scale(text_surface, new_size)
        if self.angle != 0:
            original_rect = text_surface.get_rect(center=(self.position[0] + text_surface.get_width() // 2,
                                                          self.position[1] + text_surface.get_height() // 2))
            text_surface = pygame.transform.rotate(text_surface, self.angle)
            self.rect = text_surface.get_rect(center=original_rect.center)
        else:
            self.rect = text_surface.get_rect(topleft=self.position)
        if self.shadow:
            shadow_surf = self.font.render(self.text, self.antialias, self.shadow_color)
            if self.scale != 1.0:
                shadow_surf = pygame.transform.scale(shadow_surf,
                                                     (int(shadow_surf.get_width() * self.scale),
                                                      int(shadow_surf.get_height() * self.scale)))
            if self.angle != 0:
                shadow_surf = pygame.transform.rotate(shadow_surf, self.angle)

            combined = pygame.Surface(
                (max(text_surface.get_width(), shadow_surf.get_width()) + abs(self.shadow_offset[0]),
                 max(text_surface.get_height(), shadow_surf.get_height()) + abs(self.shadow_offset[1])),
                pygame.SRCALPHA
            )

            shadow_pos = (max(0, self.shadow_offset[0]), max(0, self.shadow_offset[1]))
            combined.blit(shadow_surf, shadow_pos)

            text_pos = (max(0, -self.shadow_offset[0]), max(0, -self.shadow_offset[1]))
            combined.blit(text_surface, text_pos)

            self.text_surface = combined
        else:
            self.text_surface = text_surface

    def set_rotation(self, angle):
        self.angle = angle
        self.update_surface()

    def set_text(self, text):
        self.text = text
        self.update_surface()

    def set_font_size(self, size):
        self.font_size = size
        self._load_font()
        self.update_surface()

    def set_color(self, color):
        self.color = color
        self.update_surface()

    def set_alpha(self, alpha):
        self.alpha = alpha
        self.update_surface()

    def set_position(self, position):
        self.position = position
        self.rect.top_left = position

    def set_rotation(self, angle):
        self.rotation = angle
        self.update_surface()

    def set_scale(self, scale):
        self.scale = scale
        self.update_surface()

    def set_shadow(self, enabled, color=(0, 0, 0), offset=(2, 2)):
        self.shadow = enabled
        self.shadow_color = color
        self.shadow_offset = offset
        self.update_surface()

    def draw(self, surface):
        surface.blit(self.text_surface, self.rect)


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
