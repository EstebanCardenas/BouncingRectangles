import esper
import pygame

from src.ecs.components import CSurface, CTransform, CVelocity

def crear_cuadrado(
    world: esper.World,
    size: pygame.Vector2,
    color: pygame.Color,
    pos: pygame.Vector2,
    vel: pygame.Vector2,
):
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
