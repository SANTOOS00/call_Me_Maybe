from ...trie import Trie 
from ...parser import FunctionDefn

class ParameterGenerator:
    def __init__(self,
                 trie: Trie,
                 functions_definitions: list[FunctionDefn]) -> None:
        self.functione_definitions = functions_definitions

    def generator(self) -> None:
        pass

    def set_parameters_ids_to_trie(self) -> None:
        pass

    def builder_prompt(self) -> None:
        pass

    