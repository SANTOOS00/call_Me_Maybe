from .module import FunctionNameGenerator, ParameterGenerator
from ..parser import Prompt, FunctionDefn
from ..llm_manager import ManagerLLM
from ..trie import Trie


import numpy as np  # type: ignore[import-untyped, unused-ignore]


class Generator:
    def __init__(
        self,
        prompts: list[Prompt],
        functions_defintions: list[FunctionDefn],
        model: ManagerLLM,
    ) -> None:

        self.prompts: list[Prompt] = prompts
        self.model: ManagerLLM = model
        self.functions_defintions: list[FunctionDefn] = functions_defintions
        self.generater_fun_name: FunctionNameGenerator = FunctionNameGenerator(
            model=self.model,
            trie=Trie(),
            functions_definitions=functions_defintions
        )

    def run(self) -> None:
        for user_prompt in self.prompts:
            function: FunctionNameGenerator = self.generater_fun_name.generate(user_prompt=user_prompt)
            print(type(function))
