class ConditionException(Exception):
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg

class ExecuteException(Exception):
    def __init__(self, reason, message):
        self.reason = reason
        self.message = message
