from hub.collector import Collector
from hub.validator import Validator
from hub.faultManager import FaultManager
from hub.state import State
from hub.aggregator import Aggregator

def main():
    collector = Collector()
    validator = Validator()
    faults = FaultManager()
    state = State()
    aggregator = Aggregator(state)

    print("Nodo centrale avviato...")

    while True:
        msg = collector.receive()

        if not validator.validate(msg):
            print("Messaggio non valido:", msg)
            continue

        faults.update(msg["sensor_id"])
        state.update(msg)

        offline = faults.check_offline()
        if offline:
            print("Sensori offline:", offline)

        summary = aggregator.get_summary()
        print("Stato aggiornato:", summary)

if __name__ == "__main__":
    main()
