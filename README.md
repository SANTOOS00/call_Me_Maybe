*This project has been created as part of the 42 curriculum by moerrais*

# Call Me Maybe

## Description

Call Me Maybe is a Python project that converts natural-language prompts into
structured function calls. It uses a local Hugging Face causal language model
to select a function and extract its parameters, then writes the calls as
JSON.

The project is designed to make model-generated function calling more reliable
by constraining generation to the function definitions supplied by the user.
It includes a command-line generator, a reusable local model wrapper, JSON
schemas for inputs and outputs, and a `moulinette` utility for preparing and
grading exercises.

The repository also contains:

- `llm_sdk`: a small wrapper around Hugging Face Transformers for local
  inference.

## Instructions

### Requirements

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

### Installation

From the repository root:

```bash
uv sync --all-packages
```

Or use the Make target:

```bash
make install
```

## Example usage

### Running the function-calling generator

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

## Algorithm explanation

The generator uses a two-stage constrained-decoding pipeline:

1. `Parser` reads the function definitions and prompts from JSON, validates
   them with Pydantic, and checks that the configured paths are readable.
2. `FunctionNameGenerator` serializes the available function definitions into a
   selection prompt. Each function name is tokenized and inserted into a prefix
   trie. During greedy decoding, the trie returns only token identifiers that
   can continue a valid function name. `ManagerLLM.mask_logits` sets every
   other logit to negative infinity, so the model cannot select a token outside
   the known function-name prefixes. Once a complete name is reached, the
   matching `FunctionDefn` is selected.
3. `ParameterGenerator` builds a second prompt containing the user request,
   function prototype, and already generated arguments. It selects a generator
   based on the declared type:
   - Strings are generated with a finite-state machine that tracks content,
     escapes, closing quotes, and the prompt-derived length limit.
   - Numbers use a finite-state machine for signs, integer digits, decimals,
     and termination.
   - Integers reuse numeric generation and convert the result to `int`.
   - Booleans restrict the candidate tokens to `true` and `false`.
4. `ProductJson` validates the output model and writes the accumulated calls as
   a formatted JSON array.

This approach constrains syntax and the set of callable names, but it does not
guarantee that a semantically ambiguous prompt will produce the desired
argument value.

## Design decisions

- **Local inference:** The project uses a local Hugging Face model instead of
  sending prompts to a remote service, which keeps the execution path
  reproducible and avoids requiring an external API key.
- **Trie-based name constraints:** A prefix trie makes valid next-token lookup
  explicit and prevents the model from inventing function names.
- **Finite-state machines for values:** Small state machines are easier to
  reason about than unconstrained text generation for JSON-like strings and
  numbers.
- **Pydantic schemas:** Pydantic provides validation at the input and output
  boundaries and rejects unexpected fields.
- **Greedy decoding:** Selecting the highest-scoring allowed token keeps the
  implementation deterministic and avoids introducing sampling parameters into
  the exercise.

## Performance analysis

Function-name lookup is proportional to the generated name length, while trie
construction is proportional to the total number of tokens in all supplied
names. Parameter generation requires one model inference step per generated
token, so model inference is the dominant cost. The trie and logit masking add
small CPU-side overhead compared with loading the model and running inference.

The design improves **reliability** for function-name validity and basic value
syntax, and improves **accuracy** when the prompt clearly matches one
definition. It cannot resolve ambiguity that is not represented in the prompt
or definitions. **Speed** depends primarily on the selected model and whether
CPU, CUDA, or Apple MPS is available; the repository does not currently claim a
fixed latency or accuracy benchmark.

## Challenges faced

- Restricting free-form model output to known function names required tracking
  token prefixes rather than comparing decoded strings after generation. The
  trie solves this by exposing valid continuations at each prefix.
- Strings and numbers have different termination and escaping rules. Separate
  finite-state machines keep those rules local and make the allowed-token
  policy explicit.
- Local model execution varies by hardware. The model wrapper selects an
  available device and uses inference without gradients, while the README
  documents the memory and download requirements.
- Model output can still be semantically wrong even when syntactically valid.
  The project therefore validates schemas and documents that generated JSON
  should be reviewed before downstream use.

## Testing strategy

Validation is performed at several boundaries:

- Pydantic models validate function definitions, prompts, and generated output
  structures.
- The parser checks required paths and file readability before generation.
- The trie can be tested independently with insertion, prefix lookup, and
  complete-sequence searches.
- The numeric and string finite-state machines can be exercised with valid,
  incomplete, escaped, decimal, and terminating inputs.
- Repository checks are run with `make lint`, which invokes Flake8 and the
  configured MyPy check.
- End-to-end validation uses the sample JSON files and confirms that the
  generator writes a JSON array containing the expected call fields.

The current project does not include a dedicated automated test suite, so
model-quality claims should be evaluated with representative prompts and
additional fixtures.




### Useful Make targets

| Command | Purpose |
| --- | --- |
| `make install` | Install/sync all workspace packages. |
| `make run` | Run the main generator with the sample data. |
| `make lint` | Run Flake8 and a configured MyPy check. |
| `make lint-strict` | Run Flake8 and MyPy in strict mode. |
| `make clean` | Remove local virtual-environment/cache artifacts. |



## Model behavior and limitations

`llm_sdk.Small_LLM_Model` automatically chooses `mps`, `cuda`, or `cpu`, and
uses half precision on accelerators and full precision on CPU by default.
Inference is run with gradients disabled.

The generator currently performs greedy token selection. Parameter extraction
is deliberately constrained for numbers and uses a small finite-state-machine
for strings, so prompts with ambiguous wording, missing values, unsupported
types, malformed JSON, or complex escaping may need additional handling.
Generated output should therefore be checked before it is used downstream.

## Resources

- [Hugging Face Transformers documentation](https://huggingface.co/docs/transformers/)
  — model and tokenizer concepts used by the local inference wrapper.
- [Qwen documentation](https://qwen.readthedocs.io/) — background on the
  default Qwen model family.
- [Finite-state machine](https://en.wikipedia.org/wiki/Finite-state_machine)
  — reference for the constrained string and number generators.
- [uv documentation](https://docs.astral.sh/uv/) — installation and workspace
  dependency management.

### AI usage

AI assistance was used for documentation work: reviewing the repository
structure, drafting and organizing this README, and adding PEP 257 docstrings
to existing Python classes and functions. The AI was not used as a substitute
for runtime validation; commands, schemas, algorithm descriptions, and stated
limitations were checked against the repository. No external service is
required by the application at runtime beyond downloading the configured model
from Hugging Face.

