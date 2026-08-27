from .parser import Parser


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
    except BaseException as error:
        print(error)
        print("++ erorr ++")
