from llm_sdk import Small_LLM_Model
from typing import List
from ..system_prompt import SystemPrompt
from ..parser import Prompt
from ..custom_error import Call_Error
import numpy


class MangerLLM:
    def __init__(self, systemprompt: SystemPrompt,
                 prompts: List[Prompt] | None) -> None:
        if prompts is None:
            raise Call_Error("")
        self.model = Small_LLM_Model()
        self.system_prompts = systemprompt
        self.generter_ids: List[int]
        self.__prompts = prompts

    def get_prompt_ids(self, prompt: str) -> List[int]:
        prompt_ids = self.model.encode(prompt)
        return [int(p_id) for p_id in prompt_ids]

 
    def get_logit(self) -> List[float]:
        return self.model.get_logits_from_input_ids(self.generter_ids)

    def get_decode_string(self, high_score_id: int) -> str:
        return self.model.decode([high_score_id])

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