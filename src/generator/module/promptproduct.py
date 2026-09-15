from enum import Enum


class PromptProduct(str, Enum):
    FUNCTION_NAME = """You are a precise function router.
FUNCTION DEFINITIONS:
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
    "prompt": "Replace all numbers in \"Hello 34 I'm 233 years old\" with NUMBERS",
    "function_prototype": "fn_substitute_string_with_regex(source_string: string, regex: string, replacement: string),
    "function_description": "Replace all occurrences matching a regex pattern in a string.",
    "parameters": {
      "source_string": "Hello 34 I'm 233 years old",
      "regex": "([0-9]+)",
      "replacement": "NUMBERS"
    }
  }
Answer: {
  "prompt": "{USER_PROMPT}",
  "function_prototype: "{FUNCTION_PROTOTYPE}",
  "function_description": "{FUNCTION_DESCRIPTION}",
  "parameters": {ARGUMENTS}"""
