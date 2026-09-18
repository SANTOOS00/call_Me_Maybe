import sys

import json
import os


class FileManager:
    """Manage file operations for reading and writing function call data."""

    def write_to_file(self, output_file_path: str, functions_callings: str) -> None:
        """Write content to the output file.

        Args:
            content: List of dictionaries to write as JSON.
        """
        if "/" in output_file_path:
            index_path_directory_end: int = output_file_path.rindex("/")
            os.makedirs(
                output_file_path[:index_path_directory_end], exist_ok=True
            )  # create dir output if not exist
        try:
            with open(output_file_path, "w") as output_file:

                json.dump(
                    functions_callings,
                    output_file,
                    indent=2,
                )
        except PermissionError:
            sys.exit(0)

    def read_file(self, path: str) -> str:
        """Read and parse a JSON file into model objects.

        Args:
            path: The file path to read from.
            model: The Pydantic model class to validate data against.

        Returns:
            A list of model instances validated from the file data.

        Raises:
            ValidationError: If the file data does not match the model schema.
        """
        exists = os.access(path, os.R_OK)
        if not exists:
            raise FileNotFoundError(f"{path} Not found")
        can_read = os.access(path, os.F_OK)
        if not can_read:
            raise PermissionError(
                f"{path} Permission denied to read file [{path}]"
            )  # permissions denied
        with open(path, "r") as f:
            return f.read()
