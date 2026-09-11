from .module import FunctionNameGenerator, ParameterGenerator
from ..parser import Prompt, FunctionDefn
from ..llm_manager import ManagerLLM
from ..trie import Trie

from typing import Dict
import numpy as np  # type: ignore[import-untyped, unused-ignore]


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

    def run(self) -> None:
        for user_prompt in self.prompts:
            function: FunctionDefn | None = \
            self.generater_fun_name.generate(user_prompt=user_prompt.prompt)
            if function is None:
                print("is not function definition")
            print(function.name)
            parameters: Dict[str, int | str | bool] = self.generater_parameters.generate(
                function, user_prompt.prompt)