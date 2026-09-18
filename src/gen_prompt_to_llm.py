from .project_types import ArgType
from .model import Model
from .prompt_to_llm import PromptToLlm


class PromptLlm:
    """Generate LLM prompts for extracting function parameters.

    Attributes:
        model: The language model instance.
        function_prototype: The function signature.
        prompt: The user prompt.
        pre_value: Previously generated argument values.
    """

    def __init__(self, model: Model) -> None:
        """Initialize the prompt generator.

        Args:
            model: The language model instance.
        """
        self.model: Model = model
        self.function_prototype: str
        self.prompt: str
        self.pre_value: dict[str, ArgType]

    def __call__(
        self,
        current_name: str,
        current_type: str,
        function_prototype: str,
        prompt: str,
        pre_value: dict[str, ArgType],
    ) -> list[int]:
        """Generate token IDs for parameter extraction prompt.

        Args:
            current_name: The current parameter name.
            current_type: The current parameter type.
            function_prototype: The function signature.
            prompt: The user prompt.
            pre_value: Previously generated values.

        Returns:
            List of token IDs for the prompt.
        """
        self.function_prototype = function_prototype
        self.prompt = prompt
        self.pre_value = pre_value
        return self.__get_tokens_ids_prompt(current_name, current_type)

    def __get_tokens_ids_prompt(
        self, current_name: str, current_type: str
    ) -> list[int]:
        """Get token IDs for parameter extraction prompt.

        Args:
            current_name: The current parameter name.
            current_type: The current parameter type.

        Returns:
            List of token IDs.
        """

        def __get_arguments_format() -> str:
            """Format previously generated arguments.

            Returns:
                Formatted string of arguments in JSON-like format.
            """
            res: list[str] = list("{")
            for arg_name, arg_value in self.pre_value.items():
                res.append(f'"{arg_name}":{arg_value}, ')
            if_str: str = '"' if current_type == "string" else str()
            res.append(f'"{current_name}":{if_str}')
            return "".join(res)

        tokens: list[int] = self.model.ft_encode(
            PromptToLlm.GET_PRRAMETERS_FUNCTION.value.replace(
                "{FUNCTION}", self.function_prototype
            )
            .replace("{USER_PROMPT}", self.prompt)
            .replace("{ARGUMENTS}", __get_arguments_format())
        )
        return tokens
