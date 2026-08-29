import argparse
from pathlib import Path
from src.custom_error import Call_Error
import json
import os
from typing import Dict, List, Any


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
    def get_promtes(self, path: Path) -> List[Dict[Any, Any]]:
        self.__valid_path(path)
        with open(path, "r") as fd:
            promtes = json.load(fd)
        return promtes

    def get_function_definition(self, path: Path) -> List[Dict[Any, Any]]:
        self.__valid_path(path)
        with open(path, "r") as fd:
            promtes = json.load(fd)
        return promtes

    def __valid_path(self, path: Path) -> None:
        if not path.exists():
            raise Call_Error("sssssssssss")
        if not os.access(path, os.R_OK):
            raise Call_Error("sssssssssssssss")


class Parser:
    def __init__(self) -> None:
        self.__function_definition = None
        self.__promtes = None
        self.__parser_data: ParserReadData
        self.args: argparse.Namespace

    def run(self) -> None:
        self.set_args()
        self.__parser_data = ParserReadData()
        self.__set_promtes()
        self.__set_function_def()

    def set_args(self) -> None:
        self.args = ParserArgs().run()

    def __set_function_def(self) -> None:
        self.__function_definition = self.\
            __parser_data.get_function_definition(
                self.args.functions_definition)

    def __set_promtes(self) -> None:
        self.__promtes = self.__parser_data.get_promtes(self.args.input)
