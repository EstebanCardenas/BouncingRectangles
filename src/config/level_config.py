import json

class LevelEvent:
    def __init__(self, time: float, enemy_type: str, position: dict) -> None:
        self.time = time
        self.enemy_type = enemy_type
        self.position = (position['x'], position['y'])
        self.triggered = False

class LevelConfig:
    def __init__(self) -> None:
        self.events: list[LevelEvent] = []

    def load_config(self, config_path: str):
        with open(config_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        events_data = data['enemy_spawn_events']
        self.events = [
            LevelEvent(e['time'], e['enemy_type'], e['position'])
            for e in events_data
        ]
        # Ensure events are sorted by time for efficient processing
        self.events.sort(key=lambda x: x.time)
