from src.ecs.components import CSpecialWeapon, CSurface
from src.ecs.components.tags import CTagCooldownText
from src.engine.service_locator import ServiceLocator
import pygame
import esper

def system_update_cooldown_text(world: esper.World, font_path: str):
    player_components = world.get_component(CSpecialWeapon)
    if not player_components: return
    _, c_sw = player_components[0]
    
    # Calculate percentage
    # If time_until_next_fire is 0, it's 100%
    # If time_until_next_fire is c_sw.cooldown, it's 0%
    percentage = max(0, 100 * (1 - c_sw.time_until_next_fire / c_sw.cooldown))
    
    text = f"{int(percentage)}%"
    color = pygame.Color(255, 0, 0) if percentage < 100 else pygame.Color(0, 255, 0)
    
    # Update the text surface
    text_entities = world.get_components(CSurface, CTagCooldownText)
    for _, (c_s, _) in text_entities:
        font = ServiceLocator.fonts_service.get(font_path, 8)
        c_s.surf = font.render(text, True, color)
        c_s.area = c_s.surf.get_rect()
