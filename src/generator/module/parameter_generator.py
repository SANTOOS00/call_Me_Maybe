from ...parser import FunctionDefn
from ...llm_manager import ManagerLLM
from .promptproduct import PromptProduct

from typing import Dict, Literal, cast
import numpy


class ParameterGenerator:
    def __init__(self, model: ManagerLLM) -> None:
        self.model: ManagerLLM = model
        self.generater_valid_paramters: Dict[str, int | str | bool] = {}
        self.context_window_ids: list[int]

    def generate(self, function_definition: FunctionDefn, prompt: str) -> Dict[str, int | str | bool]:
        for name_arg, type_val in function_definition.parameters.items():
            match type_val.type:
                case "string":
                    ## nht fih axno radi decode fiha bnfash val exapmle int and str and float
                    self.generater_valid_paramters[name_arg] = self.generater_val(
                        val_arg=str,
                        function_definition=function_definition,
                        user_prompt=prompt)
                    print(self.generater_valid_paramters[name_arg])
                case "number":
                    # self.generater_valid_paramters[key_parameter] = self.generater_val(val_arg.type)
                    pass
                case "int":
                    # self.generater_valid_paramters[key_parameter] = self.generater_val(val_arg.type)
                    pass
                case "boolean":
                    # self.generater_valid_paramters[key_parameter] = self.generater_val(val_arg.type)     
                    pass
                case _:
                    pass
        return self.generater_valid_paramters

    def generater_val(self,
                     val_arg: str | bool | float,
                     function_definition: FunctionDefn,
                     user_prompt: str) -> str | int | float | bool:
        self.clean()
        model: ManagerLLM = self.model
        next_tokens = ""
        global_prompt: str = self.builder_prompt(
            user_prompt=user_prompt,
            description=function_definition.description,
            function_name=function_definition.name
        )
        self.context_window_ids = model.custom_encoder(global_prompt)
        token_prompt : list[int] = model.custom_encoder(user_prompt)
        while len(user_prompt) >= len(next_tokens):
            logits = model.mask_logits(self.context_window_ids, token_prompt)
            token_next_ids: int  = cast(int ,numpy.argmax(logits))
            self.context_window_ids.append(token_next_ids)
            token_str_next = model.decode_token(token_next_ids)
            next_tokens += token_str_next
        return next_tokens
    
    def clean(self) -> None:
        self.context_window_ids: list[int] = list()


    def builder_prompt(self,
                       user_prompt: str,
                       description: str,
                       function_name: str) -> str:
        return PromptProduct.PARAMETER.replace(
            "{function_name}", function_name
        ).replace(
            "{user_prompt}", user_prompt,  
        ).replace(
            "{description_method}", description
        )
