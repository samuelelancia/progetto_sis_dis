import json
import time
import random
import zmq

class BaseSensor:
    
    #i sensori hanno un id, e una posizione
    def __init__(self, sensor_id, position_id, interval=1):
        self.sensor_id=sensor_id
        self.position_id=position_id
        self.interval=interval
    
    #funzione definita nelle sottoclassi
    def simulate(self):
        raise NotImplementedError

    #simulo una fault inviando un messaggio specifico
    def check_fault(self):
        # 5% probabilità di fault
        if random.random() < 0.05:
            return "fault"
        return None
    
    #comportamento del sensore
    def run(self):
        
        #avvio la connessione con zmq
        context=zmq.Context()
        socket=context.socket(zmq.PUB)
        socket.connect("tcp://localhost:5556")
        
        while True:
            
            if random.random() < 0.05:
                print("Sensore",self.sensor_id,": morto per 3 secondi")
                time.sleep(3)
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
            if random.random() < 0.05:
                payload = {
                    "sensor_id": self.sensor_id,
                    "type": "corrupt"
                }
             
            #invio il messaggio e sleep di un secondo
            socket.send_string(json.dumps(payload))
            time.sleep(self.interval)