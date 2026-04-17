from src.config import PlayerSpawn, ExplosionConfig
from src.ecs.components import CTransform
from src.ecs.components import CSurface
from src.ecs.components.tags import CTagEnemy, CTagHunter
from src.create.prefab_creator import create_explosion
import esper
import pygame


def system_collision_player_enemy(
    world: esper.World,
    player_entity: int,
    player_spawn: PlayerSpawn,
    explosion_config: ExplosionConfig
):
    enemies = world.get_components(CSurface, CTransform, CTagEnemy)
    hunters = world.get_components(CSurface, CTransform, CTagHunter)
    
    player_transform = world.component_for_entity(player_entity, CTransform)
    player_surface = world.component_for_entity(player_entity, CSurface)

    player_rect = CSurface.get_area_relative(player_surface.area, player_transform.pos)
    
    # Check standard enemies
    for enemy_entity, (c_s, c_t, _) in enemies:
        enemy_rect = CSurface.get_area_relative(c_s.area, c_t.pos)
        if enemy_rect.colliderect(player_rect):
            _resolve_player_collision(world, enemy_entity, player_transform, player_surface, player_spawn, explosion_config, c_t.pos)

    # Check hunters
    for hunter_entity, (c_s, c_t, _) in hunters:
        hunter_rect = CSurface.get_area_relative(c_s.area, c_t.pos)
        if hunter_rect.colliderect(player_rect):
            _resolve_player_collision(world, hunter_entity, player_transform, player_surface, player_spawn, explosion_config, c_t.pos)

def _resolve_player_collision(world: esper.World, enemy_entity: int, player_transform: CTransform, player_surface: CSurface, player_spawn: PlayerSpawn, explosion_config: ExplosionConfig, enemy_pos: pygame.Vector2):
    world.delete_entity(enemy_entity)
    create_explosion(world, enemy_pos, explosion_config)
    
    init_x, init_y = player_spawn.position
    player_transform.pos.x = init_x - \
        (player_surface.area.w / 2)
    player_transform.pos.y = init_y - \
        (player_surface.area.h / 2)
