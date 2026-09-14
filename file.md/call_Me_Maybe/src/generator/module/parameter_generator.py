from ...parser import FunctionDefn
from ...llm_manager import ManagerLLM
from .promptproduct import PromptProduct

from typing import Dict, cast, Union
from enum import Enum, auto
import numpy

class StringFSM(Enum):
    Start_step = auto()
    Escape_step = auto()
    Content_step = auto()
    Fini_step = auto()


class NumberFSM(Enum):
    Start_step = auto()
    Sign_step = auto()
    Decimal_step = auto()
    Number_step = auto()
    End_step = auto()


class ParameterGenerator:
    def __init__(self, model: ManagerLLM) -> None:
        self.model: ManagerLLM = model
        self.valid_parameters: Dict[str, int | str | bool | float] = {}
        self.context_window_ids: list[int]

    def generate(self, function_definition: FunctionDefn, prompt: str) -> Dict[str, int | str | bool | float]:
        self.valid_parameters: Dict[str, int | str | bool | float] = {}
        for name_arg, type_val in function_definition.parameters.items():
            prompt_gengerater_parameters = self.builder_prompt(
                user_prompt=prompt,
                function_definition=function_definition
            )
            print(prompt_gengerater_parameters)
            self.context_window_ids = self.model.custom_encoder(prompt_gengerater_parameters)
            match type_val.type:
                case "string":
                    self.valid_parameters[name_arg] = self.__generater_string(name_arg, prompt)
                case "number":
                    self.valid_parameters[name_arg] = self.__generater_numbers(name_arg)
                case "integer":
                    self.valid_parameters[name_arg] = int(self.__generater_numbers(name_arg))
                case "boolean":
                    self.valid_parameters[name_arg] = self.__generater_boolean()
                case _:
                    pass
        return self.valid_parameters

    def __generater_string(self, name_arg: str, prompt: str) -> str:
        model: ManagerLLM = self.model
        token = str()

        prefix = f'"{name_arg}": ' if not self.valid_parameters else f', "{name_arg}": '
        
        self.context_window_ids += model.custom_encoder(prefix)
        
        while True:
            logits = model.get_logits(self.context_window_ids)
            token_next_ids: int = cast(int, numpy.argmax(logits))
            self.context_window_ids.append(token_next_ids)
            token_string: str = model.decode_token(token_next_ids)
            token += token_string
            
            current_state: StringFSM = self.__get_step_generator_string(token)
            if current_state == StringFSM.Fini_step or (current_state == StringFSM.Content_step and len(token) >= len(prompt) + 10):
                break
        return token

    def builder_prompt(
            self,
            user_prompt: str,
            function_definition: FunctionDefn
        ) -> str:

            def __get_forma_json(function_definition: FunctionDefn) -> str:
                params_list = [
                    f'"{key}": "{val.type}"'
                    for key, val in function_definition.parameters.items()
                ]
                parameters_formatted = ", ".join(params_list)
                
                return (
                    f'"name": "{function_definition.name}", '
                    f'"description": "{function_definition.description}", '
                    f'"parameters": {parameters_formatted}'
                )

            def __get_form_parameters(parameters: Dict[str, Union[int, float, str, bool]]) -> str:
                if not parameters:
                    return ""
                return str(parameters)

            return (
                PromptProduct.PARAMETER_GENERATOR
                .replace("{USER_PROMPT}", user_prompt)
                .replace("{FUNCTION_NAME}", function_definition.name)
                .replace("{FUNCTION_DEFINITION}", __get_forma_json(function_definition))
                .replace("{PARAMETERS}", __get_form_parameters(self.valid_parameters))
            )

    def __generater_boolean(self) -> bool:
        return True

    def __generater_numbers(self, name_arg: str) -> float:
        model: ManagerLLM = self.model
        token = str()
        prefix = f'"{name_arg}": ' if not self.valid_parameters else f', "{name_arg}": '
        self.context_window_ids += model.custom_encoder(prefix)
        while True:
            next_token_possible: list[int] | None = self.__git_tokens_possible_number(token)
            if next_token_possible is None:
                break
            logits: list[float] = model.mask_logits(self.context_window_ids, next_token_possible)
            token_id = int(numpy.argmax(logits))
            token_string = model.decode_token(token_id)
            self.context_window_ids.append(token_id)
            token += token_string
            print(token)
            step = self.__get_step_generator_number(token)
            if step == NumberFSM.End_step:
                if "," in token:
                    index = token.index(",")
                    token = token[:index]
                break
        return float(token)

    def __git_tokens_possible_number(self, number: str) -> list[int] | None:
        step_generator = self.__get_step_generator_number(number)
        match step_generator:
            case NumberFSM.Start_step:
                return self.model.encoder_chr_by_chr("-+1234567890")
            case NumberFSM.Sign_step:
                return self.model.encoder_chr_by_chr("1234567890")
            case NumberFSM.Number_step:
                return self.model.encoder_chr_by_chr("1234567890,.")
            case NumberFSM.Decimal_step:
                return self.model.encoder_chr_by_chr("1234567890,")
            case NumberFSM.End_step:
                return None

    def __get_step_generator_string(self, string: str) -> StringFSM:
        
        step_generator: StringFSM = StringFSM.Start_step
        for ch in string:
            match step_generator:
                case StringFSM.Start_step:
                    step_generator = StringFSM.Content_step
                case StringFSM.Content_step:
                    if ch == ',' or ch == '\n':
                        return StringFSM.Fini_step
                case StringFSM.Fini_step:
                    return StringFSM.Fini_step
        return step_generator

    def __get_step_generator_number(self, number: str) -> NumberFSM:
        step_generator: NumberFSM = NumberFSM.Start_step
        cont_decmal = 0
        cont_number = 0
        for nu in number:
            print(cont_number, cont_decmal)
            match step_generator:
                case NumberFSM.Start_step:
                    if nu in "-+":
                        step_generator = NumberFSM.Sign_step
                    else:
                        step_generator = NumberFSM.Number_step
                case NumberFSM.Sign_step:
                    step_generator = NumberFSM.Number_step
                case NumberFSM.Number_step:
                    if nu == '.' and cont_number != 0:
                        step_generator = NumberFSM.Decimal_step
                    elif nu == ',' or cont_number > 5:
                        return NumberFSM.End_step
                    else:
                        cont_number += 1
                case NumberFSM.Decimal_step:
                    if nu == ',' or cont_decmal > 5:
                        return NumberFSM.End_step
                    cont_decmal += 1

                case NumberFSM.End_step:
                    return step_generator

        return step_generator