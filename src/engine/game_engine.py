from src.create.prefab_creator import create_cooldown_text
from src.ecs.systems.s_special_fire import system_special_fire, system_special_weapon_cooldown
from src.create.prefab_creator import create_text
from src.engine.service_locator import ServiceLocator
import asyncio
from src.ecs.systems.s_hunter_state import system_hunter_state
from src.ecs.systems.s_explosion_kill import system_explosion_kill
from src.ecs.systems.s_collision_bullet_hunter import system_collision_bullet_hunter
from src.ecs.systems.s_player_state import system_player_state
from src.ecs.systems.s_animation import system_animation
from src.ecs.systems.s_play_track import system_play_track
from src.create.prefab_creator import create_bg_track
from src.ecs.systems.s_player_fire import system_player_fire
from src.ecs.systems.s_collision_bullet_enemy import system_collision_bullet_enemy
from src.ecs.systems.s_bullet_boundaries import system_bullet_boundaries
from src.ecs.systems.s_player_clicks import system_player_clicks
from src.ecs.systems import system_player_boundaries
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
    ) -> None:
        # Config objects
        self.config = config
        self.level_config = config.level_config
        self.player_config = config.player_config

        # Init logic
        pygame.init()
        self.screen = pygame.display.set_mode(
            config.size,
            0,
        )
        pygame.display.set_caption(config.title)
        self.clock = pygame.time.Clock()
        self.is_running = False
        self.framerate = config.framerate
        self.delta_time = 0.0
        self.current_time = 0.0
        self.is_paused = False

        # Init pause visuals
        font = ServiceLocator.fonts_service.get(config.font_path, 28)
        self.pause_text = font.render(
            'PAUSADO', True, pygame.Color(255, 255, 255))
        self.pause_rect = self.pause_text.get_rect(
            center=self.screen.get_rect().center)

        self.ecs_world = esper.World()

    async def run(self) -> None:
        self._create()
        self.is_running = True
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
            await asyncio.sleep(0)
        self._clean()

    def _create(self):
        ic = self.config.interface_config
        create_text( # Render title
            self.ecs_world,
            text=ic.title.content,
            font_path=ic.title.font,
            font_size=ic.title.font_size,
            color=ic.title.color,
            pos=(16, 16)
        )
        create_text( # Render subtitle
            self.ecs_world,
            text=ic.subtitle.content,
            font_path=ic.subtitle.font,
            font_size=ic.subtitle.font_size,
            color=ic.subtitle.color,
            pos=(16, 16 + ic.title.font_size + 8) # Initial padding + title size + spacing between title
        )
        special_text_y = self.config.size[1] - 28 - ic.special_text.font_size
        create_text( # Render special power text
            self.ecs_world,
            text=ic.special_text.content,
            font_path=ic.special_text.font,
            font_size=ic.special_text.font_size,
            color=ic.special_text.color,
            pos=(16, special_text_y)
        )
        create_cooldown_text( # Render cooldown
            self.ecs_world,
            text="100%",
            font_path=ic.special_text.font,
            font_size=8,
            color=pygame.Color(0, 255, 0),
            pos=(16, special_text_y + ic.special_text.font_size + 4)
        )

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
        create_bg_track(self.ecs_world, self.config.bg_track_path)

        system_play_track(self.ecs_world)

    def _calculate_time(self):
        self.clock.tick(self.framerate)
        self.delta_time = self.clock.get_time() / 1000.0
        self.current_time += self.delta_time

    def _process_events(self):
        for event in pygame.event.get():
            system_input_player(self.ecs_world, event, self._do_action)
            system_player_clicks(
                self.ecs_world,
                event,
                on_click=self._handle_click,
            )
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        if self.is_paused:
            return
        system_enemy_spawner(self.ecs_world, self.current_time)
        system_movement(self.ecs_world, self.delta_time)
        system_lifetime(self.ecs_world, self.delta_time)
        system_special_weapon_cooldown(self.ecs_world, self.delta_time)
        system_update_cooldown_text(self.ecs_world, self.config.interface_config.special_text.font)

        system_player_state(self.ecs_world)
        system_hunter_state(self.ecs_world)
        system_screen_bounce(self.ecs_world, self.screen)
        system_collision_player_enemy(
            self.ecs_world,
            self.player_entity,
            self.level_config.player_spawn,
            self.config.explosion_config
        )
        system_player_boundaries(
            self.ecs_world, self.screen, self.player_entity)
        system_bullet_boundaries(self.ecs_world, self.screen)
        system_collision_bullet_enemy(
            self.ecs_world, self.config.explosion_config)
        system_collision_bullet_hunter(
            self.ecs_world, self.config.explosion_config)
        system_collision_special_bullet_enemy(
            self.ecs_world, self.config.explosion_config)
        system_collision_special_bullet_hunter(
            self.ecs_world, self.config.explosion_config)

        system_animation(self.ecs_world, self.delta_time)
        system_explosion_kill(self.ecs_world)

        self.ecs_world._clear_dead_entities()

    def _draw(self):
        self.screen.fill(self.config.bg_color)
        system_rendering(self.ecs_world, self.screen)
        if self.is_paused:
            self.screen.blit(self.pause_text, self.pause_rect)
        pygame.display.flip()

    def _handle_click(self, c_input: CInputCommand, click_pos: tuple[int, int]):
        if self.is_paused:
            return
        if c_input.name == 'PLAYER_FIRE':
            system_player_fire(
                self.ecs_world,
                click_pos=click_pos,
                bullet_limit=self.level_config.player_spawn.max_bullets,
                bullet_config=self.config.bullet_config,
            )
        elif c_input.name == 'PLAYER_SPECIAL':
            system_special_fire(self.ecs_world, self.config.special_bullet_config)

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
        elif c_input.name == 'GAME_PAUSE':
            if c_input.phase == CommandPhase.START:
                self.is_paused = not self.is_paused

    def _clean(self):
        self.ecs_world.clear_database()
        pygame.quit()
