import json

class EnemyData:
    def __init__(self, size: dict, color: dict, velocity_min: float, velocity_max: float) -> None:
        self.size = (size['x'], size['y'])
        self.color = (color['r'], color['g'], color['b'])
        self.velocity_min = velocity_min
        self.velocity_max = velocity_max

class EnemiesConfig:
    def __init__(self) -> None:
        self.enemies: dict[str, EnemyData] = {}

    def load_config(self, config_path: str):
        with open(config_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        for enemy_type, enemy_info in data.items():
            self.enemies[enemy_type] = EnemyData(
                enemy_info['size'],
                enemy_info['color'],
                enemy_info['velocity_min'],
                enemy_info['velocity_max']
            )
