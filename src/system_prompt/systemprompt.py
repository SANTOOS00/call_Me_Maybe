from enum import Enum
from typing import List, Dict, Any, Tuple

from ..parser import FunctionDefn

from enum import Enum


class PromptType(Enum):
    FUNCTION_ROUTER = """You are a precise function router.

Task:
Analyze the USER PROMPT and select the single most appropriate function from the AVAILABLE FUNCTIONS list.

Rules:
1. Return ONLY the exact function name.
2. Do NOT include any extra text, explanations, code blocks, or markdown.

AVAILABLE FUNCTIONS:
{functions}

USER PROMPT:
{prompt}

SELECTED FUNCTION:
"""
    PARAMETER_IDENTIFIER = """You are an exact function-parameter selector.

Your job is to select the ONE parameter signature from AVAILABLE PARAMETERS 
that should be used to execute the function, based ONLY on the USER PROMPT.

Rules:

Match the USER PROMPT to the parameter signature whose description/functionality best fits the requested action.
The value mentioned in the USER PROMPT (for example, a person's name) does NOT need to appear literally in AVAILABLE PARAMETERS.
Return ONLY the exact parameter signature line, character-for-character, copied from AVAILABLE PARAMETERS.
Do NOT modify, reformat, complete, or infer anything inside the selected parameter line.
Ignore the descriptions when producing the output; use them only to determine which parameter matches.

USER PROMPT:
{prompt}

AVAILABLE PARAMETERS:
- {available_parameters}


SELECTED PARAMETER:"""




class Steps(Enum):
    FUNCTION_ROUTER = "FUNCTION_ROUTER"
    PARAMETER_IDENTIFIER = "PARAMETER_IDENTIFIER"


class SystemPrompt:
    def __init__(self, 
                 functions_difiniton: List[FunctionDefn]
                 ) -> None:        

        self.functions_defn = functions_difiniton
        self.prompt_type = PromptType

    def get_step_generator(self, step: Steps, prompt: str, name_fun: str = "") -> str:
        match step.value:
            case Steps.FUNCTION_ROUTER.value:
                return self.__make_prompt_function_name(prompt)
            case Steps.PARAMETER_IDENTIFIER.value:
                return self.__make_prompt_parameter(prompt, name_fun)
            case _:
                pass


    def get_parameters(self, name_fun: str) -> List[Tuple[Dict[str, Any], str]]:
        return [
            (fun.parameters, fun.description)
            for fun in self.functions_defn if name_fun == fun.name
        ]

    def __make_prompt_parameter(self, prompt: str, name_fun: str) -> str:
        formatted_params = []

        parameters = self.get_parameters(name_fun)
        
        for param_dict, description in parameters:
            param_str = ", ".join([f"{key}: {val.type}" for key, val in param_dict.items()])
            if param_str:
                formatted_params.append(f"\t- ({param_str}) \n\tdescription: {description}")

        available_parameters: str = "\n".join(formatted_params)

        return PromptType.PARAMETER_IDENTIFIER.value.format(
            prompt=prompt,
            available_parameters=available_parameters,
        )

    def __make_prompt_function_name(self, prompt: str) -> str:
        return PromptType.FUNCTION_ROUTER.value.format(
            functions="".join(f'\t-{fun.name} : {fun.description}\n' for fun in self.functions_defn),
            prompt=prompt
        )



# class FunctionCallingPrompts(Enum):
#     # 1. تحديد الدالة المناسبة (Function Router)


#     # 2. تحديد المعلمات المطلوبة (Required Parameters Identifier)

#     VALUE_EXTRACTOR = """You are a precise parameter value extractor.

# Task:
# Extract the exact value for the parameter '{parameter_name}' from the USER PROMPT.

# Rules:
# 1. Return ONLY the raw extracted value (e.g., city name, number, string).
# 2. Do NOT include keys, JSON syntax, quotes, or explanations.

# PARAMETER NAME: {parameter_name}
# USER PROMPT:
# {prompt}

# EXTRACTED VALUE:"""

#     # 4. بناء صيغة الـ JSON المكتملة (JSON Payload Assembler)
#     JSON_BUILDER = """You are a JSON formatter.

# Task:
# Construct a valid JSON object representing the tool call for function '{function_name}' with parameter '{parameter_name}' set to '{parameter_value}'.

# Rules:
# 1. Return ONLY valid JSON.
# 2. Do NOT write markdown blocks (no ```json).

# FUNCTION NAME: {function_name}
# PARAMETER NAME: {parameter_name}
# PARAMETER VALUE: {parameter_value}

# JSON OUTPUT:"""
