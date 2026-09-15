from typing import Dict


class Call_Error(Exception):
    """Represent an application-level input or generation error."""

    string = ""

    def __init__(self, message: str, **context: str) -> None:
        """Initialize an error with a message and optional context.

        Args:
            message: Human-readable error description.
            **context: Additional context values for the error message.
        """
        super().__init__(self.format_message(message, context))

    def format_message(self, message: str, context: Dict[str, str]) -> str:
        """Format an error message with contextual values.

        Args:
            message: Human-readable error description.
            context: Additional context values.

        Returns:
            Formatted error text.
        """
        return f"{message} {context}"
