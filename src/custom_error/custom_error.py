from typing import Dict


class Call_Error(Exception):
    string = ""

    def __init__(self, message: str, **context: str) -> None:
        super().__init__(self.format_message(message, context))

    def format_message(self, message: str, context: Dict[str, str]) -> str:
        return f"{message} {context}"
