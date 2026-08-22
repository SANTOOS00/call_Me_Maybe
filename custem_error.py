from typing import Dict


class CallError(Exception):
    _line_number: int = 0

    def __init__(self, message: str, **context: str) -> None:
        super().__init__(self.format_message(message, context))
        self.context: Dict[str, str] = context

    def format_message(
        self,
        message: str,
        context: Dict[str, str]
    ) -> str:
        if not context:
            return message

        labels = {
            "line_number": "line",
            "type_error": "type",
        }
        details = "; ".join(
            f"{labels.get(key, key)}: {value}"
            for key, value in context.items()
        )
        return f"{message} ({details})"

    @classmethod
    def add_line_number(cls) -> None:
        cls._line_number += 1

    @classmethod
    def get_number_line(cls) -> str:
        return str(cls._line_number)
