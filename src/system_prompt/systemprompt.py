from enum import Enum
from typing import List
from ..parser import FunctionDefn, Prompt
from src.custom_error import Call_Error




class PromptType(Enum):
    
    FUNCTION_NAME = """
    Task:
        Give me the function name only.

    AVAILABLE FUNCTIONS:
{FUNCTIONS}

    USER PROMPT:
    {PROMPT}
    """


class Steps(Enum):
    FUNCTIONS_NAME = "FUNCTION_NAME"
    NEXT = "NEXT"


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
            FUNCTIONS="".join(f'\t-{fun.name}\n' for fun in self.functions_defn),
            PROMPT=prompt
        )
