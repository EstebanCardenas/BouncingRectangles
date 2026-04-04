import json

from src.config.enemies_config import EnemyData

class LevelEvent:
    def __init__(self, time: float, enemy_type: str, enemy_data: EnemyData, position: dict) -> None:
        self.time = time
        self.enemy_type = enemy_type
        self.enemy_data = enemy_data
        self.position = (position['x'], position['y'])
        self.triggered = False

class PlayerSpawn:
    def __init__(self, position: dict[str, int]) -> None:
        self.position = (position['x'], position['y'])

class LevelConfig:
    def __init__(self, enemies: dict[str, EnemyData]) -> None:
        self.events: list[LevelEvent] = []
        self.enemies = enemies
        self.player_spawn: PlayerSpawn = None

    def load_config(self, config_path: str):
        with open(config_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Load player spawn
        self.player_spawn = PlayerSpawn(data['player_spawn']['position'])
        
        events_data = data['enemy_spawn_events']
        self.events = [
            LevelEvent(e['time'], e['enemy_type'], self.enemies[e['enemy_type']], e['position'])
            for e in events_data
        ]
        # Ensure events are sorted by time for efficient processing
        self.events.sort(key=lambda x: x.time)
