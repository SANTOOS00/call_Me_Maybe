from ..parser import Prompt
from typing import List
from ..llm_manager import ManagerLLM
from ..system_prompt import Steps
from ..custom_error import Call_Error
import numpy as np # type: ignore[import-untyped, unused-ignore]


class Generator:
    def __init__(self, prompts: List[Prompt], model: ManagerLLM) -> None:
        self.__prompts = prompts
        self.model = model
        self.generator_ids: List[int]

    def run(self) -> None:
        for prompt in self.__prompts:
            self.generate_for_prompt(prompt.prompt)

    def generate_for_prompt(self, prompt: str) -> None:
        for step in Steps:
            prompt_str = self.model.system_prompt.get_step_generator(
                step,
                prompt)
            prompt_ids: List[int] = self.build_prompt_ids(prompt_str)
            self.generator_ids = prompt_ids

            while True:
                logits: List[float] = self.model.get_logits(self.generator_ids)

                high_score_id: int = np.argmax(logits)
                self.add_next_token(high_score_id)
                Call_Error.string += self.model.decode_token(high_score_id)

    def build_prompt_ids(self, prompt: str) -> List[int]:
        return self.model.get_prompt_ids(prompt)

    def add_next_token(self, token_id: int) -> None:
        self.generator_ids.append(token_id)
