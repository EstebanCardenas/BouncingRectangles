import json
from src.config.enemies_config import EnemiesConfig
from src.config.level_config import LevelConfig
from src.config.player_config import PlayerConfig
from src.config.bullet_config import BulletConfig

class EngineConfig:
    def __init__(self) -> None:
        self.title: str
        self.size: tuple[int, int]
        self.bg_color: tuple[int, int, int]
        self.framerate: int
        self.bg_track_path: str
        self.enemies_config: EnemiesConfig = EnemiesConfig()
        self.player_config: PlayerConfig = PlayerConfig()
        self.level_config: LevelConfig = None
        self.bullet_config: BulletConfig = BulletConfig()

    def load_config(self, config_dir: str):
        # Window config
        with open(f"{config_dir}/window.json", 'r', encoding='utf-8') as file:
            data = json.load(file)
        self.title = data['title']
        self.size = (data['size']['w'], data['size']['h'])
        bg_color = data['bg_color']
        self.bg_color = (
            bg_color['r'], bg_color['g'], bg_color['b']
        )
        self.framerate = data['framerate']

        # Compose and load other configs
        self.enemies_config.load_config(f"{config_dir}/enemies.json")
        self.level_config = LevelConfig(self.enemies_config.enemies)
        self.level_config.load_config(f"{config_dir}/level_01.json")
        self.player_config.load_config(f"{config_dir}/player.json")
        self.bullet_config.load_config(f"{config_dir}/bullet.json")
