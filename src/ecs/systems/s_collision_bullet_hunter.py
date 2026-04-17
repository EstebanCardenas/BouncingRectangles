from src.ecs.components.tags import CTagBullet, CTagHunter
from src.ecs.components import CTransform, CSurface
from src.create.prefab_creator import create_explosion
from src.config import ExplosionConfig
import esper

def system_collision_bullet_hunter(
    world: esper.World,
    explosion_config: ExplosionConfig
):
    bullets = world.get_components(CSurface, CTransform, CTagBullet)
    hunters = world.get_components(CSurface, CTransform, CTagHunter)
    
    for bullet_entity, (bullet_surf, bullet_transform, _) in bullets:
        bullet_rect = CSurface.get_area_relative(bullet_surf.area, bullet_transform.pos)
        for hunter_entity, (hunter_surf, hunter_transform, _) in hunters:
            hunter_rect = CSurface.get_area_relative(hunter_surf.area, hunter_transform.pos)
            if bullet_rect.colliderect(hunter_rect):
                world.delete_entity(bullet_entity)
                world.delete_entity(hunter_entity)
                create_explosion(world, hunter_transform.pos, explosion_config)
