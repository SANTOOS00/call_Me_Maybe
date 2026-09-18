from typing_extensions import Self


class PathData:
    """Singleton class for managing file paths used by the application.

    This class uses the singleton pattern to ensure only one instance exists
    throughout the application lifetime.

    Attributes:
        output_file_path: Path to the output JSON file.
        input_prompt_file: Path to the input prompts JSON file.
        file_functions_definition: Path to the function definitions JSON file.
    """

    _instance: Self | None = None

    def __new__(cls) -> Self:
        """Create a singleton instance of PathData.

        Returns:
            The single instance of PathData.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """Initialize PathData instance paths (singleton initialization)."""
        if PathData._instance:
            return
        self.output_file_path: str
        self.input_prompt_file: str
        self.file_functions_definition: str

    def set_args_path(
        self,
        /,
        *,
        output_file_path: str,
        input_path: str,
        file_definition_path: str,
    ) -> None:
        """Initialize file paths for the FileManager."""
        self.output_file_path = output_file_path
        self.input_prompt_file = input_path
        self.file_functions_definition = file_definition_path
