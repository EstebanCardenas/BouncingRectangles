from src.config import PlayerSpawn
from src.ecs.components import CTransform
from src.ecs.components import CSurface
from src.ecs.components.tags import CTagEnemy
import esper


def system_collision_player_enemy(
    world: esper.World,
    player_entity: int,
    player_spawn: PlayerSpawn
):
    components = world.get_components(CSurface, CTransform, CTagEnemy)
    player_transform = world.component_for_entity(player_entity, CTransform)
    player_surface = world.component_for_entity(player_entity, CSurface)

    player_rect = player_surface.surf.get_rect(topleft=player_transform.pos)
    for enemy_entity, (c_s, c_t, _) in components:
        enemy_rect = c_s.surf.get_rect(topleft=c_t.pos)
        if enemy_rect.colliderect(player_rect):
            world.delete_entity(enemy_entity)
            init_x, init_y = player_spawn.position
            player_transform.pos.x = init_x - \
                (player_surface.surf.get_width() / 2)
            player_transform.pos.y = init_y - \
                (player_surface.surf.get_height() / 2)
