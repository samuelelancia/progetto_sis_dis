import time
import json

#gestisce i fault e i sensori morti
class FaultManager:

    def __init__(self):
        
        # dizionario per ultimo timestamp in cui ho visto ogni sensore
        self.last_seen = {}
        
        # stato dei sensori: ok, fault, offline
        self.status = {}
        self.fault_count = {}
        
        with open("config/system.json") as f:
            cfg = json.load(f)
                        
        self.timeout = cfg["fault_manager_timeout"]

    def mark_seen(self, sensor_id):
        self.last_seen[sensor_id] = time.time()
        
        # se arriva un messaggio, il sensore NON è offline
        if self.status.get(sensor_id) == "offline":
            #cambio stato leggendo dal dizionario la chiave
            self.status[sensor_id] = "ok"

    #stato di fault
    def mark_fault(self, sensor_id):
        self.status[sensor_id] = "fault"
        self.fault_count[sensor_id] = self.fault_count.get(sensor_id, 0) + 1
        return self.fault_count.get(sensor_id, "unknown")

    def check_offline(self):
        now = time.time()
        offline = []

        #vedo la differenza tra i tempi
        for sensor_id, ts in self.last_seen.items():
            if (now - ts > self.timeout) and self.status[sensor_id]!="offline":
                self.status[sensor_id] = "offline"
                offline.append(sensor_id)

        return offline, now

    def check_fault(self, type, sensor_id):
        if type  == "fault":
            count=self.mark_fault(sensor_id)
            return count
        return False
