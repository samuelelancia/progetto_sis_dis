import zmq
import json

class Collector:
    def __init__(self):
        context = zmq.Context()
        self.socket = context.socket(zmq.SUB)
        self.socket.bind("tcp://localhost:5556")
        self.socket.setsockopt_string(zmq.SUBSCRIBE, "") #niente topic perche' voglio ricevere tutti i messaggi
    
    def receive(self):
        raw = self.socket.recv_string()
        return json.loads(raw)