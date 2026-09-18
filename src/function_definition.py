from typing_extensions import override
from pydantic import BaseModel, Field, RootModel
from .project_types import TypeValue


class ParameterFunctionCall(BaseModel):
    """Represents a parameter for a function call.

    Attributes:
        type_value: The type of the parameter:
        (number, string, boolean, or integer).
    """

    type_value: TypeValue = Field(alias="type")  # TYPE VALUE


class FunctionDefinitionModel(BaseModel):
    """Represents a function call definition with parameters and return type.

    Attributes:
        name: The name of the function.
        description: A description of what the function does.
        parameters: A dictionary of parameter names to their types.
        returns: The return type of the function.
    """

    name: str = Field(min_length=1)
    description: str = Field(min_length=1)
    parameters: dict[str, ParameterFunctionCall]
    returns: ParameterFunctionCall

    class ConfigDict:
        extra: str = "forbid"

    @override
    def __str__(self) -> str:
        """Return a string representation of the function call.

        Returns:
            A string showing the function signature and description.
        """
        params = ", ".join(
            f"{name}: {type_a.type_value}"
            for name, type_a in self.parameters.items()  # parameters
        )
        return (
            f"{self.name}({params}) -> {self.returns.type_value}, \n "
            + f'"description": {self.description}'
        )


class FunctionDefinitionRootModel(RootModel[list[FunctionDefinitionModel]]):
    """Root model for a list of function definitions."""
    pass

