import esper
import random
import pygame

from src.ecs.components import CEnemySpawner
from src.create.prefab_creator import create_enemy_square, create_enemy_hunter

def system_enemy_spawner(
    world: esper.World,
    current_time: float,
):
    components = world.get_components(CEnemySpawner)

    c_es: CEnemySpawner
    for entity, (c_es, ) in components:
        for evt in c_es.evts:
            if current_time >= evt.time and (not evt.triggered):
                enemy_config = evt.enemy_data
                if enemy_config.enemy_type == 'asteroid':
                    # Generate random velocity magnitude
                    velocity_magnitude = random.uniform(enemy_config.velocity_min, enemy_config.velocity_max)
                    # Randomize direction components
                    velocity_direction = pygame.Vector2(random.choice([-1, 1]), random.choice([-1, 1]))
                    # Compute final velocity vector
                    velocity = velocity_direction * velocity_magnitude

                    create_enemy_square(
                        world,
                        img=enemy_config.img,
                        pos=pygame.Vector2(evt.position),
                        vel=velocity
                    )
                elif enemy_config.enemy_type == 'hunter':
                    # Hunters might start with zero velocity and follow logic in their own system
                    create_enemy_hunter(
                        world,
                        enemy_config,
                        pygame.Vector2(evt.position)
                    )
                evt.triggered = True
