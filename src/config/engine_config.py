import json

class EngineConfig:
    title: str
    size: tuple[int, int]
    bg_color: tuple[int, int, int]
    framerate: int

    def load_config(self, config_path: str):
        with open(config_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        self.title = data['title']
        self.size = (data['size']['w'], data['size']['h'])
        bg_color = data['bg_color']
        self.bg_color = (
            bg_color['r'], bg_color['g'], bg_color['b']
        )
        self.framerate = data['framerate']
