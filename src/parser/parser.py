from pathlib import Path
from src.custom_error import Call_Error
from typing import List
from .schema import FunctionDefn, Prompt
from pydantic import ValidationError


import argparse
import json
import os


class ParserArgs:
    def __init__(self) -> None:
        self.__parser = argparse.ArgumentParser(description="is test")

    def run(self) -> argparse.Namespace:
        arg: argparse.Namespace = self.__parser_args()
        self.__valdate_paths(arg)
        return arg

    def __parser_args(self) -> argparse.Namespace:
        self.__parser.add_argument(
            "--functions_definition", "-f",
            type=Path,
            required=True
        )
        self.__parser.add_argument(
            "--output", "-o",
            type=Path,
            required=True
        )
        self.__parser.add_argument(
            "--input", "-i",
            type=Path,
            required=True,
        )

        return self.__parser.parse_args()

    def __valdate_paths(self, args: argparse.Namespace) -> None:
        if not args.functions_definition.exists():
            raise Call_Error("Functions definition file "
                             f"not found: {args.functions_definition}")
        if not args.input.exists():
            raise Call_Error(f"Input file not found: {args.input}")
        if not args.output.exists():
            raise Call_Error(f"output file not found: {args.output}")


class ParserReadData:
    def get_prompts(self, path: Path) -> List[Prompt]:
        with open(path, "r") as fd:
            prompts = json.load(fd)
        return [Prompt(**prompt) for prompt in prompts]

    def get_functions_definition(self, path: Path) -> List[FunctionDefn]:
        with open(path, "r") as fd:
            function_defn: List = json.load(fd)
        return [FunctionDefn(**fun) for fun in function_defn]


class Parser:
    def __init__(self) -> None:
        self.__function_definition: List[FunctionDefn]
        self.__prompts: List[Prompt]
        self.__data: ParserReadData
        self.args: argparse.Namespace

    def run(self) -> None:
        self.__set_args()
        self.__data = ParserReadData()
        self.__set_prompts()
        self.__set_functions_definition()
        self.__valid_data_json()

    def __valid_data_json(self) -> None:
        self.__valid_path(self.args.input)
        self.__valid_path(self.args.functions_definition)

    @staticmethod
    def __valid_path(path: Path) -> None:
        if not path.exists():
            raise Call_Error("[ERROR]: Path does not existe")
        if not os.access(path, os.R_OK):
            raise Call_Error("[ERROR]: File is not readable")

    def __set_args(self) -> None:
        self.args = ParserArgs().run()

    def __set_functions_definition(self) -> None:
        try:
            self.__function_definition = self.__data.get_functions_definition(self.args.functions_definition)
        except ValidationError as e:
            raise Call_Error(str(e))
            

    def __set_prompts(self) -> None:
        try:
            self.__prompts = self.__data.get_prompts(self.args.input)
        except ValidationError as e:
            print(e)

    def get_prompts(self) -> List[Prompt]:
        return self.__prompts

    def get_functions_def(self) -> List[FunctionDefn]:
        return self.__function_definition
