from ...parser import FunctionDefn
from ...llm_manager import ManagerLLM
from .promptproduct import PromptProduct

from typing import Dict, Literal, cast
from enum import Enum, auto
import numpy



class NumberFSM(Enum):
    Start_step = auto()
    Sign_step = auto()
    Decimal_step = auto()
    Number_step = auto()
    End_step = auto()

class ParameterGenerator:
    def __init__(self, model: ManagerLLM) -> None:
        self.model: ManagerLLM = model
        self.generater_valid_paramters: Dict[str, int | str | bool] = {}
        self.context_window_ids: list[int]

    def generate(self, function_definition: FunctionDefn, prompt: str) -> Dict[str, int | str | bool]:
        for name_arg, type_val in function_definition.parameters.items():
            # self.context_window_ids = self.model.custom_encoder(self.builder_prompt(
            #     user_prompt=prompt,
            #     function_name=function_definition.name,
            #     parameter=self.generater_valid_paramters + name_arg,
            #     description=function_definition.description,
            # ))
            print(self.builder_prompt(
                            user_prompt=prompt,
                            function_name=function_definition.name,
                            parameter=str(self.generater_valid_paramters) + name_arg,
                            description=function_definition.description))
            # match type_val.type:
            #     case "string":
            #         self.generater_valid_paramters[name_arg] = self.__generater_string(
            #             function_definition=function_definition,
            #             user_prompt=prompt)
            #     case "number":
            #         self.generater_valid_paramters[name_arg] = self.__generater_numbers(float, prompt, name_arg)
            #     case "integer":
            #         self.generater_valid_paramters[name_arg] = self.__generater_numbers(int, prompt, name_arg)
            #     case "boolean":
            #         pass
            #     case _:
            #         pass
        return self.generater_valid_paramters

    def __generater_numbers(self, type: float | int,prompt: str, name_arg: str) -> float:
        model = self.model
        token = str()
        while True:
            next_token_possible: list[int] = self.__git_tokens_possible(token)
            if next_token_possible == [] or len(token) <= len(prompt):
                break
            logits: list[int] = model.mask_logits(self.context_window_ids, next_token_possible)


    def __git_tokens_possible(self, number: str) -> list[int]:
        step_generator = self.__get_step_generator_number(number)
        match step_generator:
            case NumberFSM.start_step:
                return self.model.encoder_chr_by_chr("+-1234567890")
            case NumberFSM.Sing_step:
                return self.model.encoder_chr_by_chr("1234567890")
            case NumberFSM.Number_step:
                return self.model.encoder_chr_by_chr("1234567890.,")
            case NumberFSM.Decimal_step:
                return self.model.encoder_chr_by_chr("1234567890,")
            case NumberFSM.End_step:
                return []

    def clean(self) -> None:
        self.context_window_ids: list[int] = list()

    def builder_prompt(self,
                       user_prompt: str,
                       description: str,
                       parameter: str,
                       function_name: str) -> str:
        return PromptProduct.PARAMETER.replace(
            "{function_name}", function_name
        ).replace(
            "{user_prompt}", user_prompt,  
        ).replace(
            "{description_method}", description
        ).replace(
            "{parameter}", parameter
        )

    def __get_step_generator_number(self, number: str) -> NumberFSM:
        step_generator: NumberFSM = NumberFSM.Start_step
        cont_decmal = 0
        cont_number = 0
        for nu in number:
            match step_generator:
                case NumberFSM.Sign_step:
                    if nu in "-+":
                        step_generator = NumberFSM.Sign_step
                    else:
                        step_generator = NumberFSM.Number_step
                case NumberFSM.Sign_step:
                    step_generator = NumberFSM.Number_step
                case NumberFSM.Number_step:
                    if nu == '.' and cont_decmal != 0:
                        step_generater = NumberFSM.Decimal_step
                    elif nu == ',' and cont_decmal != 0:
                        step_generater = NumberFSM.End_step
                    cont_number += 1
                case NumberFSM.Decimal_step:
                    if nu == ',' and cont_number != 0:
                        step_generator = NumberFSM.End_step
                    cont_decmal += 1
                case NumberFSM.End_step:
                    return step_generator
        return step_generator
    def __generater_string(self,
                           function_definition: FunctionDefn,
                           user_prompt: str) -> str | int | float | bool:
        # self.clean()
        # model: ManagerLLM = self.model
        # next_tokens = ""
        # global_prompt: str = self.builder_prompt(
        #     user_prompt=user_prompt,
        #     description=function_definition.description,
        #     function_name=function_definition.name
        # )
        
        # self.context_window_ids = model.custom_encoder(global_prompt)
        # token_prompt : list[int] = model.custom_encoder(user_prompt)
        # while len(user_prompt) >= len(next_tokens):
        #     logits = model.mask_logits(self.context_window_ids, token_prompt)
        #     token_next_ids: int  = cast(int ,numpy.argmax(logits))
        #     self.context_window_ids.append(token_next_ids)
        #     token_str_next = model.decode_token(token_next_ids)
        #     next_tokens += token_str_next
        return 11