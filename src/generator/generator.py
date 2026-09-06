from ..parser import Prompt, FunctionDefn
from ..llm_manager import  ManagerLLM
from ..system_prompt import Steps
from ..builderjson import FunCallBuilder
from ..trie import Trie
from ..system_prompt import SystemPrompt


import numpy as np # type: ignore[import-untyped, unused-ignore]
from typing import List


class Tokenizer(ManagerLLM, FunCallBuilder, Trie):
    def __init__(self,
                 functions_def: List[FunctionDefn]
                 ) -> None:
        self.tokens: str = ""
        self.functions_def = functions_def

        super().__init__()

    def check_valid_tokens(self, step: Steps) -> bool:
        match step.value:
            case Steps.FUNCTIONS_NAME.value:
                self._initialize_step_data(step)
                return self.valid_tokenizer()
            case Steps.PARAMETER.value:
                self._initialize_step_data(step)
                return True
        return True

    def _initialize_step_data(self,
                              current_step: Steps
                              ) -> None:
        self.clean_trie()
        match current_step.value:
            case Steps.FUNCTIONS_NAME.value:
                self.populate_trie_with_function_names()
            case Steps.PARAMETER.value:
                self.populate_trie_with_parameters()
                  
    def valid_tokenizer(self) -> bool:
        for ch in self.tokens:
            if self.isPrefix(self.tokens):
                return self.search(self.tokens)
            else:
                self.tokens = self.tokens.replace(ch, "", 1)
        return False

    def populate_trie_with_parameters(self) -> None:
        pass

    def populate_trie_with_function_names(self) -> None:
        for fun in self.functions_def:
            self.insert(fun.name)

    def get_token(self) -> str:
        return self.tokens

    def set_name_function(self) -> None:
        return super().set_name_function(self.get_token())

    def clean(self) -> None:
        self.tokens = ""
        super().clean()
        super().clean_trie()

    def add_token(self, token: str) -> None:
        self.tokens += token


class Generator(Tokenizer):
    def __init__(self,
                 prompts: List[Prompt],
                 functions_def: List[FunctionDefn],
                 system_prompt: SystemPrompt
                 ) -> None:
        self.generator_ids: List[int] = []
        self.__prompts: List[Prompt] = prompts
        self.system_prompt = system_prompt

        super().__init__(functions_def=functions_def)

    def clean_genertor_ids(self) -> None:
        self.generator_ids: List[int] = []

    def run(self) -> None:
        for prompt in self.__prompts:
            self.generate_for_prompt(prompt.prompt)

    def clean(self) -> None:
        self.clean_genertor_ids()
        super().clean()

    def generate_for_prompt(self, prompt: str) -> None:
        for step in Steps:
            self.clean()
            prompt_str = self.system_prompt.get_step_generator(step, prompt)
            prompt_ids: List[int] = self.build_prompt_ids(prompt_str)
            self.generator_ids = prompt_ids
            while True:
                logits: List[float] = self.get_logits(self.generator_ids)
                high_score_id = int(np.argmax(logits))
                self.add_next_token(high_score_id)
                self.add_token(self.decode_token(high_score_id))
                if self.check_valid_tokens(step):
                    if step.value == Steps.FUNCTIONS_NAME.value:
                        self.set_name_function()
                        self.set_prompt(prompt)
                        self.prints()
                    break

    def build_prompt_ids(self, prompt: str) -> List[int]:
        return self.get_prompt_ids(prompt)

    def add_next_token(self, token_id: int) -> None:
        self.generator_ids.append(token_id)
