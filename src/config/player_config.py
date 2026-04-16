import json

class AnimationData:
    def __init__(self, name: str, start: int, end: int, framerate: int) -> None:
        self.name = name
        self.start = start
        self.end = end
        self.framerate = 1.0 / framerate

class PlayerConfig:
    def __init__(self):
        self.image: str = ""
        self.number_frames: int = 1
        self.animations: list[AnimationData] = []
        self.input_velocity: float = 0.0

    def load_config(self, config_path: str):
        with open(config_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        self.image = data['image']
        self.input_velocity = data['input_velocity']
        
        anim_data = data['animations']
        self.number_frames = anim_data['number_frames']
        self.animations = [
            AnimationData(a['name'], a['start'], a['end'], a['framerate'])
            for a in anim_data['list']
        ]
