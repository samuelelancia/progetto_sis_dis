import json
import time
import random
import zmq

class BaseSensor:
    
    #i sensori hanno un id, e una posizione
    def __init__(self, sensor_id, position_id):
        self.sensor_id=sensor_id
        self.position_id=position_id
        
        with open("config/system.json") as f:
                cfg = json.load(f)
                    
        self.interval=cfg["sensor_interval"]
        self.fault_chance = cfg["fault_chance"]
        self.death_chance = cfg["death_chance"]
        self.corrupt_chance = cfg["corrupt_chance"]
        self.death_time = cfg["death_time"]
    
    #funzione definita nelle sottoclassi
    def simulate(self):
        raise NotImplementedError

    #simulo una fault inviando un messaggio specifico
    def check_fault(self):
        # 5% probabilità di fault
        if random.random() < self.fault_chance:
            return "fault"
        return None
    
    #comportamento del sensore
    def run(self):
        
        #avvio la connessione con zmq
        context=zmq.Context()
        socket=context.socket(zmq.PUB)
        socket.connect("tcp://localhost:5556")
        
        while True:
            
            if random.random() < self.death_chance:
                print("Sensore",self.sensor_id,": morto per ",self.death_time," secondi")
                time.sleep(self.death_time)
                continue
            
            #controllo fault
            fault=self.check_fault()
            if fault:
                payload = {
                    "sensor_id": self.sensor_id,
                    "segment": self.position_id,
                    "timestamp": time.time(),
                    "location": self.position_id,
                    #aggiungo al payload
                    "type": fault
                }
            else:
                #altrimenti comportamento normale
                payload=self.simulate()
              
            #messaggio corrotto
            if random.random() < self.corrupt_chance:
                payload = {
                    "sensor_id": self.sensor_id,
                    "type": "corrupt"
                }
             
            #invio il messaggio e sleep di un secondo
            socket.send_string(json.dumps(payload))
            time.sleep(self.interval)