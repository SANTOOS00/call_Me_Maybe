
class Call_Error(Exception):
    def __init__(self, message, context: str) -> None:
        super().__init__(self.format_message(message, context))

    def format_message(self, message, context) -> str:
        return message
