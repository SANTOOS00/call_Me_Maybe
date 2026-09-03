# 1. Neffdo l-variables dialna
function_description = "Fetches the current weather for a given city."
user_prompt = "What's the weather like in Casablanca today?"

# 2. Katktd l-string w katzeed 'f' f l-bdik (f-string)
function_argument_dynamic = f"""
    Function:
    {function}

    Description:
    {function_description}

    User request:
    {user_prompt}
    <|im_end|>

    Answer:
    """

print(function_argument_dynamic)