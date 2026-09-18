from collections.abc import Generator
from .project_types import ArgType, TypeValue, T
from .stats_enum import StateGenString, StateGenNumber
from .gen_prompt_to_llm import PromptLlm
from .function_definition import FunctionDefinitionModel
from .gen_state import GenState
from .model import Model
import numpy


class GenerateArgFunction:
    """Generate function arguments using an LLM based on function signature and
    prompt.

    Attributes:
        model: The language model to use for generation.
        all_ids: List of token IDs for the current generation.
        function_call: The function call definition.
        prompt: The user prompt.
        promptllm: Prompt LLM generator.
        state_gen: State generator for tracking generation states.
    """

    def __init__(self, model: Model, generate_state: GenState) -> None:
        """Initialize the argument generator with a model.

        Args:
            model: The language model instance to use for generation.
        """
        self.model: Model = model
        self.all_ids: list[int]
        self.function_call: FunctionDefinitionModel
        self.prompt: str
        self.__gen_result: dict[str, ArgType]
        self.promptllm: PromptLlm = PromptLlm(self.model)
        self.state_gen: GenState = generate_state

    def __call__(
        self, function_call: FunctionDefinitionModel, prompt: str
    ) -> dict[str, ArgType]:  # Generate arguments
        """Generate arguments for a function call.

        Args:
            function_call: The function call definition.
            prompt: The user prompt.

        Returns:
            Dictionary of generated arguments.
        """
        self.function_call = function_call
        self.prompt = prompt
        self.__gen_result = dict()
        self.all_ids = list()
        return self.generate_arg()

    def generate_arg(self) -> dict[str, ArgType]:
        """Generate all function arguments based on their types.

        Returns:
            Dictionary mapping argument names to their generated values.
        """

        for name, type_n in self.__yield_arg_type():
            match type_n:
                case "number":
                    self.__gen_result[name] = self.__get_argument_number(
                        name, type_n, float
                    )
                case "integer":
                    self.__gen_result[name] = self.__get_argument_number(
                        name, type_n, int
                    )
                case "string":
                    self.__gen_result[name] = self.__get_argument_string(
                        name, type_n, str
                    )
                case "boolean":
                    self.__gen_result[name] = self.__get_argument_boolean(
                        name, type_n, bool
                    )
        return self.__gen_result

    def __get_promptllm_ids(self, name_arg: str, arg_type: str) -> list[int]:
        """Get token IDs from the LLM prompt generator.

        Args:
            name_arg: The name of the argument.
            arg_type: The type of the argument.

        Returns:
            List of token IDs from the LLM.
        """
        return self.promptllm(
            name_arg,
            arg_type,
            str(self.function_call),
            self.prompt,
            self.__gen_result,  # Prompt
        )

    # *******************generate number parameters********************

    def __get_argument_number(
        self, name_arg: str, arg_type: str, type_argument: type[T]
    ) -> T:
        """Generate a numeric argument using state machine guidance.

        Args:
            name_arg: The name of the argument.
            arg_type: The type of the argument (number or integer).
            type_argument: The Python type to convert to (int or float).

        Returns:
            The generated numeric argument.
        """
        state_number_gen: StateGenNumber = StateGenNumber.START
        argument_gen: str = ""
        self.all_ids = self.__get_promptllm_ids(name_arg, arg_type)
        while True:
            state_number_gen = self.state_gen.set_state_number(
                argument_gen, state_number_gen
            )
            if state_number_gen == StateGenNumber.END:
                if argument_gen.endswith(","):
                    index: int = argument_gen.index(",")
                    argument_gen = argument_gen[:index]
                break
            valid_token: list[int] = self.state_gen.get_valid_token(
                state_number_gen
            )  # valid token
            logits: list[float] = self.__mask_invalid_token(
                self.all_ids, valid_token
            )  # logits
            new_token_id: int = int(numpy.argmax(logits))
            self.all_ids.append(new_token_id)
            argument_gen += self.model.ft_decode([new_token_id])
        return type_argument(argument_gen)

    # *******************generate string parameters********************

    def __get_argument_string(
        self, name_arg: str, arg_type: str, type_argument: type[T]
    ) -> T:
        """Generate a string argument using state machine guidance.

        Args:
            name_arg: The name of the argument.
            arg_type: The type of the argument (string or boolean).
            type_argument: The Python type to convert to (str or bool).

        Returns:
            The generated string argument.
        """
        state_string_gen: StateGenString = StateGenString.START
        argument_gen: str = ""
        self.all_ids = self.__get_promptllm_ids(name_arg, arg_type)
        while True:
            state_string_gen = self.state_gen.set_state_string(argument_gen)
            if state_string_gen == StateGenString.END or (
                state_string_gen == StateGenString.BODY
                and len(argument_gen) > len(self.prompt)
            ):
                if '"' in argument_gen:
                    quote_index: int = argument_gen.index('"')
                    argument_gen = argument_gen[:quote_index]
                break
            logits: list[float] = self.model.ft_get_logits_from_input_ids(
                self.all_ids
            )  # logits
            new_token_id: int = int(numpy.argmax(logits))
            self.all_ids.append(new_token_id)
            argument_gen += self.model.ft_decode([new_token_id])
        return type_argument(argument_gen)

    # *******************generate boolean parameters********************

    def __get_argument_boolean(
        self, name_arg: str, arg_type: str, type_argument: type[T]
    ) -> T:
        """Generate a boolean argument.

        Args:
            name_arg: The name of the argument.
            arg_type: The type of the argument.
            type_argument: The Python type to convert to (bool).

        Returns:
            The generated boolean argument.
        """
        argument_gen: str = ""
        self.all_ids = self.__get_promptllm_ids(name_arg, arg_type)
        true_false: list[str] = ["True", "False"]
        true_false_ids: list[int] = self.model.ft_encode(" ".join(true_false))
        while True:
            if argument_gen in ["True", "False"]:
                break
            logits: list[float] = self.__mask_invalid_token(
                self.all_ids, true_false_ids
            )
            new_token_id: int = int(numpy.argmax(logits))
            self.all_ids.append(new_token_id)
            argument_gen += self.model.ft_decode([new_token_id])
        return type_argument(argument_gen)

    # ********************TOOLS****************

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
        logits: list[float] = self.model.ft_get_logits_from_input_ids(tokens)
        for i in range(len(logits)):
            if i not in valid_token:
                logits[i] = float("-inf")
        return logits

    def __yield_arg_type(self) -> Generator[tuple[str, TypeValue], None, None]:
        """Yield parameter names and their types from the function call.

        Yields:
            Tuples of (parameter_name, parameter_type).
        """
        for arg_name, type_ar in self.function_call.parameters.items():
            yield arg_name, type_ar.type_value
