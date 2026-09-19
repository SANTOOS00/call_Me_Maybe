class Call_Error(Exception):
    """Attributes:
        message: The human-readable error description.
        string: The formatted error message.
    """

    string: str = ""

    def __init__(self, message: str) -> None:
        """Initialize a Call_Error exception.

        Args:
            message: Human-readable description of the error.
        """
        self.message = message
        self.string = self.format_message(message)
        super().__init__(self.string)

    def format_message(self, message: str) -> str:
        """Format an error message.

        Args:
            message: Human-readable description of the error.

        Returns:
            The formatted error message.
        """
        return f"[Call_Error] {message}"
