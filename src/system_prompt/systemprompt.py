from enum import Enum
from typing import List
from ..parser import FunctionDefn, Prompt
from src.custom_error import Call_Error




class PromptType(Enum):
    FUNCTION_NAME = """
You are a precise function router.

Task:
Analyze the USER PROMPT and select the single most appropriate function from the AVAILABLE FUNCTIONS list.

Rules:
1. Return ONLY the exact function name.
2. Do NOT include any extra text, explanations, code blocks, or punctuation.

AVAILABLE FUNCTIONS:
{FUNCTIONS}

USER PROMPT:
{PROMPT}

SELECTED FUNCTION:"""
    

class Steps(Enum):
    FUNCTIONS_NAME = "FUNCTION_NAME"


class SystemPrompt:
    def __init__(self, 
                 functions_difiniton: List[FunctionDefn] | None) -> None:        
        if functions_difiniton is None:
            raise Call_Error("")

        self.functions_defn = functions_difiniton
        self.prompt_type = PromptType

    def get_step_generator(self, step: Steps, prompt: str) -> str:
        match step.value:
            case Steps.FUNCTIONS_NAME.value:
                return self.__make_prompt_function_name(prompt)
            case _:
                return ""

    def __make_prompt_function_name(self, prompt: str) -> str:
        return PromptType.FUNCTION_NAME.value.format(
            FUNCTIONS="".join(f'\t-{fun.name} : {fun.description}\n' for fun in self.functions_defn),
            PROMPT=prompt
        )
