import pygame
from src.ecs.components.tags import CTagPlayer, CTagEnemy
import esper
import pygame

from src.ecs.components import CSurface, CTransform, CVelocity, CEnemySpawner, CInputCommand
from src.config import LevelEvent, PlayerConfig, PlayerSpawn

def create_player_square(
    world: esper.World,
    player_config: PlayerConfig,
    player_spawn: PlayerSpawn,
) -> int:
    size = pygame.Vector2(player_config.size[0], player_config.size[1])
    color = pygame.Color(player_config.color[0], player_config.color[1], player_config.color[2])
    pos = pygame.Vector2(
        player_spawn.position[0] - (size.x / 2), 
        player_spawn.position[1] - (size.y / 2),
    )
    vel = pygame.Vector2(0, 0)
    entity = create_square(world, size, color, pos, vel)
    world.add_component(entity, CTagPlayer())
    return entity

def create_enemy_square(
    world: esper.World,
    size: pygame.Vector2,
    color: pygame.Color,
    pos: pygame.Vector2,
    vel: pygame.Vector2,
):
    entity = create_square(world, size, color, pos, vel)
    world.add_component(entity, CTagEnemy())

def create_square(
    world: esper.World,
    size: pygame.Vector2,
    color: pygame.Color,
    pos: pygame.Vector2,
    vel: pygame.Vector2,
) -> int:
    cuad_entity = world.create_entity()
    world.add_component(
        cuad_entity,
        CSurface(
            size,
            color,
        )
    )
    world.add_component(
        cuad_entity,
        CTransform(pos)
    )
    world.add_component(
        cuad_entity,
        CVelocity(vel)
    )
    return cuad_entity

def create_enemy_spawner(
    world: esper.World,
    events: list[LevelEvent],
):
    spawner_entity = world.create_entity()
    world.add_component(
        spawner_entity,
        CEnemySpawner(events),
    )

def create_player_input(world: esper.World):
    input_left = world.create_entity()
    input_right = world.create_entity()
    input_up = world.create_entity()
    input_down = world.create_entity()
    world.add_component(
        input_left,
        CInputCommand(
            "PLAYER_LEFT",
            pygame.K_a,
        )
    )
    world.add_component(
        input_right,
        CInputCommand(
            "PLAYER_RIGHT",
            pygame.K_d,
        )
    )
    world.add_component(
        input_up,
        CInputCommand(
            "PLAYER_UP",
            pygame.K_w,
        )
    )
    world.add_component(
        input_down,
        CInputCommand(
            "PLAYER_DOWN",
            pygame.K_s,
        )
    )
