
class StoreExceptions(Exception):
    def __init__(self, message):
        self.message = message

class StoreNotFoundException(StoreExceptions):
    pass