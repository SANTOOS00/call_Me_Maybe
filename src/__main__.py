from .parser import Parser
from .custom_error import Call_Error
from llm_sdk.llm_sdk import Small_LLM_Model
import numpy as np

from enum import Enum


from enum import Enum


from enum import Enum
import re


class TestEnum(Enum):
    PROMPT_GENERATOR = """
    You are a strict Function Router.

    Your task is to analyze the user's prompt and select the single most
    appropriate function from the provided list of available functions.

    STRICT EXECUTION RULES:
    - Return ONLY the exact name of the selected function as plain text.
    - Do NOT include any code blocks, backticks, quotes, or Markdown formatting.
    - Do NOT write any explanations, greetings, preamble, or extra text.
    - If no function in the list matches the user's request, return "NONE".
    AVAILABLE FUNCTIONS:
    {FUNCTIONS}

    USER PROMPT:
    {PROMPT}
    """

    @classmethod
    def extract_between_quotes(cls, text: str) -> str:
        # كايقلّب على أي نص كاين بين أوّل ' وآخر '
        match = re.search(r"'(.*)'", text)
        return match.group(1) if match else text.strip()

    @classmethod
    def get_prompt_generator(
        cls,
        functions: list[str],
        prompt: str,
    ) -> str:
        cleaned_functions: list[str] = [
            cls.extract_between_quotes(fn) for fn in functions
        ]

        functions_text: str = "\n".join(
            f"- '{fn}'" for fn in cleaned_functions
        )

        return cls.PROMPT_GENERATOR.value.format(
            FUNCTIONS=functions_text,
            PROMPT=prompt,
        )



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
        model = Small_LLM_Model()
        fun_dif = cls.data.get_functions_def()
        
        prompt = "What is the sum of 2 and 3?"
        functions_difs = [fun.name for fun in fun_dif]
        prom = TestEnum.get_prompt_generator(functions_difs, prompt)
        generated_ids: list[int] = [int(dd) for dd in model.encode(prom).flatten()]
        

        while True:
            logits = model.get_logits_from_input_ids(generated_ids)
            ss: int = np.argmax(logits)
            generated_ids.append(int(ss))
            # print(generated_ids)
            with open('tes.txt', 'a') as sd:
                print(model.decode(ss), file=sd)
            print(model.decode(ss), flush=True, end="")



if __name__ == "__main__":
    try:
        Main.run()
    except Call_Error as error:
        print(error)
        print("++ erorr ++")




        # prompt_id = [int(id) for id in model.encode(prompt.prompt).flatten()]
        # generated_ids: list[int] = prompt_id
        # fn_name_ids: list[int] = list()
        # fn_name: str = str()
        # while True:
        #     logits: list[float] = model.get_logits_from_input_ids(generated_ids)
        #     high_score_id: int = np.argmax(logits)
        #     fn_name_ids.append(high_score_id)
        #     generated_ids.append(high_score_id)

        #     token = model.decode(high_score_id)
        #     fn_name_ids.append(high_score_id)
        #     print(token, end="", flush=True)

