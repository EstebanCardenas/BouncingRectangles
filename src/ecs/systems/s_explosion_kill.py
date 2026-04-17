import esper
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.tags import CTagExplosion

def system_explosion_kill(world: esper.World):
    components = world.get_components(CAnimation, CTagExplosion)
    for entity, (c_a, _) in components:
        if c_a.completed_once:
            world.delete_entity(entity)
