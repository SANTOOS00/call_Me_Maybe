from .parser import Parser
from .custom_error import Call_Error
from .llm_manager import ManagerLLM
from .generator import Generator


import sys


class Main:
    def __init__(self) -> None:
        self.data: Parser

    def run(self) -> None:
        self.parser()
        self.run_model()

    def parser(self) -> None:
        self.data = Parser()
        self.data.run()

    def run_model(self) -> None:
        model = ManagerLLM()
        generator = Generator(
            prompts=self.data.get_prompts(),
            model=model,
            functions_defintions=self.data.functions_def,
            functions_defintions_json=self.data.functions_defintions_json,
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
