import esper
import random
import pygame

from src.ecs.components import CEnemySpawner
from src.create.prefab_creator import create_enemy_square
from src.config import EnemyData

def system_enemy_spawner(
    world: esper.World,
    current_time: float,
):
    components = world.get_components(CEnemySpawner)

    c_es: CEnemySpawner
    for entity, (c_es, ) in components:
        for evt in c_es.evts:
            if current_time >= evt.time and (not evt.triggered):
                enemy = evt.enemy_data
                
                # Generate random velocity magnitude
                velocity_magnitude = random.uniform(enemy.velocity_min, enemy.velocity_max)
                # Randomize direction components
                velocity_direction = pygame.Vector2(random.choice([-1, 1]), random.choice([-1, 1]))
                # Compute final velocity vector
                velocity = velocity_direction * velocity_magnitude

                create_enemy_square(
                    world,
                    img=enemy.img,
                    pos=pygame.Vector2(evt.position),
                    vel=velocity
                )
                evt.triggered = True
