#presenta lo stato
class Aggregator:
    def __init__(self, state):
        self.state = state

    def get_summary(self):
        return {
            "traffic": self.state.traffic,
            "air_quality": self.state.air
        }