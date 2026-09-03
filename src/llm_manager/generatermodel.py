from llm_sdk.llm_sdk import Small_LLM_Model
from typing import List
from ..system_prompt import SystemPrompt, Steps
from ..parser import Prompt


import sys


class GenerterLLM:
    def __init__(self, systemPrompt: SystemPrompt, prompts: List[Prompt]) -> None:
        self.model = Small_LLM_Model()
        self.system_prompts = SystemPrompt
        self.__prompts = prompts

    def run(self) -> None:
        for prompt in self.__prompts:
            self.__step_generter_prompt(prompt)

    def __step_generter_prompt(self, prompt: Prompt) -> None:
        pass