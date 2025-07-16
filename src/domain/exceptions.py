
class TodoNotFoundError(Exception): 
    def __init__(self, message: str = "Todo not found"):
        self.message = message
        super().__init__(self.message)