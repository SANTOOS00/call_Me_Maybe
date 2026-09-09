from ...trie import Trie 
from ...parser import FunctionDefn

class Parameter_generator:
    def __init__(self,
                 functions_definitions: list[FunctionDefn]) -> None:
        self.trie = Trie()
        self.functione_definitions = functions_definitions

    def generator(self) -> None:
        pass

    def set_parameters_ids_to_trie(self) -> None:
        pass

