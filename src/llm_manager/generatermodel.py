from typing import List
from llm_sdk import Small_LLM_Model # type: ignore[import-untyped, unused-ignore]
from ..system_prompt import SystemPrompt


class ManagerLLM:
    def __init__(self, system_prompt: SystemPrompt) -> None:
        self.model = Small_LLM_Model()
        self.system_prompt = system_prompt
        self.generated_ids: List[int] = []

    def get_prompt_ids(self, prompt: str) -> List[int]:
        prompt_ids = self.model.encode(prompt)
        return [int(p_id) for p_id in prompt_ids.flatten()]

    def get_logits(self, generator_ids: List[int]) -> List[float]:
        return self.model.get_logits_from_input_ids(generator_ids)

    def decode_token(self, token_id: int) -> str:
        return self.model.decode([token_id])
