from pydantic import BaseModel
from typing import Dict, TypeAlias, Literal

types: TypeAlias = Literal["number", "string", "boolean"]


class Type(BaseModel):
    type: types


class Function_Defn(BaseModel):
    name: str
    description: str
    parameters: Dict[str, Type]
    returns: Type
