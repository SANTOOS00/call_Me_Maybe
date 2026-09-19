from .module import FunctionNameGenerator, ParameterGenerator
from ..parser import Prompt, FunctionDefn
from ..llm_manager import ManagerLLM
from ..builderjson import FormatFunctionCalling, ProductJson


from pathlib import Path
import sys


class Generator:
    """Generate function-call JSON from prompts and function definitions."""

    def __init__(
        self,
        prompts: list[Prompt],
        functions_definitions: list[FunctionDefn],
        model: ManagerLLM,
    ) -> None:
        """Initialize the function-call generator.

        Args:
            prompts: User prompts to process.
            functions_definitions: Available function definitions.
            model: Language model used for generation.
        """

        self.prompts: list[Prompt] = prompts
        self.model: ManagerLLM = model
        self.functions_defintions: list[FunctionDefn] = functions_definitions
        self.generater_fun_name: FunctionNameGenerator = FunctionNameGenerator(
            model=self.model,
            functions_definitions=functions_definitions
        )
        self.productjson: ProductJson = ProductJson()

    def run(self, path: Path) -> None:
        """Generate and write function calls for every configured prompt.

        Args:
            path: Output file receiving the generated function calls.
        """
        for user_prompt in self.prompts:
            function: FunctionDefn | None = self.generater_fun_name.generate(
                user_prompt=user_prompt.prompt)
            if function is None:
                print("is not function definition", file=sys.stderr)
                sys.exit(1)
            generater_parameters: ParameterGenerator = ParameterGenerator(
                model=self.model,
                function_definition=function,
                prompt=user_prompt.prompt
            )
            generater_parameters.generate()
            function_calling: FormatFunctionCalling = FormatFunctionCalling(
                name=function.name,
                prompt=user_prompt.prompt,
                parameters=generater_parameters.valid_parameters
            )
            self.productjson.add_function(function_calling)
            self.productjson.write_in_file(path)
