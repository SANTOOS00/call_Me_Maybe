from src.llm_manager.generatermodel import ManagerLLM
from ...parser import FunctionDefn
from src.trie import Trie
from enum import Enum
import numpy # type: ignore[import-untyped, unused-ignore]


class PromptProduct(Enum):
    FUNCTION_NAME = """You are a precise function router.

Task:
Analyze the USER PROMPT and select the single most appropriate function from the AVAILABLE FUNCTIONS list.

AVAILABLE FUNCTIONS:
{functions_defintions}


Examples: 
    Answer: {
        "prompt": "What is the sum of 2 and 3?",
        "function_name": "fn_add_numbers",

    }

Answer: {
    "prompt": "{user_prompt}",
    "function_name": \""""


class FunctionNameGenerator:
    def __init__(
        self,
        model: ManagerLLM,
        trie: Trie,
        functions_definitions: list[FunctionDefn]
    ) -> None:
        self.model: ManagerLLM = model
        self.trie: Trie = trie
        self.functions_definitions: list(FunctionDefn) = functions_definitions

        self.context_window_ids: list[int]
        self.generated_ids: list[int] = list()
        self.function_name: str = str()
        

    def generate(self, user_prompt: str) -> None:
        self.set_functions_names_ids_to_trie()
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
        return self.get_function_definition()
    
    def __get_function_definition(self) -> FunctionDefn:
        
        return (
            fun_definition 
            for fun_definiton in self.functions_definitions 
            if fun_definition.name == self.function_name
        )

    def __build_prompt(self, user_prompt: str) -> str:
        return PromptProduct.FUNCTION_NAME.value

    
    def set_functions_names_ids_to_trie(self) -> None:
        functions_names_ids: list[list[int]] = list()
        for fn_def in self.functions_definitions:
            name_ids: list[int] = self.model.custom_encoder(fn_def.name)
            functions_names_ids.append(name_ids)

        self.trie.insert_many(functions_names_ids)


