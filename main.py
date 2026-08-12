from hub.collector import Collector
from hub.validator import Validator
from hub.faultManager import FaultManager
from hub.state import State
from hub.aggregator import Aggregator
from hub.logger import Logger 
import time

#instanzio tutti gli oggetti
def main():
    collector = Collector()
    validator = Validator()
    faults = FaultManager()
    state = State()
    aggregator = Aggregator(state)
    logger = Logger()

    print("Nodo centrale avviato...")

    while True:
        msg = collector.receive()
        
        if not validator.validate(msg):
            print("Messaggio non valido:", msg)
            logger.log_fault( time.time() ,msg["sensor_id"],msg["type"])
            continue
        
        faults.mark_seen(msg["sensor_id"])
        
        if faults.check_fault(msg["type"], msg["sensor_id"]):
            print("Fault rilevata:", msg)
            logger.log_fault( time.time() ,msg["sensor_id"],msg["type"])
            continue

        state.update(msg)
        
        logger.log_data(msg)
        
        offline, ts=faults.check_offline()
        for offline_id in offline:
            logger.log_fault(ts, offline_id, "offline")

        summary = aggregator.get_summary()
        print("Stato aggiornato:", summary)

if __name__ == "__main__":
    main()
