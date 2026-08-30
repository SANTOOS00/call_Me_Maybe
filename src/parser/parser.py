from pathlib import Path
from src.custom_error import Call_Error
from typing import Dict, List, Any
from .schema import SchemaFunDefn, SchemaPrompt

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
    def get_prompts(self, path: Path) -> List[Dict[Any, Any]]:
        with open(path, "r") as fd:
            promtes = json.load(fd)
        return promtes

    def get_functions_definition(self, path: Path) -> List[Dict[Any, Any]]:
        with open(path, "r") as fd:
            prompts: List = json.load(fd)
        return self.valid_functions_definition(prompts)

    def valid_functions_definition(prompts: List) -> None:
        print(prompts)


class Parser:
    def __init__(self) -> None:
        self.__function_definition: List[SchemaFunDefn]
        self.__prompts: List[SchemaPrompt]
        self.__data: ParserReadData
        self.args: argparse.Namespace

    def run(self) -> None:
        self.__set_args()
        self.__data = ParserReadData()
        self.__set_promtes()
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
        self.__function_definition = self.\
            __data.get_function_definitions(
                self.args.functions_definition)

    def __set_promtes(self) -> None:
        self.__prompts = self.__data.get_prompts(self.args.input)
