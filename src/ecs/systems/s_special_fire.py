from src.ecs.components.tags import CTagCooldownText
from src.ecs.components.tags import CTagBullet
import pygame
from src.config import BulletConfig
from src.create.prefab_creator import create_special_fire
from src.ecs.components import CTransform, CSpecialWeapon
import esper

def system_special_fire(
    world: esper.World,
    special_bullet_config: BulletConfig,
):
    player_components = world.get_component(CSpecialWeapon)
    if not player_components: return
    _, c_sw = player_components[0]
    
    if c_sw.time_until_next_fire > 0: return

    components = world.get_components(CTransform, CTagBullet)
    if len(components) == 0: return

    fired = False
    dirs = [(-1, -1), (1, -1), (-1, 1), (1, 1)]
    for b_entity, (c_t, _) in components:
        fired = True
        for i in range(4):
            vel = pygame.Vector2(*dirs[i]) * special_bullet_config.velocity
            create_special_fire(world, c_t.pos.copy(), vel, special_bullet_config)
        world.delete_entity(b_entity)
    
    if fired:
        c_sw.time_until_next_fire = c_sw.cooldown

def system_special_weapon_cooldown(world: esper.World, delta_time: float):
    components = world.get_component(CSpecialWeapon)
    for _, c_sw in components:
        if c_sw.time_until_next_fire > 0:
            c_sw.time_until_next_fire -= delta_time
