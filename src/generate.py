# from llm_sdk.llm_sdk import Small_LLM_Model
# from src.parser.schema import Prompt
# from src.parser.schema import Function_Defn
# from dataclasses import dataclass

# @dataclass
# class FunctionCall:
#     prompt: str
#     function_name: str
#     arguments: dict
    
# class Generator:
#     def __init__(self, model: Small_LLM_Model, prompts: list[Prompt], function_definitions: list[Function_Defn]) -> None:
#         self.__model = model
#         self.__prompts: list[Prompt] = prompts
#         self.__functions_defintion: list[Function_Defn] = function_definitions
#         self.functions_call: list[FunctionCall] = list()

#     def generate(self) -> None:
#         for prompt in self.__prompts:
#             fn_name: str = self.__generate_function_name(prompt)
#             function_definition = self.__get_function_definition(fn_name)
#             if function_definition is not None:
#                 paraneters: dict = dict()
#                 self.__functions_defintion.append(FunctionCall(prompt=prompt, function_name=fn_name, arguments=paraneters))

#     def __generate_function_name(self, prompt: str) -> str:
#         return str()


#     def __get_function_definition(self, fn_name: str) -> Function_Defn | None:
#         for function_definition in self.__functions_defintions:
#             if function_definition.name == fn_name:
#                 return function_definition
#         return None

#     def __generate_arguments(self) -> None:
#         pass
