from .parser import Parser
from .custom_error import Call_Error
from .llm_manager import GenerterLLM

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
        funs_defin = cls.data_input.get_functions_def()
        prompts = cls.data_input.get_prompts()
        model = GenerterLLM(
            functions_difiniton=funs_defin,
            prompts=prompts
            )
        model.run()



if __name__ == "__main__":
    try:
        Main.run()
    except Call_Error as error:
        print(error, file=sys.stderr)
        print("++ erorr ++")
        sys.exit(1)
