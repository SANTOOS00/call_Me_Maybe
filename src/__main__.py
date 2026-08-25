import sys
from typing import List


class Main:
    @classmethod
    def run(cls) -> None:
        cls.parser(sys.argv[1:])

    @staticmethod
    def parser(args: List[str]) -> None:
        print(args)

    @staticmethod
    def run_module() -> None:
        pass


if __name__ == "__main__":
    try:
        Main.run()
    except BaseException as error:
        print(error)
        print("++ erorr ++")
