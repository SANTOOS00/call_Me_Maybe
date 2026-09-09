from .function_name_generator import FunctionNameGenerator
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
        functions_defintions_json: str,
    ) -> None:
        self.prompts: list[Prompt] = prompts
        self.model: ManagerLLM = model
        self.trie: Trie = Trie()
        self.functions_defintions: list[FunctionDefn] = functions_defintions
        self.set_functions_names_ids_to_trie()
        self.functions_defintions_json: str = functions_defintions_json

    def run(self) -> None:
        for prompt in self.prompts:
            name_generator: FunctionNameGenerator = FunctionNameGenerator(
                model=self.model,
                functions_defintions_json=self.functions_defintions_json,
                user_prompt=prompt.prompt,
                trie=self.trie,
            )
            name_generator.generate()
            print(name_generator.function_name)

    def set_functions_names_ids_to_trie(self) -> None:
        functions_names_ids: list[list[int]] = list()
        for fn_def in self.functions_defintions:
            name_ids: list[int] = self.model.custom_encoder(fn_def.name)
            functions_names_ids.append(name_ids)

        self.trie.insert_many(functions_names_ids)


# My model is hallucinating, so I’m going to fix it by making sure it doesn’t exceed a certain maximum token limit.
