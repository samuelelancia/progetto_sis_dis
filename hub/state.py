#memorizza lo stato
class State:
    def __init__(self):
        self.traffic = {}   # segment_id → ultimo valore
        self.air = {}       # intersection_id → ultimo valore

    def update(self, msg):
        if msg["type"] == "traffic":
            self.traffic[msg["location"]] = msg
        elif msg["type"] == "air_quality":
            self.air[msg["location"]] = msg