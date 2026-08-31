from .parser import Parser
from .custom_error import Call_Error
from llm_sdk.llm_sdk import Small_LLM_Model


class Main:
    data: Parser

    @classmethod
    def run(cls) -> None:
        cls.parser()
        cls.run_module()

    @classmethod
    def parser(cls) -> None:
        cls.data = Parser()
        cls.data.run()

    @classmethod
    def run_module(cls) -> None:
        module = Small_LLM_Model()
        prompt = cls.data.get_prompts()[0]
        ss = module.encode(prompt.prompt)
        print(ss)


if __name__ == "__main__":
    try:
        Main.run()
    except Call_Error as error:
        print(error)
        print("++ erorr ++")
