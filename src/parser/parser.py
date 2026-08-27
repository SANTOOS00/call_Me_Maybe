import argparse
from pathlib import Path
from src.custom_error import Call_Error


class Parser:
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(description="is test")

    def run(self) -> None:
        print("ss")
        args = self.__parser_args()
        self.__valdate_paths(args)

    def __parser_args(self) -> argparse.Namespace:
        self.parser.add_argument(
            "--functions_definition", "-f",
            type=Path,
            required=True
        )
        self.parser.add_argument(
            "--output", "-o",
            type=Path,
            required=True
        )
        self.parser.add_argument(
            "--input", "-i",
            type=Path,
            required=True,
        )

        return self.parser.parse_args()

    def __valdate_paths(self, args: argparse.Namespace) -> None:
        if not args.functions_definition.exists():
            raise Call_Error("Functions definition file "
                             f"not found: {args.functions_definition}")
        if not args.input.exists():
            raise Call_Error(f"Input file not found: {args.input}")
        if not args.output.exists():
            raise Call_Error(f"output file not found: {args.input}")
