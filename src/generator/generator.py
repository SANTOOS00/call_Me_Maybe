from ..parser import Prompt, FunctionDefn
from ..llm_manager import  ManagerLLM
from ..system_prompt import Steps
from ..custom_error import Call_Error
from ..trie import Trie
from ..system_prompt import SystemPrompt


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
            case Steps.PARAMETER.value:
                self.populate_trie_with_parameters([f"{fun.parameters}" for fun in functions_def])

    def populate_trie_with_parameters(self,
                                      parameters: List[str]) -> None:
        for parameter in parameters:
            self.trie.insert(parameter)

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
                return self.valid_tokenizer()
            case Steps.PARAMETER.value:
                return False
        return True
                                   
    def valid_tokenizer(self) -> bool:
        for ch in self.tokens:
            if self.trie.isPrefix(self.tokens):
                return self.trie.search(self.tokens)
            else:
                self.tokens = self.tokens.replace(ch, "", 1)
        return False


    
class Generator(ManagerLLM):
    def __init__(self,
                 prompts: List[Prompt],
                 functions_dif: List[FunctionDefn],
                 system_prompt: SystemPrompt
                 ) -> None:
        self.generator_ids: List[int] = []
        self.__prompts: List[Prompt] = prompts
        self.system_prompt = system_prompt
        self.functions_dif = functions_dif
        self.trie: Trie
        super().__init__()

    def clean_genertor_ids(self) -> None:
        self.generator_ids: List[int] = []

    def run(self) -> None:
        for prompt in self.__prompts:
            self.generate_for_prompt(prompt.prompt)

    def generate_for_prompt(self, prompt: str) -> None:

        for step in Steps:
            self.clean_genertor_ids()
            trie = Tokenizer(self.functions_dif, step)

            prompt_str = self.system_prompt.get_step_generator(
                step, prompt)
            prompt_ids: List[int] = self.build_prompt_ids(prompt_str)

            self.generator_ids = prompt_ids
            while True:
                logits: List[float] = self.get_logits(self.generator_ids)
                high_score_id = int(np.argmax(logits))
                self.add_next_token(high_score_id)
                trie.add_token(self.decode_token(high_score_id))
                Call_Error.string = trie.tokens
                print(trie.tokens, flush=True)
                if trie.check_valid_tokens(step):
                    break
            # print(trie.tokens)

    def build_prompt_ids(self, prompt: str) -> List[int]:
        return self.get_prompt_ids(prompt)

    def add_next_token(self, token_id: int) -> None:
        self.generator_ids.append(token_id)
