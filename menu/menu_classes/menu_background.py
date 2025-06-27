import threading
import pygame
import time
import os


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


# Dynamic switch backgrounds
class DynamicBackgroundManager(Background):
    def __init__(self, screen, folder_path, prefix = "bg", start = 0, end = 78,
                 extension = ".png", change_interval = 0.6):
        image_paths = [
            os.path.join(folder_path, f"{prefix}{i}{extension}")
            for i in range(start, end + 1)
        ]
        super().__init__(screen, image_paths = image_paths, change_interval = change_interval)
