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
                 functions_difiniton: List[FunctionDefn] | None,
                 prompts: List[Prompt] | None) -> None:
        self.prompt_type = PromptType
        

        if prompts is None:
            raise Call_Error("")
        
        if functions_difiniton is None:
            raise Call_Error("")

        self.functions_defn = functions_difiniton
        self.prompts = prompts

    def get_step(self, step: Steps) -> str:
        match step.value:
            case Steps.value:
                return self.__make_prompt_function_name()
            case _:
                return ""

    def __make_prompt_function_name(self) -> str:
        self.join_prompt()
        return ""

    def join_prompt(self) -> str:
        return ""
