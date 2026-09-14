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

    PARAMETER_GENERATOR = r"""You are a strict function-parameter extractor.

Your task is to generate the value of CURRENT PARAMETER for the selected
function. Use the complete FUNCTION DEFINITION and the USER PROMPT together.
The parameter name is only a schema key; it is not automatically the value.

Rules:
1. Extract only the value for CURRENT PARAMETER from USER PROMPT.
2. Respect the type declared in FUNCTION DEFINITION.
3. Do not copy the parameter name or reuse another parameter's value.
4. Output one value only, without a key, explanation, JSON, or markdown.

Examples:

Example A:
User prompt:
Replace all vowels in "Programming is fun" with asterisks
{"name": "fn_substitute_string_with_regex", "parameters": {
  "source_string": Programming is fun,
  "regex": [aeiouAEIOU],
  "replacement": *
}}

Example B:
User prompt:
Substitute the word "cat" with "dog" in
{"name": "fn_substitute_string_with_regex", "parameters": {
  "source_string": The cat sat on the mat with another cat,
  "regex": \bcat\b,
  "replacement": dog
}}

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