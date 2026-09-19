from pathlib import Path
from typing import Dict
from pydantic import BaseModel, TypeAdapter


class FormatFunctionCalling(BaseModel):
    """Represent one generated function call in the output schema."""

    prompt: str
    name: str
    parameters: Dict[str, str | int | float | bool]


class ProductJson:
    """Collect and serialize generated function calls."""

    def __init__(self) -> None:
        """Initialize the function-call collection.
        Args:
            functions_calling: Existing calls to include, if any.
        """

        self.functions_calling: list[FormatFunctionCalling] = []
        self.type_adapter = TypeAdapter(list[FormatFunctionCalling])

    def add_function(self, func: FormatFunctionCalling) -> None:
        """Append a generated function call.

        Args:
            func: Function call to append.
        """
        self.functions_calling.append(func)

    def write_in_file(self, path: Path) -> None:
        """Write all collected function calls as formatted JSON.

        Args:
            path: Destination file path.
        """
        with open(path, 'w', encoding='utf-8') as fb:
            json_data = self.type_adapter.dump_json(self.functions_calling,
                                                    indent=2).decode("utf-8")
            fb.write(json_data)
