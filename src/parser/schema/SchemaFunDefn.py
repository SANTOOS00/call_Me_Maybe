from pydantic import BaseModel, ValidationError


class SchemaFunDefn(BaseModel):
    age: int
