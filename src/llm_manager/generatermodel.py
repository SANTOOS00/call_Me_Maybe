from llm_sdk import Small_LLM_Model
from typing import List
from ..system_prompt import SystemPrompt
from ..parser import Prompt
from ..custom_error import Call_Error
import numpy


class MangerLLM:
    def __init__(self, systemprompt: SystemPrompt) -> None:
        self.model = Small_LLM_Model()
        self.system_prompts = systemprompt
        self.generter_ids: List[int]

    def get_prompt_ids(self, prompt: str) -> List[int]:
        prompt_ids = self.model.encode(prompt)
        return [int(p_id) for p_id in prompt_ids.flatten()]

    def get_logit(self, generator_ids: List[int]) -> List[float]: 
        return self.model.get_logits_from_input_ids(generator_ids)

    def get_decode_string(self, high_score_id: int) -> str:
        return self.model.decode([high_score_id])
