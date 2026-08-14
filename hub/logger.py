import json
import time

class Logger:

    def __init__(self, fault_file="logs/fault.log", data_file="logs/data.log"):
        self.fault_file = fault_file
        self.data_file = data_file

    def log_fault(self, timestamp, sensor_id, state, count):
        entry = {
            "timestamp": timestamp,
            "sensor_id": sensor_id,
            "state": state,
            "number_of_faults": count
        }
        with open(self.fault_file, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def log_data(self, msg):
        entry = {
            "data": msg
        }
        with open(self.data_file, "a") as f:
            f.write(json.dumps(entry) + "\n")