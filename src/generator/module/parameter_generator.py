from ...parser import FunctionDefn
from ...llm_manager import ManagerLLM
from .promptproduct import PromptProduct

from typing import Dict, Literal, cast
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
        self.valid_paramters: Dict[str, int | str | bool | float] = {}
        self.context_window_ids: list[int]
        self.token: str

    def generate(self, function_definition: FunctionDefn, prompt: str) -> Dict[str, int | str | bool | float]:
        self.valid_paramters: Dict[str, int | str | bool | float] = {}
        for name_arg, type_val in function_definition.parameters.items():
            # parameters = self.builder_parameters(self.generater_valid_paramters, name_arg)
            # print(parameters)
            prompt_gengerater_parameters = self.builder_prompt(
                user_prompt=prompt,
                function_definition=function_definition
            )
            self.token = str()
            print(prompt_gengerater_parameters)
            self.context_window_ids = self.model.custom_encoder(prompt_gengerater_parameters)
            match type_val.type:
                case "number":
                    self.valid_paramters[name_arg] = self.__generater_numbers(name_arg)
                case "integer":
                    self.valid_paramters[name_arg] = self.__generater_numbers(name_arg)
                case "string":
                    self.valid_paramters[name_arg] = self.__generater_string(name_arg)
                case "boolean":
                    pass
                case _:
                    pass
        return self.valid_paramters

    def __generater_numbers(self, name_arg: str) -> float:
        model: ManagerLLM = self.model
        token = str()
        self.context_window_ids += model.custom_encoder(f"\"{name_arg}\": ")
        while True:
            next_token_possible: list[int] | None = self.__git_tokens_possible_number(token)
            if next_token_possible is None:
                break
            logits: list[float] = model.mask_logits(self.context_window_ids, next_token_possible)
            token_id = int(numpy.argmax(logits))
            token_string = model.decode_token(token_id)
            self.context_window_ids.append(token_id)
            token += token_string
            step = self.__get_step_generator_number(token)
            if step == NumberFSM.End_step:
                if "," in token:
                    index = token.index(",")
                    token = token[:index]
                break
        return float(token)

    def __generater_string(self, name_arg: str) -> str:
        model: ManagerLLM = self.model
        token = str()
        self.context_window_ids += model.custom_encoder(f"\"{name_arg}\": ")
        while True:
            logits = model.get_logits(self.context_window_ids)
            token_next_ids: int  = cast(int ,numpy.argmax(logits))
            self.context_window_ids.append(token_next_ids)
            token_string: str = model.decode_token(token_next_ids)
            token += token_string
            print(token)
            if self.__get_step_generator_string(token) == StringFSM.Fini_step:
                if '"' in token:
                    index = token.rfind('"')
                    token = token[:index]
                break
        return token

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
        conut_char = 0
        for ch in string:
            match step_generator:
                case StringFSM.Start_step:
                    if ch == "\\":
                        step_generator = StringFSM.Escape_step
                    else:
                        step_generator = StringFSM.Content_step
                case StringFSM.Content_step:
                    if ch == "\\":
                        step_generator = StringFSM.Escape_step
                    elif ch == '"' and conut_char:
                        return StringFSM.Fini_step
                    else:
                        conut_char += 1
                case StringFSM.Escape_step:
                    step_generator = StringFSM.Content_step
                case StringFSM.Fini_step:
                    return StringFSM.Fini_step
        return step_generator
    
    def __get_step_generator_number(self, number: str) -> NumberFSM:
        step_generator: NumberFSM = NumberFSM.Start_step
        cont_decmal = 0
        cont_number = 0
        for nu in number:
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
                    elif nu == ',':
                        return NumberFSM.End_step
                    else:
                        cont_number += 1
                case NumberFSM.Decimal_step:
                    if nu == ',' and cont_decmal:
                        return NumberFSM.End_step
                    cont_decmal += 1
                case NumberFSM.End_step:
                    return step_generator
        print(step_generator, number)
        return step_generator

    def clean(self) -> None:
        self.context_window_ids: list[int] = list()

    def builder_prompt(
        self,
        user_prompt: str,
        function_definition: FunctionDefn) -> str:

        formatted_params = ", ".join(
            f"\"{key}\": {val.type}"
            for key, val in function_definition.parameters.items()
        )

        format_param_generator = ", ".join(
            f"{key}: {val}"
            for key, val in self.valid_paramters.items()
        )

        if format_param_generator:
            format_param_generator += ","

        return PromptProduct.PARAMETER_GENERATOR.replace(
            "{USER_PROMPT}", user_prompt
        ).replace(
            "{FUNCTION_NAME}", function_definition.name
        ).replace(
            "{PARAMETERS}", format_param_generator
        )
