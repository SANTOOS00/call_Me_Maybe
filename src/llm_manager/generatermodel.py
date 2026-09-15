from typing import cast
from llm_sdk import Small_LLM_Model  # type: ignore[import-untyped, unused-ignore]
from functools import lru_cache




class ManagerLLM(Small_LLM_Model):
    def __init__(
        self,
        model_name: str = "Qwen/Qwen3-0.6B",
    ) -> None:
        super().__init__(model_name)

    def custom_encoder(self, prompt: str) -> list[int]:
        return [int(p_id) for p_id in cast(list[int], self.encode(prompt)[0])]

    def get_logits(self, generator_ids: list[int]) -> list[float]:
        return self.get_logits_from_input_ids(generator_ids)

    def decode_token(self, token_id: int) -> str:
        return self.decode([token_id])

    def mask_logits(
        self, context_ids: list[int], hight_socres: list[int] | None = None
    ) -> list[float]:
        logits = self.get_logits_from_input_ids(context_ids)
        if hight_socres is None:
            return logits
        for token_id, _ in enumerate(logits):
            if token_id not in hight_socres:
                logits[token_id] = float("-inf")
        return logits
    
    def encoder_chr_by_chr(self, prompt: list[str]) -> list[int]:
        token_ids: list[int] = []
        for character in prompt:
            token_ids.append(self.custom_encoder(character)[0])
        return token_ids
