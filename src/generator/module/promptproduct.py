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
    PARAMETER = """
Task:
Analyze the user request, identify the target function, and extract its parameters.

Examples:
    Answer: {
        "function": "fn_get_weather_forecast",
        "prompt": "Weather in Casablanca for 3 days",
        "description": "Fetch weather",
        "parameters": {"city": "Casablanca", "days": 3}
    }

Answer: {
    "function": "{function_name}",
    "prompt": "{user_prompt}",
    "description": "{description_method}",
    "parameters": {parameter} \""""