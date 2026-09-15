from enum import Enum


class PromptProduct(str, Enum):
    FUNCTION_NAME = """You are a precise function router.
FUNCTIONS DEFINITIONS:
{FUNCTION_DEFINITIONS}

USER PROMPT:
{user_prompt}

FUNCTION NAME:"""

    PARAMETER_GENERATOR = """you are a strict function-parameter extractor.
Example: {
    "prompt": "What is the sum of 2 and 3?",
    "function_prototype": "fn_add_numbers(a: number, b: number)",
    "function_description": "Reverse a string and return the reversed result.",
    "parameters": {
      "a": 2.0,
      "b": 3.0,
    }
  }
Example: {
    "prompt": "Greet john",
    "function_prototype": "fn_greet(name: string)",
    "function_description": "Generate a greeting message for a person by name.",
    "parameters": {
      "name": "john",
    }
  }
Answer: {
  "prompt": "{USER_PROMPT}",
  "function_prototype: "{FUNCTION_PROTOTYPE}",
  "function_description": "{FUNCTION_DESCRIPTION}",
  "parameters": {ARGUMENTS}"""
