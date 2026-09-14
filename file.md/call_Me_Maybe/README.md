# Project Overview

`call_Me_Maybe` is a Python project designed to generate parameters based on function definitions. It utilizes a language model to assist in generating valid parameter values, including strings, numbers, integers, and booleans. The project is structured to facilitate easy extension and testing.

## Project Structure

```
call_Me_Maybe
├── src
│   ├── __init__.py
│   ├── generator
│   │   ├── __init__.py
│   │   └── module
│   │       ├── __init__.py
│   │       ├── parameter_generator.py
│   │       └── promptproduct.py
│   ├── parser
│   │   ├── __init__.py
│   │   └── function_definition.py
│   └── llm_manager
│       ├── __init__.py
│       └── manager.py
├── tests
│   ├── __init__.py
│   └── test_parameter_generator.py
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Installation

To install the required dependencies, run:

```
pip install -r requirements.txt
```

## Usage

To use the `ParameterGenerator`, you need to create an instance of the `ManagerLLM` class, which manages interactions with the language model. Then, you can create an instance of `ParameterGenerator` and call the `generate` method with a function definition and a prompt.

### Example

```python
from src.llm_manager.manager import ManagerLLM
from src.generator.module.parameter_generator import ParameterGenerator
from src.parser.function_definition import FunctionDefn

# Initialize the language model manager
model_manager = ManagerLLM()

# Create a parameter generator
param_generator = ParameterGenerator(model_manager)

# Define a function definition
function_def = FunctionDefn(name="example_function", description="An example function", parameters={"arg1": "string", "arg2": "number"})

# Generate parameters
parameters = param_generator.generate(function_def, "Generate parameters for the example function.")
print(parameters)
```

## Testing

To run the tests for the `ParameterGenerator`, navigate to the `tests` directory and run:

```
pytest test_parameter_generator.py
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.