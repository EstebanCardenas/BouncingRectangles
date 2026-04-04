import pygame
import esper

from src.ecs.components.tags import CTagEnemy
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity


def system_screen_bounce(
    world: esper.World,
    screen: pygame.Surface,
):
    screen_rect = screen.get_rect()
    components = world.get_components(
        CSurface, CTransform, CVelocity, CTagEnemy
    )

    for entity, (c_s, c_t, c_v, c_e) in components:
        rect = c_s.surf.get_rect(topleft=c_t.pos)
        if rect.left < 0 or rect.right > screen_rect.width:
            c_v.vel.x *= -1
            rect.clamp_ip(screen_rect)
            c_t.pos.x = rect.x
        if rect.top < 0 or rect.bottom > screen.height:
            c_v.vel.y *= - 1
            rect.clamp_ip(screen_rect)
            c_t.pos.y = rect.y
