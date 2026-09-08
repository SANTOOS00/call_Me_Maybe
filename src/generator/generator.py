from ..parser import Prompt, FunctionDefn
from ..llm_manager import  ManagerLLM
from ..system_prompt import Steps
from ..builderjson import FunCallBuilder
from ..trie import Trie
from ..system_prompt import SystemPrompt


import numpy as np # type: ignore[import-untyped, unused-ignore]
from typing import List, Dict, Any


class Tokenizer(FunCallBuilder):
    def __init__(self,
                 functions_def: List[FunctionDefn]
                 ) -> None:
        self.tokens: str = ""
        self.trie = Trie()
        self.functions_def = functions_def


    def check_valid_tokens(self, step: Steps) -> bool:
        match step.value:
            case Steps.FUNCTION_ROUTER.value:
                self._initialize_step_data(step)
                return self.valid_tokenizer()
            case Steps.PARAMETER_IDENTIFIER.value:
                self._initialize_step_data(step)
                return self.valid_tokenizer()
            case Steps.VALUE_EXTRACTOR.value:
                self._initialize_step_data(step)
                return self.valid_parameter()
        return True

    def valid_parameter(self) -> bool:
        print(self.tokens)
        return False

    def _initialize_step_data(self,
                              current_step: Steps
                              ) -> None:
        self.trie.clean_trie()
        match current_step.value:
            case Steps.FUNCTION_ROUTER.value:
                self.populate_trie_with_function_names()
            case Steps.PARAMETER_IDENTIFIER.value:
                self.populate_trie_with_parameters()
                  
    def valid_tokenizer(self) -> bool:
        trie = self.trie
        for ch in self.tokens:
            if trie.isPrefix(self.tokens):
                return trie.search(self.tokens)
            else:

                self.tokens = self.tokens.replace(ch, "", 1)
        return False

    def get_parameters(self) -> List[Dict[str, Any]]:
            return [
                function.parameters
                for function in self.functions_def
            ]

    def populate_trie_with_parameters(self) -> None:
        formatted_params = []
        for param_dict in self.get_parameters():
            param_str = ", ".join([f"{key}: {val.type}" for key, val in param_dict.items()])
            if param_str:
                formatted_params.append(param_str)
        for parameter in formatted_params:
            self.trie.insert(parameter)

    def populate_trie_with_function_names(self) -> None:
        trie = self.trie
        for fun in self.functions_def:  
            trie.insert(fun.name)

    def get_token(self) -> str:
        return self.tokens

    def set_name_function(self) -> None:
        return super().set_name_function(self.get_token())

    def clean(self) -> None:
        self.tokens = ""
        super().clean()
        self.trie.clean_trie()

    def add_token(self, token: str) -> None:
        self.tokens += token


class Generator:
    def __init__(self,
                 prompts: List[Prompt],
                 system_prompt: SystemPrompt,
                 tokenizes: Tokenizer,
                 model: ManagerLLM
                 ) -> None:
        self.generator_ids: List[int] = []
        self.__prompts: List[Prompt] = prompts
        self.system_prompt = system_prompt
        self.tokenizes = tokenizes
        self.model = model

    def clean_genertor_ids(self) -> None:
        self.generator_ids: List[int] = []

    def run(self) -> None:
        for prompt in self.__prompts:
            self.generate_for_prompt(prompt.prompt)

    def clean(self) -> None:
        self.tokenizes.clean()

    def generate_for_prompt(self, prompt: str) -> None:
        tokenizes = self.tokenizes
        model = self.model
        for step in Steps:
            prompt_str = self.system_prompt.get_step_generator(step, prompt, tokenizes.get_token())
            self.clean()
            prompt_ids: List[int] = model.get_prompt_ids(prompt_str)
            self.generator_ids = prompt_ids
            while True:
                logits: List[float] = model.get_logits(self.generator_ids)
                high_score_id = int(np.argmax(logits))
                self.add_next_token(high_score_id)
                tokenizes.add_token(model.decode_token(high_score_id))
                if tokenizes.check_valid_tokens(step):
                    # if step.value == Steps.FUNCTION_ROUTER.value:
                    tokenizes.set_name_function()
                    tokenizes.set_prompt(prompt)
                    tokenizes.prints()
                    break

    def add_next_token(self, token_id: int) -> None:
        self.generator_ids.append(token_id)


# My model is hallucinating, so I’m going to fix it by making sure it doesn’t exceed a certain maximum token limit.

