from enum import Enum, auto


class StateGenNumber(Enum):
    """State machine states for numeric generation.

    States:
        START: Initial state.
        SIGN: Optional sign (+/-) has been generated.
        INTEGER: Integer part is being generated.
        DECIMAL: Decimal point has been found.
        END: Generation is complete.
    """

    START = auto()
    SIGN = auto()
    INTEGER = auto()
    DECIMAL = auto()
    END = auto()


class StateGenString(Enum):
    """State machine states for string generation.

    States:
        START: Initial state.
        BODY: String body is being generated.
        END: Closing quote has been found.
    """

    START = auto()
    BODY = auto()
    IGNORE = auto()
    END = auto()
