#!/usr/bin/python3
"""Función Main"""

from src.config import EngineConfig, LevelConfig, EnemiesConfig, PlayerConfig
from src.engine.game_engine import GameEngine

BASE_CONFIG_PATH = 'assets/cfg_0{}'
CONFIG_NUM = 0

if __name__ == "__main__":
    # Load config
    engine_config = EngineConfig()
    engine_config.load_config(BASE_CONFIG_PATH.format(CONFIG_NUM))

    # Run engine
    engine = GameEngine(engine_config)
    engine.run()
