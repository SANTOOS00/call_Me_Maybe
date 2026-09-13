from .module import FunctionNameGenerator, ParameterGenerator
from ..parser import Prompt, FunctionDefn
from ..llm_manager import ManagerLLM
from ..builderjson import FormatFunctionCalling, ProductJson
from pathlib import Path


from typing import Dict
import sys


class Generator:
    def __init__(
        self,
        prompts: list[Prompt],
        functions_definitions: list[FunctionDefn],
        model: ManagerLLM,
    ) -> None:

        self.prompts: list[Prompt] = prompts
        self.model: ManagerLLM = model
        self.functions_defintions: list[FunctionDefn] = functions_definitions
        self.generater_fun_name: FunctionNameGenerator = FunctionNameGenerator(
            model=self.model,
            functions_definitions=functions_definitions
        )
        self.generater_parameters: ParameterGenerator = ParameterGenerator(
            model=model
        )
        self.productjson: ProductJson = ProductJson()

    def run(self, path: Path) -> None:
        for user_prompt in self.prompts:
            function: FunctionDefn | None = \
            self.generater_fun_name.generate(user_prompt=user_prompt.prompt)
            if function is None:
                print("is not function definition")
                sys.exit(1)
            parameters: Dict[str, int | str | bool | float] = self.generater_parameters.generate(function_definition=function,
                                                                                                 prompt=user_prompt.prompt)
            self.__valid_parameters(parameters)
            function_calling: FormatFunctionCalling = FormatFunctionCalling(
                name=function.name,
                prompt=user_prompt.prompt,
                parameters=parameters
            )
            print(function_calling)
            self.productjson.add_function(function_calling)
            self.productjson.write_in_file(path)

    def __valid_parameters(self, parameters: Dict[str, int | float | str | float]) -> None:
        for key, val in parameters.items():
            if isinstance(val, str):
                parameters[key] = val[2:]

