from ..parser import Prompt
from typing import List
from ..llm_manager import MangerLLM
from ..system_prompt import Steps
import numpy as np


class Generator:
    def __init__(self, prompts: List[Prompt], model: MangerLLM) -> None:
        self.__prompts = prompts
        self.model = model
        self.generator_ids: List[int]
    def run(self) -> None:
        for prompt in self.__prompts:
            self.step_generator_promtp(prompt.prompt)

    def step_generator_promtp(self, prompt: str) -> None:
        for step in Steps:
            prompt_str = self.model.system_prompts.get_step_generator(
                step,
                prompt)
            prompt_ids: List[int] = self.generator_prompt(prompt_str)
            self.generator_ids = prompt_ids

            while True:
                logits: List[float] = self.model.get_logit(self.generator_ids)

                high_score_id: int = np.argmax(logits)
                self.add_next_token(high_score_id)
                print(self.model.get_decode_string(high_score_id), end='', flush=True)





        # prompt_id = [int(id) for id in model.encode(prompt.prompt).flatten()]
        # generated_ids: list[int] = prompt_id
        # fn_name_ids: list[int] = list()
        # fn_name: str = str()
        # while True:
        #     logits: list[float] = model.get_logits_from_input_ids(generated_ids)
        #     high_score_id: int = np.argmax(logits)

        #     generated_ids.append(high_score_id)

        #     token = model.decode(high_score_id)
        #     print(token, end="", flush=True)

    def generator_prompt(self, prompt: str) -> List[int]:
        return self.model.get_prompt_ids(prompt)

    def add_next_token(self, high_score_id: int) -> None:
        self.generator_ids.append(high_score_id)
