from enum import Enum

class CPlayerState():
    def __init__(self):
        self.player_state = PlayerState.IDLE

class PlayerState(Enum):
    IDLE = 0
    MOVE = 1
