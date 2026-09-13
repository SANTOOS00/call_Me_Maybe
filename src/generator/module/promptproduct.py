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


    PARAMERTER_GENERATER = """
You are a precise AI function router. Your task is to analyze the user input and convert it into a valid JSON function call based on the provided schemas.

### Guidelines:
1. STRICT EXTRACTION: Only extract parameters explicitly present in the user prompt. DO NOT invent, hallucinate, or assume default values unless required by the schema.
2. TYPES & CONVERSION: Ensure extracted values strictly match the schema data types. Convert integer inputs to floats when expected by the function schema.
3. PATTERN MATCHING: Dynamically map minimal text patterns from the prompt to the correct argument fields logically.
4. STRICT OUTPUT FORMAT: Respond ONLY with a valid JSON object matching the requested schema. Do not include any explanations, markdown code blocks, or reasoning text.
5. not Duplicate val
### Output Schema:
{
  "name": "function_name",
  "arguments": { ... }
}

### User Input:
{USER_PROMPT}

### Output:
{
    "name" : "{FUNCTION_NAME}"
    "arguments: {PARAMETERS}\""""
