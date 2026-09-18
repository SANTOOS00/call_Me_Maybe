from typing import TypeVar, Literal, TypeAlias
from pydantic import BaseModel

TypeValue = Literal["number", "string", "boolean", "integer"]

ArgType: TypeAlias = int | float | str | bool


T = TypeVar("T", int, float, str, bool)

T_B = TypeVar("T_B", bound=BaseModel)
