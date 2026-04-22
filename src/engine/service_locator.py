from src.engine.services.sounds_service import SoundsService
from src.engine.services.images_service import ImagesService


class ServiceLocator:
    images_service = ImagesService()
    sounds_service = SoundsService()
