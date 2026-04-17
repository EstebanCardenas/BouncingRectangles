from enum import Enum

class CHunterState():
    def __init__(self):
        self.hunter_state = HunterState.IDLE

class HunterState(Enum):
    IDLE = 0
    MOVE = 1
    RETURN = 2
