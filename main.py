#!/usr/bin/python3
"""Función Main"""

from src.engine.engine_config import EngineConfig
from src.engine.game_engine import GameEngine

CONFIG_PATH = 'assets/cfg/window.json'

if __name__ == "__main__":
    engine_config = EngineConfig()
    engine_config.load_config(CONFIG_PATH)
    engine = GameEngine(engine_config)
    engine.run()
