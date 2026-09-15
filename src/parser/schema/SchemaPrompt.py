from pydantic import BaseModel, ConfigDict


class Prompt(BaseModel):
    """Represent one user prompt supplied to the generator."""

    model_config = ConfigDict(extra='forbid')
    prompt: str
