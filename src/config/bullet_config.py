import json

class BulletConfig:
    def __init__(self) -> None:
        self.img = ""
        self.velocity: float = 0.0

    def load_config(self, config_path: str):
        with open(config_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        self.img = data['image']
        self.velocity = data['velocity']
