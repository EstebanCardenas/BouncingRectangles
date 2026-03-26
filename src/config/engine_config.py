import json

class EngineConfig:
    title: str
    size: tuple[int, int]
    bg_color: tuple[int, int, int]
    framerate: int

    def load_config(self, config_path: str):
        with open(config_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        config = data['window']
        if config == None:
            raise Exception('Config has no window object')
        self.title = config['title']
        self.size = (config['size']['w'], config['size']['h'])
        bg_color = config['bg_color']
        self.bg_color = (
            bg_color['r'], bg_color['g'], bg_color['b']
        )
        self.framerate = config['framerate']
