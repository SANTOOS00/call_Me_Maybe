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

    PARAMETER_GENERATOR = """You are a strict function-parameter extractor.

Your task is to generate the value of CURRENT PARAMETER for the selected
function. Use the complete FUNCTION DEFINITION and the USER PROMPT together.
The parameter name is only a schema key; it is not automatically the value.

Rules:
1. Extract only the value for CURRENT PARAMETER from USER PROMPT.
2. Respect the type declared in FUNCTION DEFINITION.
3. Do not copy the parameter name or reuse another parameter's value.
4. Output one value only, without a key, explanation, JSON, or markdown.
5. For strings, remove only the surrounding quotes from the prompt.
6. For numbers and integers, output only the numeric literal.

Examples:

Example 1 - regex:
Function definition:
{"name": "fn_substitute_string_with_regex", "parameters": {
  "source_string": {"type": "string"},
  "regex": {"type": "string"},
  "replacement": {"type": "string"}
}}
User prompt: "Replace all numbers in 'Hello 34' with 'NUMBERS'"
Current parameter: source_string
Output: Hello 34
Current parameter: regex
Output: \\d+
Current parameter: replacement
Output: NUMBERS

Example 2 - regex with a word:
Function definition:
{"name": "fn_substitute_string_with_regex", "parameters": {
  "source_string": {"type": "string"},
  "regex": {"type": "string"},
  "replacement": {"type": "string"}
}}
User prompt: "Replace the word 'cat' with 'dog' in 'cat sat'"
Current parameter: source_string
Output: cat sat
Current parameter: regex
Output: \\bcat\\b
Current parameter: replacement
Output: dog

Now extract from the actual request:

FUNCTION DEFINITION:
{FUNCTION_DEFINITION}

USER PROMPT:
{USER_PROMPT}

ALREADY EXTRACTED PARAMETERS:
{PARAMETERS}

CURRENT PARAMETER:
Name: {PARAMETER_NAME}
Type: {PARAMETER_TYPE}

CURRENT VALUE:"""
