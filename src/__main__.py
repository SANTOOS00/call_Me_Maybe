from .parser import Parser
from .custom_error import Call_Error
from .llm_manager import ManagerLLM
from .generator import Generator

import sys


class Main:
    """Coordinate input parsing and function-call generation."""

    def __init__(self) -> None:
        """Initialize the application coordinator."""
        self.data: Parser

    def run(self) -> None:
        """Parse input data and generate the requested function calls."""
        self.parser()
        self.run_model()

    def parser(self) -> None:
        """Create the parser and load the application's input data."""
        self.data = Parser()
        self.data.run()

    def run_model(self) -> None:
        """Generate function calls from the parsed prompts and definitions."""
        model = ManagerLLM()
        generator = Generator(
            prompts=self.data.get_prompts,
            model=model,
            functions_definitions=self.data.functions_def,
        )
        generator.run(path=self.data.get_path_funcall_json())


if __name__ == "__main__":
    try:
        call_me_maybe = Main()
        call_me_maybe.run()
    except Call_Error as error:
        print(error, file=sys.stderr)
        print("++ erorr ++")
        print(Call_Error.string)
        sys.exit(1)
