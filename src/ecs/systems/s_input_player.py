from src.ecs.components import CInputCommand, CommandPhase
from typing import Callable
import pygame
import esper


def system_input_player(
    world: esper.World,
    event: pygame.event.Event,
    do_action: Callable[[CInputCommand], None]
):
    components = world.get_components(CInputCommand)
    for _, (c_ipt, ) in components:
        c_ipt: CInputCommand
        if event.type == pygame.KEYDOWN and c_ipt.key == event.key:
            c_ipt.phase = CommandPhase.START
            do_action(c_ipt)
        elif event.type == pygame.KEYUP and c_ipt.key == event.key:
            c_ipt.phase = CommandPhase.END
            do_action(c_ipt)
