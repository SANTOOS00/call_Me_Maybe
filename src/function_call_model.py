from pydantic import BaseModel, RootModel
from .project_types import ArgType


class FunctionCallModel(BaseModel):
    """Represents a function call with its prompt, name, and arguments.

    Attributes:
        prompt: The user prompt that triggered the function call.
        function: The name of the function to call.
        arguments: Dictionary mapping parameter names to their values.
    """
    prompt: str
    function: str
    arguments: dict[str, ArgType]

    class ConfigDict:
        extra: str = "forbid"


class FunctionCallRootModel(RootModel[list[FunctionCallModel]]):
    """Root model for a list of function calls."""
    pass
