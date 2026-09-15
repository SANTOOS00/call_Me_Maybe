from pydantic import BaseModel, ConfigDict
from typing import Dict, TypeAlias, Literal

types: TypeAlias = Literal["number", "string", "boolean", "integer"]
ARG_TYPE: TypeAlias = int | float | bool | str


class Type(BaseModel):
    model_config = ConfigDict(extra='forbid')
    type: types


class FunctionDefn(BaseModel):
    model_config = ConfigDict(extra='forbid')
    name: str
    description: str
    parameters: Dict[str, Type]
    returns: Type
    def __str__(self) -> str:
        func_prototype: list[str] = list(f"{self.name}(")

        for idx, (arg_name, arg_type) in enumerate(self.parameters.items()):
            func_prototype.append(f"{arg_name}: {arg_type.type}")
            if idx < len(self.parameters.keys()) - 1:
                func_prototype.append(', ')


        func_prototype.append(")")
        return "".join(func_prototype)

    

    def get_pre_generated_argument_format(self, generated_arguments: dict[str, ARG_TYPE], current_arg: tuple[str, type]) -> str:
        format_arg: list[str] = list("{\n\t")
        prefix_suffex: str
        for arg_name, arg_value in generated_arguments.items():
            prefix_suffex = '"' if isinstance(arg_value, str) else str()
            format_arg.append(f'"{arg_name}": {prefix_suffex}{arg_value}{prefix_suffex},\n\t')
        current_arg_name, current_arg_type = current_arg
        prefix_suffex = '"' if current_arg_type == "string" else str()
        format_arg.append(f'"{current_arg_name}": {prefix_suffex}')
        return "".join(format_arg)


if __name__ == "__main__":
    preg_generated_argument: dict[str, ARG_TYPE]={"a": 42132, "b": 2}
    parameters={"a": Type(type="string"), "b": Type(type="string")}
    function_def: FunctionDefn = FunctionDefn( name="fn_add", description="description", parameters=parameters, returns= Type(type="number"))
    print(function_def)

    current_arg: tuple[str, type] = ("a", "number")
    print(function_def.get_pre_generated_argument_format(preg_generated_argument, current_arg))