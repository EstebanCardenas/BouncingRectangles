#!/usr/bin/python3
"""Función Main"""

from src.config import EngineConfig, LevelConfig, EnemiesConfig
from src.engine.game_engine import GameEngine

CONFIG_PATH = 'assets/cfg/window.json'
LEVEL_CONFIG_PATH = 'assets/cfg/level_01.json'
ENEMIES_CONFIG_PATH = 'assets/cfg/enemies.json'

if __name__ == "__main__":
    # Load config
    engine_config = EngineConfig()
    engine_config.load_config(CONFIG_PATH)
    enemies_config = EnemiesConfig()
    enemies_config.load_config(ENEMIES_CONFIG_PATH)
    level_config = LevelConfig(enemies_config.enemies)
    level_config.load_config(LEVEL_CONFIG_PATH)

    # Run engine
    engine = GameEngine(engine_config, level_config)
    engine.run()
