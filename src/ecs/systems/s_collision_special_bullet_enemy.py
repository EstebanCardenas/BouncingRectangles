from src.ecs.components.tags import CTagSpecialBullet, CTagEnemy
from src.ecs.components import CTransform, CSurface
from src.create.prefab_creator import create_explosion
from src.config import ExplosionConfig
import esper

def system_collision_special_bullet_enemy(
    world: esper.World,
    explosion_config: ExplosionConfig
):
    special_bullets = world.get_components(CSurface, CTransform, CTagSpecialBullet)
    enemies = world.get_components(CSurface, CTransform, CTagEnemy)
    
    for sb_entity, (sb_surf, sb_transform, _) in special_bullets:
        sb_rect = CSurface.get_area_relative(sb_surf.area, sb_transform.pos)
        for enemy_entity, (enemy_surf, enemy_transform, _) in enemies:
            enemy_rect = CSurface.get_area_relative(enemy_surf.area, enemy_transform.pos)
            if sb_rect.colliderect(enemy_rect):
                world.delete_entity(sb_entity)
                world.delete_entity(enemy_entity)
                create_explosion(world, enemy_transform.pos, explosion_config)
