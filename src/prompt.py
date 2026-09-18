from pydantic import BaseModel, Field, RootModel


class Prompt(BaseModel):
    """Represents a user prompt for function calling.

    Attributes:
        prompt: The prompt text (must be non-empty).
    """

    prompt: str = Field(min_length=1)

    class ConfigDict:
        extra: str = "forbid"


class PromptRootModel(RootModel[list[Prompt]]):
    """Root model for a list of user prompts."""
    pass
