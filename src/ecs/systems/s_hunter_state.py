from src.engine.service_locator import ServiceLocator
from src.ecs.components.c_hunter_state import CHunterState, HunterState
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_chase import CChase
from src.ecs.components.c_return import CReturn
from src.ecs.components import CVelocity, CTransform
from src.ecs.components.tags import CTagPlayer
import esper
import pygame

def system_hunter_state(
    world: esper.World,
):
    player_entities = world.get_components(CTagPlayer, CTransform)
    if not player_entities:
        return
    
    _, (_, p_t) = player_entities[0]

    components = world.get_components(CVelocity, CAnimation, CHunterState, CChase, CReturn, CTransform)
    for _, (c_v, c_a, c_hs, c_ch, c_ret, c_t) in components:
        distance = c_t.pos.distance_to(p_t.pos)
        if c_hs.hunter_state == HunterState.IDLE:
            _do_hunter_idle(c_v, c_a, c_hs, c_ch, distance)

        elif c_hs.hunter_state == HunterState.MOVE:
            _do_hunter_move(c_v, c_a, c_hs, c_ch, c_ret, p_t.pos, c_t.pos)

        elif c_hs.hunter_state == HunterState.RETURN:
            _do_hunter_return(c_v, c_a, c_hs, c_ret, c_t.pos)

def _do_hunter_idle(c_v: CVelocity, c_a: CAnimation, c_hs: CHunterState, c_ch: CChase, distance: float):
    _set_animation(c_a, 1)
    c_v.vel.x = 0
    c_v.vel.y = 0
    if distance <= c_ch.distance_start_chase:
        c_hs.hunter_state = HunterState.MOVE
        if c_ch.chase_sound != None: ServiceLocator.sounds_service.play(c_ch.chase_sound)

def _do_hunter_move(c_v: CVelocity, c_a: CAnimation, c_hs: CHunterState, c_ch: CChase, c_ret: CReturn, p_pos: pygame.Vector2, h_pos: pygame.Vector2):
    _set_animation(c_a, 0)
    c_v.vel = (p_pos - h_pos).normalize() * c_ch.velocity_chase
    
    dist_from_start = h_pos.distance_to(c_ret.start_point)
    if dist_from_start > c_ret.distance_start_return:
        c_hs.hunter_state = HunterState.RETURN

def _do_hunter_return(c_v: CVelocity, c_a: CAnimation, c_hs: CHunterState, c_ret: CReturn, h_pos: pygame.Vector2):
    _set_animation(c_a, 0)
    dist_to_start = h_pos.distance_to(c_ret.start_point)
    if dist_to_start < 2:
        c_v.vel.x = 0
        c_v.vel.y = 0
        c_hs.hunter_state = HunterState.IDLE
    else:
        c_v.vel = (c_ret.start_point - h_pos).normalize() * c_ret.velocity_return

def _set_animation(c_a: CAnimation, anim: int):
    if c_a.curr_anim == anim: return

    c_a.curr_anim = anim
    c_a.curr_anim_time = 0
    c_a.curr_frame = c_a.animations_list[c_a.curr_anim].start
