import pygame
import os
from typing import Dict, Optional


class SoundEngine:
    def __init__(self, max_channels: int = 32):
        pygame.mixer.init()
        self.stop_all()
        pygame.mixer.set_num_channels(max_channels)
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.music_volume: float = 1.0
        self.sound_volume: float = 1.0
        self.current_music: Optional[str] = None
        self.now_music_volume : float = 1
        self.now_sound_volume : float = 1

    def load_sound(self, name: str, file_path: str, sound_volume : float = None) -> None:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Sound file not found: {file_path}")
        self.sounds[name] = pygame.mixer.Sound(file_path)
        if sound_volume:
            self.sounds[name].set_volume(sound_volume)
        else:
            self.sounds[name].set_volume(self.sound_volume)

    def play_sound(self, name: str, loops: int = 0, volume: Optional[float] = None) -> None:
        if name in self.sounds:
            if volume is not None:
                self.sounds[name].set_volume(volume)
            self.sounds[name].play(loops=loops)
        else:
            raise ValueError(f"Sound not loaded: {name}")

    def stop_sound(self, name: str) -> None:
        if name in self.sounds:
            self.sounds[name].stop()

    def load_music(self, file_path: str) -> None:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Music file not found: {file_path}")
        pygame.mixer.music.load(file_path)

    def play_music(self, file_path: Optional[str] = None, loops: int = -1, volume: Optional[float] = None) -> None:
        if file_path:
            self.load_music(file_path)
            self.current_music = file_path

        if volume is not None:
            self.set_music_volume(volume)

        pygame.mixer.music.play(loops=loops)

    def stop_music(self) -> None:
        pygame.mixer.music.stop()
        self.current_music = None

    def pause_music(self) -> None:
        pygame.mixer.music.pause()

    def resume_music(self) -> None:
        pygame.mixer.music.unpause()

    def set_music_volume(self, volume: float) -> None:
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)

    def set_sound_volume(self, volume: float) -> None:
        self.sound_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.sound_volume)

    def fadeout_music(self, duration: int = 1000) -> None:
        pygame.mixer.music.fadeout(duration)
        self.current_music = None

    def is_music_playing(self) -> bool:
        return pygame.mixer.music.get_busy()

    def stop_all(self):
        pygame.mixer.stop()
        pygame.mixer.music.stop()

    def update(self) -> None:
        pass