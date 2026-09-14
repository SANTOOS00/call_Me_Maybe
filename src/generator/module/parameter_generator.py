import json
from enum import Enum, auto
from typing import Dict

import numpy

from ...llm_manager import ManagerLLM
from ...parser import FunctionDefn
from .promptproduct import PromptProduct


ParameterValue = int | str | bool | float


class NumberFSM(Enum):
    START = auto()
    SIGN = auto()
    INTEGER = auto()
    DECIMAL = auto()
    END = auto()


class ParameterGenerator:

    def __init__(self, model: ManagerLLM) -> None:
        self.model = model
        self.valid_parameters: Dict[str, ParameterValue] = {}
        self.context_window_ids: list[int] = []

    def generate(
        self, function_definition: FunctionDefn, prompt: str
    ) -> Dict[str, ParameterValue]:
        self.valid_parameters = {}

        for name, parameter_type in function_definition.parameters.items():
            parameter_prompt = self.builder_prompt(
                user_prompt=prompt,
                function_definition=function_definition,
                parameter_name=name,
                parameter_type=parameter_type.type,
            )
            print(parameter_prompt)
            self.context_window_ids = self.model.custom_encoder(parameter_prompt)

            match parameter_type.type:
                case "string":
                    value = self.__generate_string(len(prompt))
                case "number":
                    value = self.__generate_number(len(prompt))
                case "integer":
                    value = int(self.__generate_number(len(prompt)))
                case "boolean":
                    value = self.__generate_boolean(len(prompt))
                case _:
                    pass
            self.valid_parameters[name] = value
        return self.valid_parameters

    def __generate_string(self, max_tokens: int) -> str:
        generated = self.__generate_text(max_tokens)
        generated = generated.splitlines()[0].strip() if generated else ""
        generated = generated.split(",", maxsplit=1)[0].strip()
        generated = generated.rstrip("},")
        if len(generated) >= 2 and generated[0] == generated[-1] in {'"', "'"}:
            generated = generated[1:-1]
        return generated.strip()

    def __generate_boolean(self, max_token) -> bool:
        generated = self.__generate_text(max_token)
        candidates = generated.strip().lower().split(",", maxsplit=1)[0].split()
        if not candidates:
            raise ValueError("Model generated an empty boolean value")
        value = candidates[0]
        if value not in {"true", "false"}:
            raise ValueError(f"Model generated an invalid boolean value: {generated}")
        return value == "true"

    def __generate_text(self, max_tokens: int) -> str:
        generated: str = ""
        for _ in range(max_tokens):
            logits = self.model.get_logits(self.context_window_ids)
            token_id = int(numpy.argmax(logits))
            token = self.model.decode_token(token_id)
            self.context_window_ids.append(token_id)
            if not token:
                break
            generated += token
            if any(character in token for character in ("\n", "\r")):
                break
        return generated

    def __generate_number(self, max_token: int) -> float:
        generated: str = ""
        for _ in range(max_token):
            token_possible: list[int] | None = self.__possible_number_tokens(generated)
            if token_possible is None:
                break
            logits: list[float] = self.model.mask_logits(self.context_window_ids, token_possible)
            token_id = int(numpy.argmax(logits))
            token = self.model.decode_token(token_id)
            self.context_window_ids.append(token_id)
            generated += token
            print(generated)
            step = self._number_state(token)
            if step == NumberFSM.END:
                if "," in token:
                    index = token.index(",")
                    token = token[:index]
                break
        return float(generated)

    def __possible_number_tokens(self, number: str) -> list[int] | None:
        state = self._number_state(number)
        if state == NumberFSM.START:
            characters = "-+0123456789"
        elif state == NumberFSM.SIGN:
            characters = "0123456789"
        elif state == NumberFSM.INTEGER:    
            characters = "0123456789.,"
        elif state == NumberFSM.DECIMAL:
            characters = "0123456789,"
        else:
            return None
        return self.model.encoder_chr_by_chr(characters)

    def _number_state(self, number: str) -> NumberFSM:
        step_generator: NumberFSM = NumberFSM.START
        cont_decmal: int = 0
        cont_number: int = 0
        for nu in number:
            match step_generator:
                case NumberFSM.START:
                    if nu in "-+":
                        step_generator = NumberFSM.SIGN
                    else:
                        step_generator = NumberFSM.INTEGER
                case NumberFSM.SIGN:
                    step_generator = NumberFSM.INTEGER
                case NumberFSM.INTEGER:
                    if nu == '.' and cont_number != 0:
                        step_generator = NumberFSM.DECIMAL
                    elif nu == ',' or cont_number > 5:
                        return NumberFSM.END
                    else:
                        cont_number += 1
                case NumberFSM.DECIMAL:
                    if (nu == ',' and cont_decmal) or cont_decmal > 5:
                        return NumberFSM.END
                    cont_decmal += 1
                case NumberFSM.END:
                    return step_generator
        return step_generator

    def builder_prompt(
            self,
            user_prompt: str,
            function_definition: FunctionDefn,
            parameter_name: str,
            parameter_type: str,
        ) -> str:
        return (
            PromptProduct.PARAMETER_GENERATOR
            .replace("{USER_PROMPT}", user_prompt)
            .replace("{FUNCTION_NAME}", function_definition.name)
            .replace("{FUNCTION_DESCRIPTION}", function_definition.description)
            .replace(
                "{FUNCTION_DEFINITION}",
                json.dumps(function_definition.model_dump(), indent=2),
            )
            .replace("{PARAMETERS}", repr(self.valid_parameters))
            .replace("{PARAMETER_NAME}", parameter_name)
            .replace("{PARAMETER_TYPE}", parameter_type)
        )
