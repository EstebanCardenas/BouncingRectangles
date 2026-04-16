from src.ecs.components.tags import CTagBullet
from src.ecs.components.tags import CTagEnemy
from src.ecs.components import CTransform
from src.ecs.components import CSurface
import esper

def system_collision_bullet_enemy(
    world: esper.World,
):
    bullets = world.get_components(CSurface, CTransform, CTagBullet)
    enemies = world.get_components(CSurface, CTransform, CTagEnemy)
    
    for bullet_entity, (bullet_surf, bullet_transform, _) in bullets:
        bullet_rect = CSurface.get_area_relative(bullet_surf.area, bullet_transform.pos)
        for enemy_entity, (enemy_surf, enemy_transform, _) in enemies:
            enemy_rect = CSurface.get_area_relative(enemy_surf.area, enemy_transform.pos)
            if bullet_rect.colliderect(enemy_rect):
                world.delete_entity(bullet_entity)
                world.delete_entity(enemy_entity)
