from hub.collector import Collector
from hub.validator import Validator
from hub.faultManager import FaultManager
from hub.state import State
from hub.aggregator import Aggregator

#instanzio tutti gli oggetti
def main():
    collector = Collector()
    validator = Validator()
    faults = FaultManager()
    state = State()
    aggregator = Aggregator(state)

    print("Nodo centrale avviato...")

    while True:
        msg = collector.receive()
        
        faults.mark_seen(msg["sensor_id"])

        if not validator.validate(msg):
            print("Messaggio non valido:", msg)
            continue

        if faults.check_fault(msg["type"], msg["sensor_id"]):
            print("Fault rilevata:", msg)
            continue

        state.update(msg)
        
        offline=faults.check_offline()

        summary = aggregator.get_summary()
        print("Stato aggiornato:", summary)

if __name__ == "__main__":
    main()
