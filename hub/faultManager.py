import time

#gestisce i fault e i sensori morti
class FaultManager:

    def __init__(self, timeout=2):
        
        # dizionario per ultimo timestamp in cui ho visto ogni sensore
        self.last_seen = {}
        
        # stato dei sensori: ok, fault, offline
        self.status = {}
        self.timeout = timeout

    def mark_seen(self, sensor_id):
        self.last_seen[sensor_id] = time.time()
        
        # se arriva un messaggio, il sensore NON è offline
        if self.status.get(sensor_id) == "offline":
            #cambio stato leggendo dal dizionario la chiave
            self.status[sensor_id] = "ok"

    #stato di fault
    def mark_fault(self, sensor_id):
        self.status[sensor_id] = "fault"

    def check_offline(self):
        now = time.time()
        offline = []

        #vedo la differenza tra i tempi
        for sensor_id, ts in self.last_seen.items():
            if now - ts > self.timeout:
                self.status[sensor_id] = "offline"
                offline.append(sensor_id)

        return offline, now

    def get_status(self, sensor_id):
        #unknown e' il risultato di default se non trovo la chiave
        return self.status.get(sensor_id, "unknown")
    
    def check_fault(self, type, sensor_id):
        if type  == "fault":
            self.mark_fault(sensor_id)
            return True
        return False
