from src.ecs.components.tags import CTagSpecialBullet, CTagHunter
from src.ecs.components import CTransform, CSurface
from src.create.prefab_creator import create_explosion
from src.config import ExplosionConfig
import esper

def system_collision_special_bullet_hunter(
    world: esper.World,
    explosion_config: ExplosionConfig
):
    special_bullets = world.get_components(CSurface, CTransform, CTagSpecialBullet)
    hunters = world.get_components(CSurface, CTransform, CTagHunter)
    
    for sb_entity, (sb_surf, sb_transform, _) in special_bullets:
        sb_rect = CSurface.get_area_relative(sb_surf.area, sb_transform.pos)
        for hunter_entity, (hunter_surf, hunter_transform, _) in hunters:
            hunter_rect = CSurface.get_area_relative(hunter_surf.area, hunter_transform.pos)
            if sb_rect.colliderect(hunter_rect):
                world.delete_entity(sb_entity)
                world.delete_entity(hunter_entity)
                create_explosion(world, hunter_transform.pos, explosion_config)
