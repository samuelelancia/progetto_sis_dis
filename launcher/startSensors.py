import json
from threading import Thread
from sensors.trafficSensors import TrafficSensor
from sensors.airSensors import AirSensor

#carico la mappa salvata nel json
def load_map():
    with open("config/map.json") as f:
        return json.load(f)
    
def start_sensors():
    
    map = load_map()
    threads = []
    id=1
    
    #sensori traffico: uno per ogni segmento
    for segment in map["segments"]:
        seg_id = segment["id"]
        sensor_id = i
        i=1+1
        sensor = TrafficSensor(sensor_id, seg_id)

        t = Thread(target=sensor.run)
        t.start()
        threads.append(t)
        
    #sensori aria:uno per ogni incorcio
    for intersection in map["intersections"]:
        int_id = intersection["id"]
        sensor_id = i
        i=1+1
        sensor = TrafficSensor(sensor_id, int_id)

        t = Thread(target=sensor.run)
        t.start()
        threads.append(t)
        
    for t in threads:
        t.join()


if __name__ == "__main__":
    start_sensors()
        