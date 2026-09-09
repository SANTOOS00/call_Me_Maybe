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
        self.trie: Trie = Trie()
        self.functions_defintions: list[FunctionDefn] = functions_defintions

    def run(self) -> None:
        for prompt in self.prompts:
            name_generator: FunctionNameGenerator = FunctionNameGenerator(
                model=self.model,
                user_prompt=prompt.prompt,
                trie=self.trie,
                functions_definitions=self.functions_defintions
            )
            name_generator.generate()
            parameter_generater: ParameterGenerator = ParameterGenerator(
                trie=self.trie,
                functions_definitions=self.functiones_definition,
            )

            
            print(name_generator.function_name)
