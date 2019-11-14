class ExecuteException(Exception):
    def __init__(self, reason, message):
        self.reason = reason
        self.message = message