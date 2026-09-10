from ...trie import Trie 
from ...parser import FunctionDefn
from ...trie import Trie
from typing import Dict, Any, Literal


class ParameterGenerator:
    def __init__(self) -> None:
        self.generater_valid_paramters: Dict[str, int | str | bool] = {}

    def generate(self, function_definition: FunctionDefn | None, prompt: str) -> Dict[str, int | str | bool]:
        for key_parameter, type_val in function_definition.parameters.items():
            print(key_parameter)
            match type_val.type:
                case "string":
                    self.generater_valid_paramters[key_parameter] = self.generater_val(key_parameter)
                case "number":
                    self.generater_valid_paramters[key_parameter] = self.generater_val(key_parameter)
                case "int":
                    self.generater_valid_paramters[key_parameter] = self.generater_val(key_parameter)
                case "boolean":
                    self.generater_valid_paramters[key_parameter] = self.generater_val(key_parameter)     
                case _:
                    pass
        return self.generater_valid_paramters

    def generater_val(self,
                     parameter: str
                     ) -> str:
        # print(parameter)
        return parameter

    def builder_prompt(self) -> None:
        pass
