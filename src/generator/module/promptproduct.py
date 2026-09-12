from enum import Enum


class PromptProduct(str, Enum):
    FUNCTION_NAME = """You are a precise function router.

Task:
Analyze the USER PROMPT and select the single most appropriate function from the AVAILABLE FUNCTIONS list.

Examples: 
    Answer: {
        "prompt": "What is the sum of 2 and 3?",
        "function_name": "fn_add_numbers",

    }

Answer: {
    "prompt": "{user_prompt}",
    "function_name": \""""
    PARAMERTER_GEMERATER ="""
- You are an AI assistant designed for system integration and automated function calling.
- Your sole task is to analyze the user's request and extract the necessary arguments defined in
    the provided function interface.

# Available Function:
- User Prompt: {USER_PROMPT}
- Function Name: {FUNCTION_NAME}
- Description: {FUNCTION_DESCRIPTION}
- Available Parameters and Types:
{FUNCTION_PARAMETERS_LIST}

# Strictly Allowed Parameter Types:
1. string: Text wrapped in double quotes (e.g., "example").
2. int: Integer numbers without decimals or quotes (e.g., 42).
3. float: Floating-point numbers without quotes (e.g., 3.14).
4. bool: Boolean values without quotes (true or false).

EXAMPLE:
    Answer: {
        "User Prompt": Replace all vowels in 'Programming is fun' with asterisks,
        "Function name": fn_substitute_string_with_regex,
        "Description": Replace all occurrences matching a regex pattern in a string.,
        "Parameters": {
        "source_string": "Programming is fun",
        "regex": "aeiouAEIOU",
        "replacement": "*"
        }
Answer: {
    "User Prompt": {USER_PROMPT},
    "Function Name": {FUNCTION_NAME},
    "Description": {FUNCTION_DESCRIPTION},
    "Parameters": {PARAMERTS}"""