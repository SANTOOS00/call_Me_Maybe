from ..parser import Prompt
from ..llm_manager import ManagerLLM
from ..system_prompt import Steps
from ..trie import Trie

import numpy as np # type: ignore[import-untyped, unused-ignore]
from typing import List


class Token:
    def __init__(self) -> None:
        self.trie = Trie()
        self.tokens: str = ""

    def clean_token(self) -> None:
        self.tokens: str = ""

    def add_token(self, token: str) -> None:
        self.tokens += token


    def check_valid_tokens(self, step: Steps) -> bool:
        match step.value:
            case _:
                return self.valid_forma_name_function()
        return True

    def valid_forma_name_function(self) -> bool:
        return True

    
class Generator(Token):
    def __init__(self,
                 prompts: List[Prompt],
                 model: ManagerLLM
                 ) -> None:
        self.function_name: str = ""
        self.generator_ids: List[int] = []
        self.__prompts: List[Prompt] = prompts
        self.model = model

    def run(self) -> None:
        for prompt in self.__prompts:
            self.generate_for_prompt(prompt.prompt)

    def clean_genertor_ids(self) -> None:
        self.generator_ids: List[int] = []

    def generate_for_prompt(self, prompt: str) -> None:
        for step in Steps:
            prompt_str = self.model.system_prompt.get_step_generator(
                step, prompt)
            prompt_ids: List[int] = self.build_prompt_ids(prompt_str)
            self.clean_genertor_ids()
            self.clean_token()
            self.generator_ids = prompt_ids
            while True:
                logits: List[float] = self.model.get_logits(self.generator_ids)
                high_score_id = int(np.argmax(logits))
                self.add_next_token(high_score_id)
                self.add_token(self.model.decode_token(high_score_id))
                if self.check_valid_tokens(step):
                    break

    def build_prompt_ids(self, prompt: str) -> List[int]:
        return self.model.get_prompt_ids(prompt)

    def add_next_token(self, token_id: int) -> None:
        self.generator_ids.append(token_id)
