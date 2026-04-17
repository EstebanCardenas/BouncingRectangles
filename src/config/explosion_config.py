import json
from src.config.player_config import AnimationData, AnimationsInfo

class ExplosionConfig:
    def __init__(self) -> None:
        self.image: str = ""
        self.animations: AnimationsInfo = None

    def load_config(self, config_path: str):
        with open(config_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        self.image = data['image']
        
        anim_data = data['animations']
        animations_list = [
            AnimationData(a['name'], a['start'], a['end'], a['framerate'])
            for a in anim_data['list']
        ]
        self.animations = AnimationsInfo(anim_data['number_frames'], animations_list)
