import json
import time
import random
import zmq

class BaseSensor:
    def __init__(self, sensor_id, position_id, interval=1):
        self.sensor_id=sensor_id
        self.position_id=position_id
        self.interval=interval
        
    def simulate(self):
        raise NotImplementedError

    def check_fault(self):
        # 5% probabilità di fault
        if random.random() < 0.05:
            return {"fault": True, "error": "Simulated sensor failure"}
        return None
    
    def run(self):
        context=zmq.Context()
        socket=context.socket(zmq.PUB)
        socket.connect("tcp://localhost:5556")
        
        while True:
            fault=self.check_fault
            if fault:
                payload = {
                    "sensor_id": self.sensor_id,
                    "segment": self.position_id,
                    "timestamp": time.time(),
                    "fault": fault
                }
            else:
                payload=self.simulate()
             
            socket.send_string(json.dumps(payload))
            time.sleep(self.interval)