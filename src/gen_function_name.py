from .model import Model
from .prompt_to_llm import PromptToLlm
from .guidemodel import GuideModel
from .function_definition import FunctionDefinitionModel
from .stats_enum import StateGenString
from .gen_state import GenState
import numpy


class GenerateFunctionName:
    """Generate function names from user prompts using an LLM.

    Attributes:
        functions_call: Dictionary of available function calls.
        model: The language model used for generation.
        guider: Guide model for constraining valid tokens.
    """

    def __init__(
        self,
        functions_definition: dict[str, FunctionDefinitionModel],
        model: Model,  # model
        generate_state: GenState,
    ) -> None:  # Initialize the function name generator
        """Initialize the function name generator.

        Args:
            functions_call: Dictionary mapping function names to FunctionCall
            objects.
            model: The language model instance.
        """
        self.functions_definition: dict[str, FunctionDefinitionModel] = (
            functions_definition
        )
        self.model: Model = model
        self.generate_state: GenState = generate_state
        self.guider: GuideModel = GuideModel(
            self.__get_valid_tokens_function_name()
        )  # guider

    def __get_tokens_ids_prompt(self, prompt: str) -> list[int]:
        """Get token IDs for the function name prompt.

        Args:
            prompt: The user prompt.

        Returns:
            List of token IDs from encoding the prompt.
        """

        tokens: list[int] = self.model.ft_encode(
            PromptToLlm.GET_FUNCTION_NAME.value.replace(
                "{FUNCTIONS}", self.__join_all_function_call()
            ).replace("{PROMPT USER}", prompt)
        )

        return tokens

    def __get_valid_tokens_function_name(self) -> list[list[int]]:
        """Get valid token sequences for all available function names.

        Returns:
            List of token sequences, one for each function name.
        """
        valid_token: list[list[int]] = []
        for _, func in self.functions_definition.items():
            tokens: list[int] = self.model.ft_encode(f'{func.name}"')
            valid_token.append(tokens)
        return valid_token

    def __join_all_function_call(self) -> str:
        """Join all function calls into a formatted string.

        Returns:
            Newline-separated string of all function calls.
        """
        function_call: str = "\n".join(
            str(func) for _, func in self.functions_definition.items()
        )  # join function_call
        return function_call

    def get_function_name(self, prompt: str) -> str:
        """Generate a function name that matches the user prompt.

        Args:
            prompt: The user prompt.

        Returns:
            The selected function name.
        """
        tokens: list[int] = self.__get_tokens_ids_prompt(prompt)
        result: list[int] = []
        generated_value: str = str()
        while True:
            next_tokens, current_state = self.__get_next_possible_tokens(
                result, generated_value
            )
            if (
                not next_tokens
                or current_state == StateGenString.END
                or (
                    current_state == StateGenString.BODY
                    and len(generated_value) > len(prompt)
                )
            ):
                if '"' in generated_value:
                    quote_index: int = generated_value.index('"')
                    generated_value = generated_value[:quote_index]
                break
            logits = self.__mask_invalid_token(tokens + result, next_tokens)
            new_token_id = numpy.argmax(logits)
            result.append(int(new_token_id))
            generated_value = self.model.ft_decode(result)
        return generated_value

    def __get_next_possible_tokens(
        self, generated_ids: list[int], generated_value: str
    ) -> tuple[list[int], StateGenString]:
        next_possible_tokns: list[int] = self.guider.get_the_valid_tokens(generated_ids)
        state_generated: StateGenString = self.generate_state.set_state_string(
            generated_value
        )
        return next_possible_tokns, state_generated

    def __mask_invalid_token(
        self, tokens: list[int], valid_token: list[int]
    ) -> list[float]:
        """Mask logits for invalid tokens by setting them to negative infinity.

        Args:
                    tokens: List of token IDs.
                    valid_token: List of valid token indices.

                Returns:
                    List of logits with invalid tokens masked.
        """
        logits = self.model.ft_get_logits_from_input_ids(tokens)
        for i in range(len(logits)):
            if i not in valid_token:
                logits[i] = float("-inf")
        return logits
