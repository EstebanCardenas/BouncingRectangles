from typing import Callable
from src.ecs.systems.s_player_fire import system_player_fire
import pygame
from src.ecs.components import CInputCommand
import esper

def system_player_clicks(
    world: esper.World,
    event: pygame.event.Event,
    on_click: Callable[[CInputCommand, tuple[int, int]], None]
):
    components = world.get_components(CInputCommand)
    for _, (c_ipt, ) in components:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == c_ipt.key:
            on_click(c_ipt, event.pos)
