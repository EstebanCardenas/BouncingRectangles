import pygame
import esper

from src.engine.engine_config import EngineConfig
from src.create.prefab_creator import crear_cuadrado
from src.ecs.components import *
from src.ecs.systems import *

class GameEngine:
    config: EngineConfig

    def __init__(self, config: EngineConfig) -> None:
        self.config = config
        pygame.init()
        self.screen = pygame.display.set_mode(
            config.size,
            pygame.SCALED,
        )
        pygame.display.set_caption(config.title)
        self.clock = pygame.time.Clock()
        self.is_running = False
        self.framerate = config.framerate
        self.delta_time = 0.0

        self.ecs_world = esper.World()

    def run(self) -> None:
        self._create()
        self.is_running = True
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
        self._clean()

    def _create(self):
        crear_cuadrado(
            self.ecs_world, 
            size=pygame.Vector2(50, 50), 
            color=pygame.Color(255, 255, 100),
            pos=pygame.Vector2(150, 100),
            vel=pygame.Vector2(100, 100),
        )

    def _calculate_time(self):
        self.clock.tick(self.framerate)
        self.delta_time = self.clock.get_time() / 1000.0

    def _process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        system_movement(self.ecs_world, self.delta_time)
        system_screen_bounce(self.ecs_world, self.screen)

    def _draw(self):
        self.screen.fill(self.config.bg_color)
        system_rendering(self.ecs_world, self.screen)
        pygame.display.flip()

    def _clean(self):
        pygame.quit()
