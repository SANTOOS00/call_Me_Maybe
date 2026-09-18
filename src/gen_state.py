from hmac import new

from .stats_enum import StateGenString, StateGenNumber
from .model import Model


class GenState:
    """Track and manage generation states for numeric and string generation.

    Attributes:
        model: The language model instance.
    """

    def __init__(self, model: Model) -> None:
        """Initialize the state generator.

        Args:
            model: The language model instance.
        """
        self.model: Model = model

    def set_state_number(
        self, current_gen: str, current_state: StateGenNumber
    ) -> StateGenNumber:
        """Update state machine for numeric generation.

        Args:
            current_gen: The currently generated string.
            current_state: The current state in the state machine.

        Returns:
            The next state based on the generated content.
        """
        if not current_gen:
            return StateGenNumber.START

        for c in current_gen:
            match current_state:
                case StateGenNumber.START:
                    if c in "+-":
                        return StateGenNumber.SIGN
                    elif c in "0123456789":
                        return StateGenNumber.INTEGER
                case StateGenNumber.SIGN:
                    return StateGenNumber.INTEGER
                case StateGenNumber.INTEGER:
                    if c == ".":
                        return StateGenNumber.DECIMAL
                    elif c == ",":
                        return StateGenNumber.END
                case StateGenNumber.DECIMAL:
                    if c == ",":
                        return StateGenNumber.END
                case StateGenNumber.END:
                    return StateGenNumber.END
        return current_state

    def set_state_string(self, current_gen: str) -> StateGenString:
        """Update state machine for string generation.

        Args:
            current_gen: The currently generated string.
            current_state: The current state in the state machine.

        Returns:
            The next state based on the generated content.
        """
        new_state: StateGenString = StateGenString.START
        for c in current_gen:
            match new_state:
                case StateGenString.START:
                    if c == '"':
                        new_state = StateGenString.END
                    elif c == "\\":
                        new_state = StateGenString.IGNORE
                    else:
                        new_state = StateGenString.BODY
                case StateGenString.IGNORE:
                    new_state = StateGenString.BODY
                case StateGenString.BODY:
                    if c == '"':
                        new_state = StateGenString.END
                    elif c == "\\":
                        new_state = StateGenString.IGNORE
                case StateGenString.END:
                    return StateGenString.END
        return new_state

    def get_valid_token(
        self, current_state: StateGenNumber
    ) -> list[int]:  # valid tokens
        """Get valid tokens for the current generation state.

        Args:
            current_state: The current state in the state machine.

        Returns:
            A callable that returns the list of valid token IDs.
        """
        token_start: list[int] = [
            self.model.ft_encode(c)[0] for c in "+-0123456789"
        ]  # token start
        token_sign: list[int] = [
            self.model.ft_encode(c)[0] for c in "0123456789"
        ]  # token sign
        token_integer: list[int] = [
            self.model.ft_encode(c)[0] for c in "0123456789.,"
        ]  # token sign
        token_decimal: list[int] = [
            self.model.ft_encode(c)[0] for c in "0123456789,"
        ]  # token decimal

        def get_token() -> list[int]:
            match current_state:
                case StateGenNumber.START:
                    return token_start
                case StateGenNumber.SIGN:
                    return token_sign
                case StateGenNumber.INTEGER:
                    return token_integer
                case StateGenNumber.DECIMAL:
                    return token_decimal
                case StateGenNumber.END:
                    return []

        return get_token()
