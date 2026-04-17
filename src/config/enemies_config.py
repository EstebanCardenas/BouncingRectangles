import json
from src.config.player_config import AnimationData, AnimationsInfo

class Enemy:
    def __init__(self, enemy_type: str):
        self.enemy_type = enemy_type

class AsteroidData(Enemy):
    def __init__(self, img: str, velocity_min: float, velocity_max: float) -> None:
        super().__init__('asteroid')
        self.img = img
        self.velocity_min = velocity_min
        self.velocity_max = velocity_max

class HunterData(Enemy):
    def __init__(self, img: str, animations: AnimationsInfo, v_chase: int, v_return: int, d_chase: int, d_return: int) -> None:
        super().__init__('hunter')
        self.img = img
        self.animations = animations
        self.velocity_chase = v_chase
        self.velocity_return = v_return
        self.distance_start_chase = d_chase
        self.distance_start_return = d_return

class EnemiesConfig:
    def __init__(self) -> None:
        self.enemies: dict[str, Enemy] = {}

    def load_config(self, config_path: str):
        with open(config_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        for enemy_name, enemy_info in data.items():
            if enemy_name == 'Hunter':
                # Process Hunter
                anim_data = enemy_info['animations']
                animations_list = [
                    AnimationData(a['name'], a['start'], a['end'], a['framerate'])
                    for a in anim_data['list']
                ]
                animations = AnimationsInfo(anim_data['number_frames'], animations_list)
                self.enemies[enemy_name] = HunterData(
                    enemy_info['image'],
                    animations,
                    enemy_info['velocity_chase'],
                    enemy_info['velocity_return'],
                    enemy_info['distance_start_chase'],
                    enemy_info['distance_start_return']
                )
            elif enemy_name.startswith('Asteroid'):
                # Process Asteroid
                self.enemies[enemy_name] = AsteroidData(
                    enemy_info['image'],
                    enemy_info['velocity_min'],
                    enemy_info['velocity_max']
                )

