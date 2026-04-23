#!/usr/bin/python3
"""Función Main"""

from src.config import EngineConfig, LevelConfig, EnemiesConfig, PlayerConfig
from src.engine.game_engine import GameEngine
import asyncio

from pathlib import Path
import os

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent

BASE_CONFIG_PATH = str(PROJECT_ROOT / 'assets' / 'cfg_0{}')
CONFIG_NUM = 0

BG_TRACK_PATH = str(PROJECT_ROOT / 'assets' / 'snd' / 'crossing-the-rubicon.ogg')
FONT_PATH = str(PROJECT_ROOT / 'assets' / 'fnt' / 'PressStart2P.ttf')

async def main():
    # Load config
    engine_config = EngineConfig()
    # We pass the formatted path
    engine_config.load_config(BASE_CONFIG_PATH.format(CONFIG_NUM))
    engine_config.bg_track_path = BG_TRACK_PATH
    engine_config.font_path = FONT_PATH

    # Run engine
    engine = GameEngine(engine_config)
    await engine.run()

if __name__ == "__main__":
    asyncio.run(main())
