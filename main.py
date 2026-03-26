#!/usr/bin/python3
"""Función Main"""

from src.config import EngineConfig, LevelConfig, EnemiesConfig
from src.engine.game_engine import GameEngine

CONFIG_PATH = 'assets/cfg_0{}/window.json'
LEVEL_CONFIG_PATH = 'assets/cfg_0{}/level_01.json'
ENEMIES_CONFIG_PATH = 'assets/cfg_0{}/enemies.json'

CONFIG_NUM = 0

if __name__ == "__main__":
    # Load config
    engine_config = EngineConfig()
    engine_config.load_config(CONFIG_PATH.format(CONFIG_NUM))
    enemies_config = EnemiesConfig()
    enemies_config.load_config(ENEMIES_CONFIG_PATH.format(CONFIG_NUM))
    level_config = LevelConfig(enemies_config.enemies)
    level_config.load_config(LEVEL_CONFIG_PATH.format(CONFIG_NUM))

    # Run engine
    engine = GameEngine(engine_config, level_config)
    engine.run()
