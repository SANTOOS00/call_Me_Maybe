from .parser import Parser
from .custom_error import Call_Error
from llm_sdk.llm_sdk import Small_LLM_Model
import numpy as np


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
        prompt = cls.data.get_prompts()[0]

        generated_ids: list[int] = [int(dd) for dd in model.encode(prompt.prompt).flatten()]
        

        while True:
            logits = model.get_logits_from_input_ids(generated_ids)
            ss: int = np.argmax(logits)
            generated_ids.append(ss)

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

