from .promptproduct import PromptProduct
from ...llm_manager import ManagerLLM
from ...parser import FunctionDefn



from enum import Enum, auto
from typing import Dict, Literal, TypeAlias
import numpy

SCHEMA_TYPES: TypeAlias = Literal["number", "string", "boolean", "integer"]
ParameterValue = int | str | bool | float


class NumberFSM(Enum):
    START = auto()
    SIGN = auto()
    INTEGER = auto()
    DECIMAL = auto()
    END = auto()


class StringFSM(Enum):
    START = auto()
    CONTENT = auto()
    ESCAPE = auto()
    END = auto()


class ParameterGenerator:
    def __init__(self,
                 model: ManagerLLM,
                 function_definition: FunctionDefn,
                 prompt: str) -> None:
        self.model = model
        self.valid_parameters: Dict[str, ParameterValue] = {}
        self.context_window_ids: list[int] = []
        self.function_definition: FunctionDefn = function_definition
        self.prompt: str = prompt

    def generate(self) -> None:
        for name, argtype in self.function_definition.parameters.items():
            parameter_prompt = self.builder_prompt(
                user_prompt=self.prompt,
                function_definition=self.function_definition,
                arg_name=name,
                arg_value=argtype.type,
            )
            print(parameter_prompt, end="", flush=True)
            self.context_window_ids = self.model.custom_encoder(
                parameter_prompt)
            match argtype.type:
                case "string":
                    value = self.__generate_string(len(self.prompt))
                case "number":
                    value = float(self.__generate_number())
                case "integer":
                    value = int(self.__generate_number())
                case "boolean":
                    value = self.__generate_boolean()
                case _:
                    pass
            self.valid_parameters[name] = value

    def __generate_string(self, prompt_len: int) -> str:
        current_state: StringFSM
        generated_value:  str = str()
        while True:
            logits: list[float] = self.model.mask_logits(
                self.context_window_ids)
            token_id: int = int(numpy.argmax(logits))
            token: str = self.model.decode_token(token_id)
            generated_value += token
            current_state = self.__get_string_fsm_state(generated_value,
                                                        prompt_len)
            self.context_window_ids.append(token_id)
            if current_state == StringFSM.END:
                if '"' in generated_value:
                    idx_quotes: int = generated_value.index('"')
                    generated_value = generated_value[:idx_quotes]
                break
            print(token, end="", flush=True)
        return generated_value

    def __generate_boolean(self) -> bool:
        model = self.model
        possible_tokens: list[int] = model.encoder_chr_by_chr(["false",
                                                               "true"])
        logit: list[float] = model.mask_logits(self.context_window_ids,
                                               possible_tokens)
        token: int = int(numpy.argmax(logit))
        return model.decode_token(token) == "true"

    def __generate_number(self) -> float:
        generated: str = ""
        while True:
            token_possible: list[int] = self.__possible_number_tokens(
                generated)
            logits: list[float] = self.model.mask_logits(
                self.context_window_ids, token_possible)
            token_id = int(numpy.argmax(logits))
            token = self.model.decode_token(token_id)
            self.context_window_ids.append(token_id)
            generated += token
            current_state: NumberFSM = self._number_state(generated)
            if current_state == NumberFSM.END:
                if "," in generated:
                    index = generated.rindex(",")
                    generated = generated[:index]
                break
            print(token, end="", flush=True)
        return float(generated)

    def __possible_number_tokens(self, number: str) -> list[int]:
        characters: list[str]
        state: NumberFSM = self._number_state(number)
        if state == NumberFSM.START:
            characters = list("-+0123456789")
        elif state == NumberFSM.SIGN:
            characters = list("0123456789")
        elif state == NumberFSM.INTEGER:
            characters = list("0123456789.,")
        elif state == NumberFSM.DECIMAL:
            characters = list("0123456789,")
        else:
            characters = list(",")
        return self.model.encoder_chr_by_chr(characters)

    def _number_state(self, number: str) -> NumberFSM:
        step_generator: NumberFSM = NumberFSM.START
        cont_decmal: int = 0
        cont_number: int = 0
        for nu in number:
            match step_generator:
                case NumberFSM.START:
                    if nu in "-+":
                        step_generator = NumberFSM.SIGN
                    else:
                        step_generator = NumberFSM.INTEGER
                case NumberFSM.SIGN:
                    step_generator = NumberFSM.INTEGER
                case NumberFSM.INTEGER:
                    if nu == '.':
                        step_generator = NumberFSM.DECIMAL
                    elif nu == ',' or cont_number > 5:
                        step_generator = NumberFSM.END
                    else:
                        cont_number += 1
                case NumberFSM.DECIMAL:
                    if (nu == ',' and cont_decmal) or cont_decmal > 5:
                        step_generator = NumberFSM.END
                    cont_decmal += 1
                case NumberFSM.END:
                    return step_generator
        return step_generator

    def __get_string_fsm_state(self, string: str, max_len: int) -> StringFSM:
        current_state: StringFSM = StringFSM.START
        for ch in string:
            match current_state:
                case StringFSM.START:
                    if ch == '\\':
                        current_state = StringFSM.ESCAPE
                    elif ch == '"':
                        current_state = StringFSM.END
                    else:
                        current_state = StringFSM.CONTENT
                case StringFSM.CONTENT:
                    if ch == '\\':
                        current_state = StringFSM.ESCAPE
                    elif len(string) >= max_len:
                        current_state = current_state.END
                    elif ch == '"':
                        current_state = StringFSM.END
                case StringFSM.ESCAPE:
                    current_state = StringFSM.CONTENT
                case StringFSM.END:
                    ...
        return current_state

    def builder_prompt(
            self,
            user_prompt: str,
            function_definition: FunctionDefn,
            arg_name: str,
            arg_value: SCHEMA_TYPES
            ) -> str:
        arguments: str = function_definition.get_pre_generated_argument_format(
            self.valid_parameters, (arg_name, arg_value))
        return (
            PromptProduct.PARAMETER_GENERATOR
            .replace("{USER_PROMPT}", user_prompt)
            .replace("{FUNCTION_NAME}", function_definition.name)
            .replace("{FUNCTION_DESCRIPTION}",
                     function_definition.description)
            .replace("{FUNCTION_PROTOTYPE}", str(function_definition))
            .replace("{ARGUMENTS}", arguments)
        )
