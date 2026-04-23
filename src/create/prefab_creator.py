from src.ecs.components.tags.c_tag_special_bullet import CTagSpecialBullet
from src.engine.service_locator import ServiceLocator
from src.ecs.components.c_hunter_state import CHunterState
from src.ecs.components.c_return import CReturn
from src.ecs.components.c_chase import CChase
from src.ecs.components.tags.c_tag_hunter import CTagHunter
from src.ecs.components.c_player_state import CPlayerState
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_background_track import CBackgroundTrack
import pygame
from src.ecs.components.tags import CTagPlayer, CTagEnemy, CTagBullet, CTagExplosion, CTagCooldownText
import esper
import pygame

from src.ecs.components import CSurface, CTransform, CVelocity, CLifetime, CSpecialWeapon, CEnemySpawner, CInputCommand
from src.config import LevelEvent, PlayerConfig, PlayerSpawn, BulletConfig, HunterData, ExplosionConfig
from src.engine.service_locator import ServiceLocator


def create_player_square(
    world: esper.World,
    player_config: PlayerConfig,
    player_spawn: PlayerSpawn,
) -> int:
    player_surface = ServiceLocator.images_service.get(player_config.image)
    size = player_surface.size
    size = (size[0] / player_config.animations.number_frames, size[1])
    pos = pygame.Vector2(
        player_spawn.position[0] - (size[0] / 2),
        player_spawn.position[1] - (size[1] / 2),
    )
    vel = pygame.Vector2(0, 0)
    entity = create_sprite(world, pos, vel, player_surface)
    world.add_component(entity, CTagPlayer())
    world.add_component(entity, CAnimation(player_config.animations))
    world.add_component(entity, CPlayerState())
    world.add_component(entity, CSpecialWeapon(2.5))
    return entity


def create_sprite(
    world: esper.World,
    pos: pygame.Vector2,
    vel: pygame.Vector2,
    surface: pygame.Surface,
) -> int:
    entity = world.create_entity()
    world.add_component(entity, CTransform(pos))
    world.add_component(entity, CVelocity(vel))
    world.add_component(entity, CSurface.from_surface(surface))
    return entity


def create_enemy_square(
    world: esper.World,
    img: str,
    pos: pygame.Vector2,
    vel: pygame.Vector2,
    sound: str,
):
    enemy_surface = ServiceLocator.images_service.get(img)
    entity = create_sprite(world, pos, vel, enemy_surface)
    world.add_component(entity, CTagEnemy())
    ServiceLocator.sounds_service.play(sound)


def create_enemy_hunter(
    world: esper.World,
    hunter_config: HunterData,
    pos: pygame.Vector2,
):
    hunter_surface = ServiceLocator.images_service.get(hunter_config.img)
    size = hunter_surface.get_size()
    size = (size[0] / hunter_config.animations.number_frames, size[1])
    # Center the hunter on the spawn position
    adj_pos = pygame.Vector2(pos.x - size[0] / 2, pos.y - size[1] / 2)
    vel = pygame.Vector2(0, 0)
    entity = create_sprite(world, adj_pos, vel, hunter_surface)
    world.add_component(entity, CTagHunter())
    world.add_component(entity, CChase(
        hunter_config.velocity_chase,
        hunter_config.distance_start_chase,
        hunter_config.chase_sound,
    ))
    world.add_component(entity, CReturn(
        hunter_config.velocity_return,
        hunter_config.distance_start_return,
        adj_pos.copy(),
    ))

    world.add_component(entity, CAnimation(hunter_config.animations))
    world.add_component(entity, CHunterState())


def create_bullet_square(
    world: esper.World,
    pos: pygame.Vector2,
    vel: pygame.Vector2,
    bullet_config: BulletConfig
):
    bullet_surface = ServiceLocator.images_service.get(bullet_config.img)
    bullet_size = bullet_surface.size
    # Correct the position so that the given position is the center of the bullet
    adj_pos = pygame.Vector2(
        pos.x - bullet_size[0] / 2, pos.y - bullet_size[1] / 2)
    entity = create_sprite(
        world, adj_pos, vel, bullet_surface,
    )
    world.add_component(entity, CTagBullet())
    ServiceLocator.sounds_service.play(bullet_config.sound)


def create_special_fire(
    world: esper.World,
    pos: pygame.Vector2,
    vel: pygame.Vector2,
    bullet_config: BulletConfig,
) -> int:
    surf = ServiceLocator.images_service.get(bullet_config.img)
    entity = create_sprite(world, pos, vel, surf)
    world.add_component(entity, CTagSpecialBullet())
    world.add_component(entity, CLifetime(0.7))
    ServiceLocator.sounds_service.play(bullet_config.sound)
    return entity


def create_explosion(
    world: esper.World,
    pos: pygame.Vector2,
    explosion_config: ExplosionConfig,
):
    explosion_surface = ServiceLocator.images_service.get(
        explosion_config.image)
    size = explosion_surface.get_size()
    size = (size[0] / explosion_config.animations.number_frames, size[1])
    vel = pygame.Vector2(0, 0)
    entity = create_sprite(world, pos, vel, explosion_surface)
    world.add_component(entity, CTagExplosion())
    world.add_component(entity, CAnimation(explosion_config.animations))
    ServiceLocator.sounds_service.play(explosion_config.sound)


def create_square(
    world: esper.World,
    size: pygame.Vector2,
    color: pygame.Color,
    pos: pygame.Vector2,
    vel: pygame.Vector2,
) -> int:
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
    return cuad_entity


def create_enemy_spawner(
    world: esper.World,
    events: list[LevelEvent],
):
    spawner_entity = world.create_entity()
    world.add_component(
        spawner_entity,
        CEnemySpawner(events),
    )


def create_player_input(world: esper.World):
    input_left = world.create_entity()
    input_right = world.create_entity()
    input_up = world.create_entity()
    input_down = world.create_entity()
    input_click = world.create_entity()
    input_special = world.create_entity()
    input_pause = world.create_entity()
    world.add_component(
        input_left,
        CInputCommand(
            "PLAYER_LEFT",
            pygame.K_LEFT,
        )
    )
    world.add_component(
        input_right,
        CInputCommand(
            "PLAYER_RIGHT",
            pygame.K_RIGHT,
        )
    )
    world.add_component(
        input_up,
        CInputCommand(
            "PLAYER_UP",
            pygame.K_UP,
        )
    )
    world.add_component(
        input_down,
        CInputCommand(
            "PLAYER_DOWN",
            pygame.K_DOWN,
        )
    )
    world.add_component(
        input_click,
        CInputCommand(
            "PLAYER_FIRE",
            pygame.BUTTON_LEFT,
        )
    )
    world.add_component(
        input_special,
        CInputCommand(
            "PLAYER_SPECIAL",
            pygame.BUTTON_RIGHT,
        )
    )
    world.add_component(
        input_pause,
        CInputCommand(
            "GAME_PAUSE",
            pygame.K_p,
        )
    )


def create_text(
    world: esper.World,
    text: str,
    font_path: str,
    font_size: int,
    color: pygame.Color,
    pos: tuple[int, int],
) -> int:
    entity = world.create_entity()
    font = ServiceLocator.fonts_service.get(font_path, font_size)
    surf = font.render(text, True, color)
    world.add_component(entity, CSurface.from_surface(surf))
    world.add_component(entity, CTransform(pygame.Vector2(pos[0], pos[1])))
    return entity


def create_cooldown_text(
    world: esper.World,
    text: str,
    font_path: str,
    font_size: int,
    color: pygame.Color,
    pos: tuple[int, int],
) -> int:
    entity = create_text(world, text, font_path, font_size, color, pos)
    world.add_component(entity, CTagCooldownText())
    return entity


def create_bg_track(world: esper.World, track_path: str):
    entity = world.create_entity()
    world.add_component(entity, CBackgroundTrack(track_path))
