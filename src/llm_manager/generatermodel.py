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
        return [int(p_id) for p_id in cast(list[int], self.encode(prompt).flatten())]

    def get_logits(self, generator_ids: list[int]) -> list[float]:
        return self.get_logits_from_input_ids(generator_ids)

    def decode_token(self, token_id: int) -> str:
        return self.decode([token_id])

    def mask_logits(
        self, context_ids: list[int], hight_socres: list[int]
    ) -> list[float]:
        logits = self.get_logits_from_input_ids(context_ids)
        for token_id, _ in enumerate(logits):
            if token_id not in hight_socres:
                logits[token_id] = float("-inf")
        return logits
    
    @lru_cache(maxsize=4)
    def encoder_chr_by_chr(self, prompt: str) -> list[int]:
        return [int(self.encode(token)) for token in prompt]

#    def __get_number_state(self, number: str) -> NumberState:
#         current_state: NumberState = NumberState.START
#         integer_counter: int = 0
#         decimal_counter: int = 0
#         for n in number:
#             match current_state:
#                 case NumberState.START:
#                     if n in "+-":
#                         current_state = NumberState.SIGN
#                     else:
#                         current_state = NumberState.INTEGER
#                 case NumberState.SIGN:
#                     current_state = NumberState.INTEGER
#                 case NumberState.INTEGER:
#                     if integer_counter != 0 and n == ".":
#                         current_state = NumberState.DECIMAL
#                     elif integer_counter != 0 and n == ",":
#                         current_state = NumberState.END
#                     else:
#                         integer_counter += 1
#                 case NumberState.DECIMAL:
#                     if decimal_counter != 0 and n == ",":
#                         current_state = NumberState.END
#                     else:
#                         decimal_counter += 1
#                 case NumberState.END:
#                     return current_state
#         return current_state
