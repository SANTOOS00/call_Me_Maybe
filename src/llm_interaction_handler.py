from .function_definition import FunctionDefinitionModel
from .function_call_model import FunctionCallModel, FunctionCallRootModel
from .gen_function_name import GenerateFunctionName
from .gen_args_function import GenerateArgFunction
from .project_types import ArgType
from .filemanager import FileManager
from .prompt import Prompt
from .model import Model
from .path import PathData
from .gen_state import GenState


class LLMInteractionHandler:
    """Orchestrate LLM-based function calling from user prompts.

    Attributes:
        functions_call: Dictionary of available function calls.
        prompts: List of user prompts.
        model: The language model instance.
        gen_function: Generator for function names.
        gen_arg: Generator for function arguments.
        file_manager: File manager for output.
    """

    def __init__(
        self,
        functions_definition: dict[str, FunctionDefinitionModel],
        prompts: list[Prompt],
        model: Model,
    ) -> None:
        """Initialize the LLM interaction handler.

        Args:
            functions_call: Dictionary mapping function names to FunctionCall
            objects.
            prompts: List of user prompts to process.
        """
        self.functions_call: dict[str, FunctionDefinitionModel] = (
            functions_definition  # function definition
        )
        self.prompts: list[Prompt] = prompts
        self.generate_state: GenState = GenState(model)
        self.model: Model = model
        self.gen_function: GenerateFunctionName = GenerateFunctionName(
            self.functions_call, self.model, self.generate_state
        )
        self.gen_arg: GenerateArgFunction = GenerateArgFunction(
            self.model, self.generate_state
        )
        self.file_manager: FileManager = FileManager()
        self.path: PathData = PathData()
        self.function_call_root_model: FunctionCallRootModel = FunctionCallRootModel([])

    def generate_output(self) -> None:
        """Generate function calls for all prompts.

        Returns:
            List of dictionaries containing prompt, function name, and
            parameters.
        """
        return_val: list[FunctionCallModel] = list()
        for prompt in self.prompts:
            function_name: str = self.gen_function.get_function_name(
                prompt.prompt
            )  # FUNCTION NAME
            parameters: dict[str, ArgType] = self.gen_arg(
                self.functions_call[function_name], prompt.prompt
            )
            function_call: FunctionCallModel = FunctionCallModel(
                prompt=prompt.prompt,
                function=function_name,
                arguments=parameters,  # arguments
            )
            return_val.append(function_call)
            self.function_call_root_model.root.append(function_call)
        self.file_manager.write_to_file(
            self.path.output_file_path, self.function_call_root_model.model_dump_json()
        )
