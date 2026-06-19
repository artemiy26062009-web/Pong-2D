class Stats:
    def __init__(self): self.reset()
    def reset(self):
        self.hits = 0; self.wall_hits = 0; self.goals_left = 0; self.goals_right = 0
        self.max_speed = 0; self.current_streak = 0; self.max_streak = 0; self.fastest_goal = 999
    def add_hit(self): self.hits += 1
    def add_wall_hit(self): self.wall_hits += 1
    def add_goal(self, side, t, spd):
        if side == "left": self.goals_left += 1; self.current_streak += 1; self.max_streak = max(self.max_streak, self.current_streak)
        else: self.goals_right += 1; self.current_streak = 0
        if t < self.fastest_goal: self.fastest_goal = t
        if spd > self.max_speed: self.max_speed = spd