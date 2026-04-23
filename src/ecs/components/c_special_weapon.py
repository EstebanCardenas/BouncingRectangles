class CSpecialWeapon:
    def __init__(self, cooldown: float):
        self.cooldown = cooldown
        self.time_until_next_fire = 0.0
