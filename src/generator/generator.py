from ..parser import Prompt, FunctionDefn
from ..llm_manager import ManagerLLM
from ..system_prompt import Steps
from ..trie import Trie


import numpy as np # type: ignore[import-untyped, unused-ignore]
from typing import List


class Tokenizer:
    def __init__(self,
                 functions_def: List[FunctionDefn],
                 current_step: Steps) -> None:
        self.trie = Trie()
        self.tokens: str = ""

        self._initialize_step_data(functions_def, current_step)

    def _initialize_step_data(self,
                              functions_def: List[FunctionDefn],
                              current_step: Steps
                              ) -> None:
        match current_step.value:
            case Steps.FUNCTIONS_NAME.value:
                self.populate_trie_with_function_names([fun.name for fun in functions_def])
            case _:
                pass

    def populate_trie_with_function_names(self,
                                          functions_name: List[str]
                                          ) -> None:
        for name in functions_name:
            self.trie.insert(name)

    def clean_token(self) -> None:
        self.tokens: str = ""

    def add_token(self, token: str) -> None:
        self.tokens += token


    def check_valid_tokens(self, step: Steps) -> bool:
        match step.value:
            case Steps.FUNCTIONS_NAME.value:
                return self.valid_forma_name_function()
            case _:
                return False
        return True

    def valid_forma_name_function(self) -> bool:
        print('is perfict')
        return True

    
class Generator:
    def __init__(self,
                 prompts: List[Prompt],
                 functions_dif: List[FunctionDefn],
                 model: ManagerLLM
                 ) -> None:
        self.generator_ids: List[int] = []
        self.__prompts: List[Prompt] = prompts
        self.model = model

        self.functions_dif = functions_dif
        self.trie: Trie

    def run(self) -> None:
        for prompt in self.__prompts:
            self.generate_for_prompt(prompt.prompt)

    def clean_genertor_ids(self) -> None:
        self.generator_ids: List[int] = []

    def generate_for_prompt(self, prompt: str) -> None:

        for step in Steps:
            self.clean_genertor_ids()
            trie = Tokenizer(self.functions_dif, step)

            prompt_str = self.model.system_prompt.get_step_generator(
                step, prompt)
            prompt_ids: List[int] = self.build_prompt_ids(prompt_str)

            self.generator_ids = prompt_ids
            while True:
                logits: List[float] = self.model.get_logits(self.generator_ids)
                high_score_id = int(np.argmax(logits))
                self.add_next_token(high_score_id)
                trie.add_token(self.model.decode_token(high_score_id))
                if trie.check_valid_tokens(step):
                    break

    def build_prompt_ids(self, prompt: str) -> List[int]:
        return self.model.get_prompt_ids(prompt)

    def add_next_token(self, token_id: int) -> None:
        self.generator_ids.append(token_id)
