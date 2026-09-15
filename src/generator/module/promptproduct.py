from enum import Enum


class PromptProduct(str, Enum):
    FUNCTION_NAME = """You are a precise function router.

Task:
Analyze the USER PROMPT and select the single most appropriate function from
the FUNCTION DEFINITIONS. Return only one exact function name.

FUNCTION DEFINITIONS:
{FUNCTION_DEFINITIONS}

USER PROMPT:
{user_prompt}

FUNCTION NAME:"""

    PARAMETER_GENERATOR = r"""you are a strict function-parameter extractor.
Example: 
Answer: {
    "prompt": "What is the sum of 2 and 3?",
    "function_prototype": "fn_add_numbers(a: number, b: number)",
    "function_description": "Reverse a string and return the reversed result.",
    "parameters": {
      "a": 2.0,
      "b": 3.0,
    }
  }

Answer: {
    "prompt": "Greet shrek",
    "function_prototype: "fn_greet(name: string)",
    "function_description": "Generate a greeting message for a person by name.",
    "parameters": {
      "name": "shrek"
    }
  }


Answer: {
  "prompt": "{USER_PROMPT}",
  "function_prototype: "{FUNCTION_PROTOTYPE}",
  "function_description": "{FUNCTION_DESCRIPTION}",
  "parameters": {ARGUMENTS}"""