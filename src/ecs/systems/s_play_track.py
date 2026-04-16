import pygame
from src.ecs.components.c_background_track import CBackgroundTrack
import esper


def system_play_track(world: esper.World):
    components = world.get_components(CBackgroundTrack)
    for _, (c_bg_track, ) in components:
        pygame.mixer.music.load(c_bg_track.track_path)
        pygame.mixer.music.set_volume(0.25)
        pygame.mixer.music.play()
