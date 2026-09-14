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
4. Output one value only.
5. For strings, remove only the surrounding quotes from the prompt.

Exampe 1:
Prompt: "what is the sum of 1 and 2"
Answer:
{
    "prompt": "what is the sum of 1 and 2",
    "name": "fn_add_numbers",
    "parameters": {"a": 1.0,
                   "b": 2.0}
}
Exampe 2:
Prompt: "Replace all numbers in \"Hello 34 I'm 233 years old\" with NUMBERS"
Answer:
{
    "prompt": "Replace all numbers in \"Hello 34 I'm 233 years old\" with NUMBERS",
    "name": "fn_substitute_string_with_regex",
    "parameters": {"source_string": "Hello 34 I'm 233 years old",
                   "regex": "\d+",
                   "replacement": "NUMBERS"}
}
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