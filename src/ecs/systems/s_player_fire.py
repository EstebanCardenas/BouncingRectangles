from src.config import BulletConfig
from src.ecs.components.tags import CTagBullet, CTagPlayer
from src.ecs.components import CSurface, CTransform
from src.create.prefab_creator import create_bullet_square
import esper
import pygame

def system_player_fire(
    world: esper.World,
    click_pos: tuple[int, int],
    bullet_limit: int,
    bullet_config: BulletConfig,
):
    # Check for bullet limit before firing
    bullet_components = world.get_components(CTagBullet)
    if len(bullet_components) == bullet_limit:
        return

    # Fire bullet if limit has not been reached yet
    player_components = world.get_components(CTagPlayer, CTransform, CSurface)
    for _, (tag, transform, surface) in player_components:
        # Calculate player center
        player_center = pygame.Vector2(
            transform.pos.x + surface.surf.get_width() / 2,
            transform.pos.y + surface.surf.get_height() / 2
        )
        # Mouse target position
        target_pos = pygame.Vector2(click_pos[0], click_pos[1])
        
        # Calculate direction and normalize it
        direction = target_pos - player_center
        if direction.length() > 0:
            direction = direction.normalize()
        
        # Use bullet configuration velocity
        bullet_speed = bullet_config.velocity
        bullet_vel = direction * bullet_speed
        
        # Position the bullet at player's center
        bullet_start_pos = pygame.Vector2(player_center.x, player_center.y)
        
        create_bullet_square(world, bullet_start_pos, bullet_vel, bullet_config)
