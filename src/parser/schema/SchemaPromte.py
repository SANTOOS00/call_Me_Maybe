from pydantic import BaseModel, ValidationError


class SchemaPromte(BaseModel):
    age: int
