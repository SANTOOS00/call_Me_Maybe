from pathlib import Path
from typing import Dict
from pydantic import BaseModel, TypeAdapter


class FormatFunctionCalling(BaseModel):
    prompt: str
    name: str
    parameters: Dict[str, str | int | float | bool]


class ProductJson:
    def __init__(self, functions_calling: list[FormatFunctionCalling] | None = None) -> None:
        self.functions_calling = functions_calling or []
        self.type_adapter = TypeAdapter(list[FormatFunctionCalling])

    def add_function(self, func: FormatFunctionCalling) -> None:
        self.functions_calling.append(func)

    def write_in_file(self, path: Path) -> None:
        with open(path, 'w', encoding='utf-8') as fb:
            json_data = self.type_adapter.dump_json(self.functions_calling, indent=2).decode("utf-8")
            fb.write(json_data)