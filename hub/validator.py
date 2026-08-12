class Validator:
    #campi minimi del messaggio
    REQUIRED_FIELDS = ["sensor_id", "location", "timestamp", "type"]

    def validate(self, msg):
        for field in self.REQUIRED_FIELDS:
            if field not in msg:
                return False
        return True
