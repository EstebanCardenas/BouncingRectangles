from src.config.player_config import AnimationData

class CAnimation:
    def __init__(self, number_frames:int, animations: list[AnimationData]):
        self.number_frames = number_frames
        self.animations_list = animations
        self.curr_anim = 0
        self.curr_anim_time = 0
        self.curr_frame = self.animations_list[self.curr_anim].start
