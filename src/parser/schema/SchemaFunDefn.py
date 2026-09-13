from pydantic import BaseModel, ConfigDict
from typing import Dict, TypeAlias, Literal

types: TypeAlias = Literal["number", "string", "boolean", "integer"]


class Type(BaseModel):
    model_config = ConfigDict(extra='forbid')
    type: types


class FunctionDefn(BaseModel):
    model_config = ConfigDict(extra='forbid')
    name: str
    description: str
    parameters: Dict[str, Type]
    returns: Type

