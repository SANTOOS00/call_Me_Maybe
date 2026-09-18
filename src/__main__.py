from .llm_interaction_handler import LLMInteractionHandler
from .prompt import Prompt
from .function_definition import FunctionDefinitionModel
from .parsing import Parsing
from .model import Model
from pydantic import ValidationError
import sys


def main() -> None:
    """Main entry point for CALL_ME_MAYBE_42 function calling system."""
    # try:
    parser: Parsing = Parsing(sys.argv)
    model: Model = Model()
    functions_definition: dict[str, FunctionDefinitionModel] = (
        parser.create_function_def()
    )
    prompts: list[Prompt] = parser.create_prompt()
    llm_interaction: LLMInteractionHandler = LLMInteractionHandler(
        functions_definition, prompts, model
    )
    llm_interaction.generate_output()
    """

    except ValidationError as e:
        f"{e.errors()[0]['msg']}"
    except ValueError as e:
        print(e)
    except (FileNotFoundError, PermissionError) as e:
        print(e)
    """


if __name__ == "__main__":
    main()
