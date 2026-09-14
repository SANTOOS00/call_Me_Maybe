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


    PARAMETER_GENERATOR = """
        You are a function-calling assistant that
        helps me get a JSON format from a user prompt.

        Available functions:
        {FUNCTION_DEFINITION}

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

    User prompt: {USER_PROMPT}

    JSON:
    {
        "prompt": "{USER_PROMPT}",
        "name": "{FUNCTION_NAME}",
        "parameters": {{PARAMETERS}"""