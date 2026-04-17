from src.config.player_config import AnimationsInfo

class CAnimation:
    def __init__(self, animations: AnimationsInfo):
        self.number_frames = animations.number_frames
        self.animations_list = animations.list
        self.curr_anim = 0
        self.curr_anim_time = 0
        self.curr_frame = self.animations_list[self.curr_anim].start
        self.completed_once = False
