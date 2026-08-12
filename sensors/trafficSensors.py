from sensors.baseSensors import BaseSensor
import time
import random

class TrafficSensor(BaseSensor):
    
    # Velocità media: 20–35 km/h sulle strade urbane comuni; scende a 10–15 km/h nelle ore di punta o in centro. 
    # Deviazione standard: 6–10 km/h se la strada è scorrevole; può aumentare molto (fino a 15 km/h o più) se vi 
    # sono semafori, code improvvise o comportamenti di guida molto disomogenei.
    
    def simulate(self):
        return {
            "sensor_id": self.sensor_id,
            "segment": self.position_id,
            "timestamp": time.time(),
            "type": "traffic",
            "vehicles_per_min": random.randint(0, 30),
            "avg_speed": random.randint(10, 40)
        }