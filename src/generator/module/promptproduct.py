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
    "function_name": \""""


    PARAMERTER_GEMERATER ="""
- You are an AI assistant designed for system integration and automated function calling.

EXAMPLE:
    ouput: {
        "User Prompt": "Replace all vowels in 'Programming is fun' with asterisks",
        "Function Name": "fn_substitute_string_with_regex",
        "Available Parameters and Types": ("source_string": "string", "regex": "string", "replacement": "string")
        "Description": "Replace all occurrences matching a regex pattern in a string.",
        "Parameters": ("source_string": "Programming is fun", "regex": "aeiouAEIOU", "replacement": "*")
        ,
        {
        "User Prompt": "Greet shrek",
        "Function Name": "fn_greet",
        "Available Parameters and Types": ("name": "string")
        "Description": "Generate a greeting message for a person by name."
        "Parameters": ("name": "shrek")
        }
Answer: {
    "User Prompt": "{USER_PROMPT}",
    "Function Name": "{FUNCTION_NAME}",
    "Available Parameters and Types": {FUNCTION_PARAMETERS_LIST}
    "Description": "{FUNCTION_DESCRIPTION}",
    "Parameters": {PARAMETERS}"""   