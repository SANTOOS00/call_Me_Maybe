from enum import Enum


class PromptToLlm(str, Enum):
    """Prompt templates for LLM interaction in function calling.

    Attributes:
        GET_FUNCTION_NAME: Prompt template for selecting a function by name.
        GET_PRRAMETERS_FUNCTION: Prompt template for extracting functions
        parameters.
    """

    GET_FUNCTION_NAME = """
    You are a function selector.

    Your task is to select exactly one function from the available functions
    that best matches the user's request.

    Return ONLY a valid JSON object with exactly this structure:

    {
      "name": "<function_name>"
    }

    Rules:
    - Select exactly one function.
    - The value of "name" MUST be exactly one of the available function names.
    - Do not modify the function name.
    - Do not add any other fields.
    - Do not explain your choice.
    - Output JSON only.

    USER'S REQUEST:
    {PROMPT USER}

    AVAILABLE FUNCTIONS:
    {FUNCTIONS}

        name: \""""

    GET_PRRAMETERS_FUNCTION = """
        You are a function-calling parameter extraction model.

        Your task is to extract the parameters required by the selected
        functionsfrom the user's request.

        ## RULES

        1. Generate ONLY the parameters as valid JSON.
        2. Use ONLY parameters defined in the function definition.
        3. Extract parameter values directly from the user's request.
        4. Do NOT invent values.

        Examples:
        Answer: {
            "prompt": "Greet shrek",
            "function": "greet(name: string)",
            "description": "Generate a greeting message for a person by name.",
            "arguments": "{"name": "shrek"}
        }

        Answer: {
            "prompt": "Replace all vowels in 'Programming is fun'
            with asterisks"
            "name": "fn_substitute_string_with_regex",
            "description": "Replace all occurrences matching a regex pattern
            in a string.",
            "arguments": {"source_string": "Programming is fun",
            "regex": "[aeiou]", "replacement": "*"},

        Answer: {
            "prompt": "{USER_PROMPT}",
            "function": "{FUNCTION}",
            "arguments": {ARGUMENTS}"""
