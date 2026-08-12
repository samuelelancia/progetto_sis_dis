import time

class FaultManager:
    def __init__(self):
        self.last_seen = {}

    def update(self, sensor_id):
        self.last_seen[sensor_id] = time.time()

    def check_offline(self, timeout=5):
        offline = []
        now = time.time()
        for sensor_id, ts in self.last_seen.items():
            if now - ts > timeout:
                offline.append(sensor_id)
        return offline