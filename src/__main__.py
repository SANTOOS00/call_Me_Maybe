from .parser import Parser
from .custom_error import Call_Error
from .llm_manager import ManagerLLM
from .system_prompt import SystemPrompt
from .generator import Generator

import sys

class Main:
    data_input: Parser

    @classmethod
    def run(cls) -> None:
        cls.parser()
        cls.run_model()

    @classmethod
    def parser(cls) -> None:
        cls.data_input = Parser()
        cls.data_input.run()

    @classmethod
    def run_model(cls) -> None:
        systemprompt = SystemPrompt(cls.data_input.get_functions_def())
        model = ManagerLLM(
            system_prompt=systemprompt, 
            )
        generator = Generator(
            prompts=cls.data_input.get_prompts(),
            model=model
            )
        generator.run()


if __name__ == "__main__":
    try:
        Main.run()
    except Call_Error as error:
        print(error, file=sys.stderr)
        print("++ erorr ++")
        sys.exit(1)
