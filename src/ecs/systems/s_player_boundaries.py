from src.ecs.components import CTransform
from src.ecs.components import CSurface
import pygame
import esper

def system_player_boundaries(
    world: esper.World,
    screen: pygame.Surface,
    player_entity: int,
):
    screen_rect = screen.get_rect()
    ply_surface = world.component_for_entity(player_entity, CSurface)
    ply_transform = world.component_for_entity(player_entity, CTransform)
    ply_rect = CSurface.get_area_relative(ply_surface.area, ply_transform.pos)
    
    # Correct horizontal position
    if ply_rect.left < 0:
        ply_transform.pos.x = 0
    elif ply_rect.right > screen_rect.width:
        ply_transform.pos.x = screen_rect.width - ply_rect.width
    # Correct vertical position
    if ply_rect.top < 0:
        ply_transform.pos.y = 0
    elif ply_rect.bottom > screen_rect.height:
        ply_transform.pos.y = screen_rect.height - ply_rect.height
