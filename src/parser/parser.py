from src.custom_error import Call_Error
from .schema import FunctionDefn, Prompt
from typing import cast, Any


from pydantic import ValidationError
from pathlib import Path
import argparse
import json
import os
import sys


class ParserArgs:
    """Parse and validate command-line input paths."""

    def __init__(self) -> None:
        """Initialize the command-line argument parser."""
        self.__parser = argparse.ArgumentParser(description="is test")

    def run(self) -> argparse.Namespace:
        """Parse command-line arguments and validate their paths.

        Returns:
            Parsed command-line arguments.
        """
        arg: argparse.Namespace = self.__parser_args()
        self.__valdate_paths(arg)
        return arg

    def __parser_args(self) -> argparse.Namespace:
        """Define and parse the supported command-line arguments.

        Returns:
            Parsed command-line arguments.
        """
        self.__parser.add_argument(
            "--functions_definition",
            "-f",
            type=Path,
        )
        self.__parser.add_argument(
            "--output",
            "-o",
            type=Path,
            )
        self.__parser.add_argument(
            "--input",
            "-i",
            type=Path,
        )
        return self.__parser.parse_args()

    def __valdate_paths(self, args: argparse.Namespace) -> None:
        """Validate that configured input and output paths exist.

        Args:
            args: Parsed command-line arguments containing the paths.
        """
        if not args.functions_definition.exists() or\
           not args.functions_definition.exists():
            raise Call_Error(
                "Functions definition file "
                f"not found: {args.functions_definition}"
            )
        if not args.input.exists() or not args.input.exists():
            raise Call_Error(f"Input file not found: {args.input}")
        if not args.output.exists() or not args.output.exists():
            raise Call_Error(f"output file not found: {args.output}")


class ParserReadData:
    """Read prompts and function definitions from JSON files."""

    def get_prompts(self, path: Path) -> list[Prompt]:
        """Read prompts from a JSON file.

        Args:
            path: JSON file containing prompt objects.

        Returns:
            Validated prompt models.
        """
        try:
            with open(path, "r") as fd:
                prompts = json.load(fd, object_pairs_hook=self.valid_json)
            if not isinstance(prompts, list):
                raise TypeError(
                    "Expected the JSON content to be a list of prompts.")
            return [Prompt(**prompt) for prompt in prompts]
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON syntax in file '{path}' at "
                  f"line {e.lineno}: {e.msg}", file=sys.stderr)
            sys.exit(1)
        except ValidationError as e:
            print("Error: Data validation failed for Prompt"
                  f" schema in '{path}':\n{e}", file=sys.stderr)
            sys.exit(1)
        except TypeError as e:
            print("Error: Data structure mismatch while "
                  f"loading '{path}': {e}", file=sys.stderr)
            sys.exit(1)
        except BaseException as e:
            print("Error: An unexpected error occurred while"
                  f" loading prompts: {e}", file=sys.stderr)
            sys.exit(1)

    def get_functions_definition(self, path: Path) -> list[FunctionDefn]:
        """Read function definitions from a JSON file.

        Args:
            path: JSON file containing function definition objects.

        Returns:
            Validated function definition models.
        """
        try:
            with open(path, "r") as fd:
                function_defn: Any = json.load(fd, object_pairs_hook=self.valid_json)
            return [FunctionDefn(**fun) for fun in function_defn]
        except json.JSONDecodeError as e:
            print("Error: Invalid JSON syntax in file"
                  f" '{path}' at line {e.lineno}: {e.msg}", file=sys.stderr)
            sys.exit(1)
        except ValidationError as e:
            print("Error: Data validation failed for Prompt "
                  f"schema in '{path}':\n{e}", file=sys.stderr)
            sys.exit(1)
        except TypeError as e:
            print("Error: Data structure mismatch while "
                  f"loading '{path}': {e}", file=sys.stderr)
            sys.exit(1)
        except BaseException as e:
            print("Error: An unexpected error occurred while "
                  f"loading Functions definitions: {e}", file=sys.stderr)
            sys.exit(1)

    @staticmethod
    def valid_json(data_json: list[tuple[str, Any]]) -> dict[str, Any]:
        """Validate JSON key uniqueness and construct a dictionary.

        Custom object pairs hook for json.load to detect duplicate keys
        within any JSON object during parsing.

        Args:
            data_json: A list of key-value tuples representing a parsed
            JSON object.

        Returns:
            A dictionary containing the validated key-value pairs.

        Raises:
            ValueError: If a duplicate key is detected within the JSON object.
        """
        seen_keys: set[str] = set()
        validated_data: dict[str, Any] = {}
        for key, val in data_json:
            if key in seen_keys:
                raise ValueError(f"Duplicate key '{key}' detected in JSON object.")
            seen_keys.add(key)
            validated_data[key] = val
        return validated_data


class Parser:
    """Coordinate argument parsing and input data loading."""

    def __init__(self) -> None:
        """Initialize parser state."""
        self.__function_definition: list[FunctionDefn]
        self.__prompts: list[Prompt]
        self.__data: ParserReadData
        self.args: argparse.Namespace

    def run(self) -> None:
        """Parse arguments, load JSON data, and validate the inputs."""
        self.__set_args()
        self.__data = ParserReadData()
        self.__set_prompts()
        self.__set_functions_definition()
        self.__valid_data_json()

    def __valid_data_json(self) -> None:
        """Validate the input JSON paths after loading arguments."""
        self.__valid_path(self.args.input)
        self.__valid_path(self.args.functions_definition)

    @staticmethod
    def __valid_path(path: Path) -> None:
        """Ensure a path exists and is readable.

        Args:
            path: Path to validate.
        """
        if not path.exists():
            raise Call_Error("[ERROR]: Path does not existe")
        if not os.access(path, os.R_OK):
            raise Call_Error("[ERROR]: File is not readable")

    def get_path_funcall_json(self) -> Any:
        """Return the configured function-call output path.

        Returns:
            The output path supplied on the command line.
        """
        return self.args.output

    def __set_args(self) -> None:
        """Parse and store command-line arguments."""
        self.args = ParserArgs().run()

    def __set_functions_definition(self) -> None:
        """Load and validate function definitions from the input file."""
        self.__function_definition = (
            self.__data.get_functions_definition(
                cast(Path, self.args.functions_definition))
                )

    def __set_prompts(self) -> None:
        """Load and validate prompts from the input file."""
        self.__prompts = self.__data.get_prompts(self.args.input)

    @property
    def get_prompts(self) -> list[Prompt]:
        """Return the loaded prompts.

        Returns:
            Parsed prompt models.
        """
        return self.__prompts

    @property
    def functions_def(self) -> list[FunctionDefn]:
        """Return the loaded function definitions.

        Returns:
            Parsed function definition models.
        """
        return self.__function_definition
