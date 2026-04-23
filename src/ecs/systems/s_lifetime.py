from src.ecs.components import CLifetime
import esper

def system_lifetime(world: esper.World, delta_time: float):
    components = world.get_component(CLifetime)
    for entity, c_l in components:
        c_l.lifetime -= delta_time
        if c_l.lifetime <= 0:
            world.delete_entity(entity)
