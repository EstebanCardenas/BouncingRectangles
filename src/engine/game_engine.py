from src.ecs.systems.s_collision_player_enemy import system_collision_player_enemy
import pygame
import esper

from src.config import EngineConfig, LevelConfig, PlayerConfig
from src.create.prefab_creator import create_enemy_spawner, create_player_square, create_player_input
from src.ecs.components import *
from src.ecs.systems import *


class GameEngine:
    config: EngineConfig
    level_config: LevelConfig
    player_config: PlayerConfig

    def __init__(
        self,
        config: EngineConfig,
        level_config: LevelConfig,
        player_config: PlayerConfig,
    ) -> None:
        # Config objects
        self.config = config
        self.level_config = level_config
        self.player_config = player_config
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
        self.player_entity = create_player_square(
            self.ecs_world,
            self.player_config,
            self.level_config.player_spawn,
        )
        self.player_c_vel = self.ecs_world.component_for_entity(
            self.player_entity, CVelocity)

        create_enemy_spawner(
            self.ecs_world,
            events=self.level_config.events,
        )
        create_player_input(self.ecs_world)

    def _calculate_time(self):
        self.clock.tick(self.framerate)
        self.delta_time = self.clock.get_time() / 1000.0
        self.current_time += self.delta_time

    def _process_events(self):
        for event in pygame.event.get():
            system_input_player(self.ecs_world, event, self._do_action)
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        system_movement(self.ecs_world, self.delta_time)
        system_screen_bounce(self.ecs_world, self.screen)
        system_enemy_spawner(self.ecs_world, self.current_time)
        system_collision_player_enemy(
            self.ecs_world,
            self.player_entity,
            self.level_config.player_spawn
        )
        self.ecs_world._clear_dead_entities()

    def _draw(self):
        self.screen.fill(self.config.bg_color)
        system_rendering(self.ecs_world, self.screen)
        pygame.display.flip()

    def _do_action(self, c_input: CInputCommand):
        if c_input.name == 'PLAYER_LEFT':
            if c_input.phase == CommandPhase.START:
                self.player_c_vel.vel.x -= self.player_config.input_velocity
            elif c_input.phase == CommandPhase.END:
                self.player_c_vel.vel.x += self.player_config.input_velocity
        elif c_input.name == 'PLAYER_RIGHT':
            if c_input.phase == CommandPhase.START:
                self.player_c_vel.vel.x += self.player_config.input_velocity
            elif c_input.phase == CommandPhase.END:
                self.player_c_vel.vel.x -= self.player_config.input_velocity
        elif c_input.name == 'PLAYER_UP':
            if c_input.phase == CommandPhase.START:
                self.player_c_vel.vel.y -= self.player_config.input_velocity
            elif c_input.phase == CommandPhase.END:
                self.player_c_vel.vel.y += self.player_config.input_velocity
        elif c_input.name == 'PLAYER_DOWN':
            if c_input.phase == CommandPhase.START:
                self.player_c_vel.vel.y += self.player_config.input_velocity
            elif c_input.phase == CommandPhase.END:
                self.player_c_vel.vel.y -= self.player_config.input_velocity

    def _clean(self):
        self.ecs_world.clear_database()
        pygame.quit()
