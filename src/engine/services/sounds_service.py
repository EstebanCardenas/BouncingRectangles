import pygame


class SoundsService:
    def __init__(self):
        self._sounds = {}
        self._music_tracks = set()

    def play(self, path: str):
        if path not in self._sounds:
            self._sounds[path] = pygame.mixer.Sound(path)
        self._sounds[path].play()
