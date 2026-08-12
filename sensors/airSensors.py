from sensors.baseSensors import BaseSensor
import time
import random

class AirSensor(BaseSensor):
    def simulate(self):
            return {
                "sensor_id": self.sensor_id,
                "segment": self.position_id,
                "timestamp": time.time(),
                "type": "air",
                #Soglia di attenzione: Tra 1.000 e 1.500 ppm (aria viziata, calo di attenzione)
                "co2": random.uniform(1000, 1500),
                
                #Media annuale limite a 40 μg/m³ (in transizione verso i 20 μg/m³).
                "pm10": random.uniform(25, 35),
                
                #Media annuale limite a 25 μg/m³ (in riduzione a 10 μg/m³)
                "pm2_5": random.uniform(10, 20)
            }