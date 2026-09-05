from .parser import Parser
from .custom_error import Call_Error
from .llm_manager import ManagerLLM
from .system_prompt import SystemPrompt
from .generator import Generator
from .trie import Trie

import sys


class Main:
    data: Parser

    
    @classmethod
    def run(cls) -> None:
        cls.parser()
        cls.run_model()

    @classmethod
    def parser(cls) -> None:
        cls.data = Parser()
        cls.data.run()

    @classmethod
    def run_model(cls) -> None:
        systemprompt = SystemPrompt(cls.data.get_functions_def())
        model = ManagerLLM(
            system_prompt=systemprompt, 
            )
        generator = Generator(
            prompts=cls.data.get_prompts(),
            functions_dif=cls.data.get_functions_def(),
            model=model
            )
        generator.run()


if __name__ == "__main__":
    try:
        call_me_maybe = Main()
        call_me_maybe.run()
    except Call_Error as error:
        print(error, file=sys.stderr)
        print("++ erorr ++")
        print(Call_Error.string)
        sys.exit(1)
