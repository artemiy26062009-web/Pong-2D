import json
from config import ACHIEVEMENTS_FILE, ACHIEVEMENTS_LIST


class Achievements:
    def __init__(self):
        self.data = {k: False for k in ACHIEVEMENTS_LIST}
        self.load()

    def load(self):
        try:
            with open(ACHIEVEMENTS_FILE, "r") as f:
                saved = json.load(f)
                for k in saved:
                    if k in self.data: self.data[k] = saved[k]
        except:
            pass

    def save(self):
        try:
            with open(ACHIEVEMENTS_FILE, "w") as f:
                json.dump(self.data, f)
        except:
            pass

    def unlock(self, name):
        if name in self.data and not self.data[name]:
            self.data[name] = True;
            self.save();
            return True
        return False

    def get_all(self):
        return [(n, ACHIEVEMENTS_LIST[n], self.data.get(n, False)) for n in ACHIEVEMENTS_LIST]