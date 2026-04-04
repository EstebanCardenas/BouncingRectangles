import json

class PlayerConfig:
    def __init__(self):
        self.size: tuple[int, int] = (0, 0)
        self.color: tuple[int, int, int] = (0, 0, 0)
        self.input_velocity: float = 0.0

    def load_config(self, config_path: str):
        with open(config_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        self.size = (data['size']['x'], data['size']['y'])
        self.color = (data['color']['r'], data['color']['g'], data['color']['b'])
        self.input_velocity = data['input_velocity']
