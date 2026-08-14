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
        #arriva il messaggio
        msg = collector.receive()
        
        #controllo se e' valido
        if not validator.validate(msg):
            print("Messaggio non valido:", msg)
            logger.log_corrupt_offline( time.time() ,msg["sensor_id"],msg["type"])
            continue
        
        #aggiorno last seen
        faults.mark_seen(msg["sensor_id"])
        
        #controllo fault
        fault_count=faults.check_fault(msg["type"], msg["sensor_id"])
        if fault_count:
            print("Fault rilevata:", msg)
            logger.log_fault( time.time() ,msg["sensor_id"], msg["type"], fault_count)
            continue

        #aggiorno gli ultimi messaggi visti
        state.update(msg)
        
        #efettuo log dei dati
        logger.log_data(msg)
        
        #controllo sensori offline
        offline, ts=faults.check_offline()
        for offline_id in offline:
            logger.log_corrupt_offline(ts, offline_id, "offline")

        #stampo ultimi messaggi visti
        summary = aggregator.get_summary()
        print("Stato aggiornato:", summary)

if __name__ == "__main__":
    main()
