import pygame


class ImagesService:
    def __init__(self):
        self._images = {}

    def get(self, path: str) -> pygame.Surface:
        if path in self._images:
            return self._images[path]

        self._images[path] = pygame.image.load(path).convert_alpha()
        return self._images[path]
