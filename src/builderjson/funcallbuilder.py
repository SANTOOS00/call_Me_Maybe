from typing import Dict


class FunCallBuilder:
    def __init__(self) -> None:
        self.name_function: str
        self.prompt: str
        self.paramiters: Dict[str, str]

    def set_name_function(self, name: str) -> None:
        self.name_function = name

    def set_prompt(self, prompt: str) -> None:
        self.prompt = prompt

    def set_paramiters(self, paramiters: Dict[str, str]) -> None:
        self.paramiters = paramiters

    def prints(self) -> None:
        print(self.name_function, flush=True)

    def clean(self) -> None:
        self.prompt = ""
        self.name_function = ""
        self.paramiters: Dict[str, str]
