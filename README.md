# Call Me Maybe

Call Me Maybe is a Python project that converts natural-language prompts into
structured function calls. It uses a local Hugging Face causal language model
to select a function and extract its parameters, then writes the calls as
JSON.

The repository also contains:

- `llm_sdk`: a small wrapper around Hugging Face Transformers for local
  inference.
- `moulinette`: a CLI for generating function-calling exercises and grading
  submitted answers.
- `test_project`: small experiments for the finite-state-machine and prompt
  parsing ideas.

## Requirements

- Python 3.11 or newer for the main project.
- [`uv`](https://docs.astral.sh/uv/) for dependency management.
- A machine able to load the configured model (`Qwen/Qwen3-0.6B` by default).
  The model and tokenizer are downloaded from Hugging Face on first use.

The main project dependencies are declared in `pyproject.toml`:

- `llm-sdk` (the workspace package)
- `numpy`
- `pydantic`

The `llm-sdk` package adds `torch`, `transformers`, and
`huggingface-hub`. The `moulinette` package has its own dependencies
(`fire`, `pydantic`, and `colorama`).

## Installation

From the repository root:

```bash
uv sync --all-packages
```

Or use the Make target:

```bash
make install
```

## Running the function-calling generator

The main CLI requires three paths:

```bash
uv run python -m src \
  --functions_definition data/input/functions_definition.json \
  --input data/input/function_calling_tests.json \
  --output data/output/function_calls.json
```

The equivalent Make target is:

```bash
make run
```

`src.parser.Parser` validates the input files and converts them into Pydantic
models. `src.generator.Generator` then:

1. Uses `FunctionNameGenerator` and a trie to restrict generation to the
   function names supplied in the definitions.
2. Uses `ParameterGenerator` to extract values for `string`, `number`,
   `integer`, and `boolean` parameters.
3. Uses `ProductJson` to append each call and write the result to the output
   file.

The generated output is a JSON array with this shape:

```json
[
  {
    "prompt": "Greet shrek",
    "name": "fn_greet",
    "parameters": {
      "name": "shrek"
    }
  }
]
```

### Input formats

Function definitions are an array of objects:

```json
[
  {
    "name": "fn_greet",
    "description": "Generate a greeting message for a person by name.",
    "parameters": {
      "name": {"type": "string"}
    },
    "returns": {"type": "string"}
  }
]
```

Prompts are an array containing one `prompt` field:

```json
[
  {"prompt": "Greet shrek"}
]
```

Supported parameter types are `string`, `number`, `integer`, and `boolean`.
The Pydantic schemas reject unexpected fields.

## Moulinette: exercises and grading

`moulinette` contains public and private exercise definitions. Public exercises
are intended for students; private exercises are intended to remain hidden and
are used for grading.

Generate an exercise set:

```bash
uv run python -m moulinette prepare_exercises --set public
uv run python -m moulinette prepare_exercises --set private
```

The command writes:

- `data/input/functions_definition.json`
- `data/input/function_calling_tests.json`
- `data/correction/function_calling_corrections.json`

To grade a generated student answer file:

```bash
uv run python -m moulinette grade_student_answers \
  --student_answer_path data/output/function_calls.json \
  --set public
```

The grader checks the prompt, function name, parameter validity, and returned
value. It prints a per-test result and a final score. Set `NO_COLOR=1` to
disable terminal colors.

## Useful Make targets

| Command | Purpose |
| --- | --- |
| `make install` | Install/sync all workspace packages. |
| `make run` | Run the main generator with the sample data. |
| `make run_test` | Run the `test_project` module with the sample data. |
| `make lint` | Run Flake8 and a configured MyPy check. |
| `make lint-strict` | Run Flake8 and MyPy in strict mode. |
| `make clean` | Remove local virtual-environment/cache artifacts. |

## Project layout

```text
.
├── src/
│   ├── __main__.py                 # Main CLI entry point
│   ├── parser/                     # CLI arguments, JSON loading, Pydantic schemas
│   ├── generator/                  # Function and parameter generation
│   ├── builderjson/                # Output models and JSON writer
│   ├── llm_manager/                # Project-specific model adapter
│   ├── trie/                       # Token-prefix trie for function names
│   └── custom_error/               # Domain error type
├── llm_sdk/                        # Reusable local Hugging Face model wrapper
├── moulinette/                     # Exercise generation and grading CLI
├── data/
│   ├── input/                      # Function definitions and prompts
│   └── output/                     # Generated function calls
├── test_project/                   # Small FSM/prompt experiments
├── Makefile
├── pyproject.toml
└── uv.lock
```

## Model behavior and limitations

`llm_sdk.Small_LLM_Model` automatically chooses `mps`, `cuda`, or `cpu`, and
uses half precision on accelerators and full precision on CPU by default.
Inference is run with gradients disabled.

The generator currently performs greedy token selection. Parameter extraction
is deliberately constrained for numbers and uses a small finite-state-machine
for strings, so prompts with ambiguous wording, missing values, unsupported
types, malformed JSON, or complex escaping may need additional handling.
Generated output should therefore be checked before it is used downstream.

## Development notes

Run the checks after making changes:

```bash
make lint
```

The repository includes exploratory files and generated JSON fixtures. Virtual
environments and Python cache directories are local build artifacts and should
not be edited manually.
