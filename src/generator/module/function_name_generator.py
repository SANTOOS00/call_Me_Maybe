from src.llm_manager.generatermodel import ManagerLLM
from .promptproduct import PromptProduct
from ...parser import FunctionDefn
from ...trie import Trie


import json
import numpy


class FunctionNameGenerator:
    """Generate a function name constrained by available definitions."""

    def __init__(
        self,
        model: ManagerLLM,
        functions_definitions: list[FunctionDefn]
    ) -> None:
        """Initialize constrained function-name generation.

        Args:
            model: Language model used for generation.
            functions_definitions: Candidate function definitions.
        """
        self.model: ManagerLLM = model
        self.trie: Trie = Trie()
        self.functions_definitions: list[FunctionDefn] = functions_definitions

        self.context_window_ids: list[int]
        self.generated_ids: list[int] = list()
        self.set_functions_names_ids_to_trie()

    def generate(self, user_prompt: str) -> FunctionDefn | None:
        """Generate the function definition matching a user prompt.

        Args:
            user_prompt: User request used to select a function.

        Returns:
            Matching function definition, or ``None`` if no match is found.
        """
        def __check_fini_generator(tokens_str: str) -> bool:
            """Check whether generated text identifies a complete function."""
            token_id: list[int] = self.model.custom_encoder(tokens_str)
            return self.trie.search(token_id)
        self.clean()
        global_prompt: str = self.__build_prompt(user_prompt)

        self.context_window_ids = self.model.custom_encoder(global_prompt)
        while True:
            high_scores: list[int] = self.trie.get_children(self.generated_ids)
            if len(high_scores) == 0:
                break
            logits: list[float] = self.model.mask_logits(
                self.context_window_ids, high_scores
            )
            next_token_id: int = int(numpy.argmax(logits))
            next_token: str = self.model.decode([next_token_id])
            self.context_window_ids.append(next_token_id)
            self.generated_ids.append(next_token_id)
            self.function_name += next_token
            if __check_fini_generator(self.function_name):
                break
        return self.__get_function_definition()

    def __get_function_definition(self) -> FunctionDefn | None:
        """Find the definition matching the generated function name.

        Returns:
            Matching function definition, or ``None`` if absent.
        """
        for fun in self.functions_definitions:
            if fun.name == self.function_name[:-1]:
                return fun
        return None

    def clean(self) -> None:
        """Reset generated token and function-name state."""
        self.context_window_ids = list()
        self.generated_ids = list()
        self.function_name: str = str()

    def __build_prompt(self, user_prompt: str) -> str:
        """Build the model prompt containing available function definitions.

        Args:
            user_prompt: User request to include in the prompt.

        Returns:
            Function-selection prompt text.
        """
        function_definitions = [
            function.model_dump() for function in self.functions_definitions
        ]
        return PromptProduct.FUNCTION_NAME.replace(
            "{user_prompt}", user_prompt
        ).replace(
            "{FUNCTION_DEFINITIONS}", json.dumps(function_definitions,
                                                 indent=2)
        )

    def set_functions_names_ids_to_trie(self) -> None:
        """Add tokenized function names to the prefix trie."""
        functions_names_ids: list[list[int]] = list()
        for fn_def in self.functions_definitions:
            name_ids: list[int] = self.model.custom_encoder(fn_def.name)
            name_ids.append(self.model.custom_encoder('"')[0])
            functions_names_ids.append(name_ids)
        self.trie.insert_many(functions_names_ids)
