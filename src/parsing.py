from argparse import Action, ArgumentParser, Namespace
from .prompt import Prompt, PromptRootModel
from .path import PathData
from typing import cast
from .function_definition import (
    FunctionDefinitionModel,
    FunctionDefinitionRootModel,
)
from .filemanager import FileManager
import json


class Parsing:
    """Parse command-line arguments for file paths and configuration."""

    def __init__(self, argv: list[str]) -> None:
        """Initialize the parser with command-line arguments."""
        self.__argv: list[str] = argv
        self.file_manager: FileManager = FileManager()
        self.path: PathData = PathData()
        self.__get_path_data()

    def __get_path_data(self) -> None:
        """Parse and process command-line arguments."""
        argparser: ArgumentParser = ArgumentParser()
        _: Action = argparser.add_argument(
            "--functions_definition",
            type=str,
            default="data/input/functions_definition.json",
        )
        _: Action = argparser.add_argument(
            "--input",
            type=str,
            default="data/input/function_calling_tests.json",
        )
        _: Action = argparser.add_argument(
            "--output",
            type=str,
            default="data/output/function_calls.json",
        )
        args: Namespace = argparser.parse_args(self.__argv[1:])
        output_file: str = cast(str, args.output)
        input_file: str = cast(str, args.input)
        functions_def: str = cast(str, args.functions_definition)
        self.path.set_args_path(
            output_file_path=output_file,
            input_path=input_file,
            file_definition_path=functions_def,
        )

    def detect_duplicate_keys(
        self,
        pairs: list[tuple[str, str]],
    ) -> dict[str, str]:
        """Detect and raise error on duplicate keys in JSON data.

        Args:
            pairs: List of key-value tuples from JSON parsing.

        Returns:
            Dictionary of validated key-value pairs.

        Raises:
            ValueError: If a duplicate key is detected.
        """
        result: dict[str, str] = {}

        for key, value in pairs:
            if key in result:
                raise ValueError(f"Duplicate key detected: '{key}'")
            result[key] = value
        return result

    def create_function_def(
        self,
    ) -> dict[str, FunctionDefinitionModel]:
        """Load and parse function definitions from JSON file.

        Returns:
            Dictionary mapping function names to FunctionDefinitionModel instances.

        Raises:
            FileNotFoundError: If the functions definition file does not exist.
            PermissionError: If the file cannot be read.
            ValueError: If duplicate function names are found.
        """
        data_function_definition: str = self.file_manager.read_file(
            self.path.file_functions_definition
        )

        data = json.loads(
            data_function_definition,
            object_pairs_hook=self.detect_duplicate_keys,
        )

        functions_definition = FunctionDefinitionRootModel.model_validate(data)

        return {func.name: func for func in functions_definition.root}

    def create_prompt(self) -> list[Prompt]:
        """Load and parse user prompts from JSON file.

        Returns:
            List of Prompt instances.

        Raises:
            FileNotFoundError: If the prompts file does not exist.
            PermissionError: If the file cannot be read.
            ValueError: If duplicate prompt entries are found.
        """
        prompt_data: str = self.file_manager.read_file(
            self.path.input_prompt_file
        )  # prompt data

        _: object = cast(
            object,
            json.loads(
                prompt_data,
                object_pairs_hook=self.detect_duplicate_keys,
            ),
        )

        prompts: list[Prompt] = PromptRootModel.model_validate_json(prompt_data).root

        return prompts
