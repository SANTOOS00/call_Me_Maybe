from llm_sdk.llm_sdk import Small_LLM_Model
from typing import List
from ..system_prompt import SystemPrompt, Steps
from ..parser import Prompt
from ..custom_error import Call_Error


import sys


class GenerterLLM:
    def __init__(self, systemprompt: SystemPrompt,
                 prompts: List[Prompt] | None) -> None:
        if prompts is None:
            raise Call_Error("")
        self.model = Small_LLM_Model()
        self.system_prompts = systemprompt
        self.__prompts = prompts

    def run(self) -> None:
        for prompt in self.__prompts:
            self.__step_generter_prompt(prompt)

    def __step_generter_prompt(self, prompt: Prompt) -> None:

        for step in Steps:
            prompt_string = self.system_prompts.get_step(step, prompt)
            print(prompt_string)