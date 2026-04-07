from src.ecs.components.tags import CTagBullet
from src.ecs.components import CTransform
from src.ecs.components import CSurface
import pygame
import esper

def system_bullet_boundaries(
    world: esper.World,
    screen: pygame.Surface,
):
    components = world.get_components(CSurface, CTransform, CTagBullet)
    for bullet_entity, (surf, transform, _) in components:
        rect = surf.surf.get_rect(topleft = transform.pos)
        if rect.left < 0 or rect.right > screen.width:
            world.delete_entity(bullet_entity)
        if rect.top < 0 or rect.bottom > screen.height:
            world.delete_entity(bullet_entity)
