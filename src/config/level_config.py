import json

from src.config.enemies_config import Enemy

class LevelEvent:
    def __init__(self, time: float, enemy_type: str, enemy_data: Enemy, position: dict) -> None:
        self.time = time
        self.enemy_type = enemy_type
        self.enemy_data = enemy_data
        self.position = (position['x'], position['y'])
        self.triggered = False

class PlayerSpawn:
    def __init__(self, position: dict[str, int], max_bullets: int) -> None:
        self.position = (position['x'], position['y'])
        self.max_bullets = max_bullets

class LevelConfig:
    def __init__(self, enemies: dict[str, Enemy]) -> None:
        self.events: list[LevelEvent] = []
        self.enemies = enemies
        self.player_spawn: PlayerSpawn = None

    def load_config(self, config_path: str):
        with open(config_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Load player spawn
        self.player_spawn = PlayerSpawn(
            data['player_spawn']['position'],
            data['player_spawn']['max_bullets']
        )
        
        events_data = data['enemy_spawn_events']
        self.events = [
            LevelEvent(e['time'], e['enemy_type'], self.enemies[e['enemy_type']], e['position'])
            for e in events_data
        ]
        # Ensure events are sorted by time for efficient processing
        self.events.sort(key=lambda x: x.time)
