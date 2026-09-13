from enum import Enum


class PromptProduct(str, Enum):
    FUNCTION_NAME = """You are a precise function router.

Task:
Analyze the USER PROMPT and select the single most appropriate function from the AVAILABLE FUNCTIONS.

Examples: 
    Answer: {
        "prompt": "What is the sum of 2 and 3?",
        "function_name": "fn_add_numbers",

    }

Answer: {
    "prompt": "{user_prompt}",
    "function_name": """

    PARAMERTER_GEMERATER = """You are an AI assistant designed for system integration and automated function calling.

Task:
Extract and map the required parameters for the selected function based on the USER PROMPT.
Dynamically construct the regex pattern based on what the user actually asks to replace.


EXAMPLES:

Output:
{
    "User Prompt": "Substitute the word 'cat' with 'dog' in 'The cat sat on the mat with another cat'",
    "Function Name": "fn_substitute_string_with_regex",
    "Available Parameters and Types": {
        "source_string": "string",
        "regex": "string",
        "replacement": "string"
    },
    "Description": "Replace all occurrences matching a regex pattern in a string.",
    "Parameters": {
        "source_string": "The cat sat on the mat with another cat",
        "regex": "\\bcat\\b",
        "replacement": "dog"
    }
}
Output:
{
    "User Prompt": "Greet shrek",
    "Function Name": "fn_greet",
    "Available Parameters and Types": {
        "name": "string"
    },
    "Description": "Generate a greeting message for a person by name.",
    "Parameters": {
        "name": "shrek"
    }
}

CURRENT REQUEST:
Answer: {
    "User Prompt": "{USER_PROMPT}",
    "Function Name": "{FUNCTION_NAME}",
    "Available Parameters and Types": {FUNCTION_PARAMETERS_LIST},
    "Description": "{FUNCTION_DESCRIPTION}",
    "Parameters": {/{PARAMETERS}
"""