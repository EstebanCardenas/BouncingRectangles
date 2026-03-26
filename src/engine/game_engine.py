import pygame
import esper

from src.config import EngineConfig, EnemyData, EnemiesConfig, LevelConfig
from src.create.prefab_creator import create_enemy_spawner
from src.ecs.components import *
from src.ecs.systems import *


class GameEngine:
    config: EngineConfig
    level_config: LevelConfig
    enemies: dict[str, EnemyData]

    def __init__(
        self, 
        config: EngineConfig,
        level_config: LevelConfig,
        enemies_config: EnemiesConfig,
    ) -> None:
        # Config objects
        self.config = config
        self.level_config = level_config
        self.enemies = enemies_config.enemies
        # Init logic
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
        self.current_time = 0.0

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
        create_enemy_spawner(
            self.ecs_world,
            events=self.level_config.events,
        )

    def _calculate_time(self):
        self.clock.tick(self.framerate)
        self.delta_time = self.clock.get_time() / 1000.0
        self.current_time += self.delta_time

    def _process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        system_movement(self.ecs_world, self.delta_time)
        system_screen_bounce(self.ecs_world, self.screen)
        system_enemy_spawner(self.ecs_world, self.current_time, self.enemies)

    def _draw(self):
        self.screen.fill(self.config.bg_color)
        system_rendering(self.ecs_world, self.screen)
        pygame.display.flip()

    def _clean(self):
        pygame.quit()
