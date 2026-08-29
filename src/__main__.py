from .parser import Parser
from .custom_error import Call_Error

class Main:
    @classmethod
    def run(cls) -> None:
        cls.parser()

    @staticmethod
    def parser() -> None:
        parser = Parser()
        parser.run()

    @staticmethod
    def run_module() -> None:
        pass


if __name__ == "__main__":
    try:
        Main.run()
    except Call_Error as error:
        print(error)
        print("++ erorr ++")
