from .parser import Parser
from .custom_error import Call_Error
from .llm_manager import ManagerLLM
from .system_prompt import SystemPrompt
from .generator import Generator
from .trie import Trie

import sys

class Main:
    data_input: Parser

    def run(self) -> None:
        self.parser()
        self.run_model()

    def parser(self) -> None:
        self.data_input = Parser()
        self.data_input.run()

    def run_model(self) -> None:
        self.init_trie()
        systemprompt = SystemPrompt(Main.data_input.get_functions_def())
        model = ManagerLLM(
            system_prompt=systemprompt, 
            )
        generator = Generator(
            prompts=Main.data_input.get_prompts(),
            model=model
            )
        generator.run()

    def init_trie(self) -> None:
        for 
        Trie().insert()


if __name__ == "__main__":
    try:
        call_me_maybe = Main()
        call_me_maybe.run()
    except BaseException as error:
        print(error, file=sys.stderr)
        print("++ erorr ++")
        print(Call_Error.string)
        sys.exit(1)
