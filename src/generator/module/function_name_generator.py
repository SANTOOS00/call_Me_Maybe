from src.llm_manager.generatermodel import ManagerLLM
from ...parser import FunctionDefn
from ...trie import Trie
from enum import Enum
from .promptproduct import PromptProduct
import numpy # type: ignore[import-untyped, unused-ignore]

class FunctionNameGenerator:
    def __init__(
        self,
        model: ManagerLLM,
        functions_definitions: list[FunctionDefn]
    ) -> None:
        self.model: ManagerLLM = model
        self.trie: Trie = Trie()
        self.functions_definitions: list(FunctionDefn) = functions_definitions

        self.context_window_ids: list[int]
        self.generated_ids: list[int] = list()
        self.function_name: str = str()
        self.set_functions_names_ids_to_trie()
        


    def generate(self, user_prompt: str) -> FunctionDefn | None:
        self.clean()
        global_prompt: str = self.__build_prompt(user_prompt)
        self.context_window_ids = self.model.custom_encoder(global_prompt)
        while True:
            high_scores: list[int] = self.trie.get_children(self.generated_ids)
            if len(high_scores) == 0:
                break
            logits: list[float] = self.model.mask_logits(
                self.context_window_ids, high_scores
            )
            next_token_id: int = int(numpy.argmax(logits))
            next_token: str = self.model.decode([next_token_id])
            self.context_window_ids.append(next_token_id)
            self.generated_ids.append(next_token_id)
            self.function_name += next_token
        return self.__get_function_definition()
    

    def __get_function_definition(self) -> FunctionDefn | None :
        for fun in self.functions_definitions:
            if fun.name in self.function_name:
                return fun
        return None

    def clean(self) -> None:
        self.context_window_ids: list[int] = list()
        self.generated_ids: list[int] = list()
        self.function_name: str = str()

    def __build_prompt(self, user_prompt: str) -> str:
        return PromptProduct.FUNCTION_NAME.replace(
            "{user_prompt}", user_prompt
        )

    def set_functions_names_ids_to_trie(self) -> None:
        functions_names_ids: list[list[int]] = list()
        for fn_def in self.functions_definitions:
            name_ids: list[int] = self.model.custom_encoder(fn_def.name)
            functions_names_ids.append(name_ids)
        self.trie.insert_many(functions_names_ids)

    # def __get_function_definition(self) -> str:
    #     print(self.function_name)
    #     return "hSSSS"
    #     # for fun in self.functions_definitions:
    #     #     if fun.name == self.function_name:
    #     #         print(self)
