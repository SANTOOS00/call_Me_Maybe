# Contents of the file: /call_Me_Maybe/call_Me_Maybe/src/generator/module/promptproduct.py

class PromptProduct:
    PARAMETER_GENERATOR = """
    {
        "user_prompt": "{USER_PROMPT}",
        "function_name": "{FUNCTION_NAME}",
        "function_definition": {FUNCTION_DEFINITION},
        "parameters": {PARAMETERS}
    }
    """