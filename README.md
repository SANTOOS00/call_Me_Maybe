# SLD-LLM

This document outlines the architecture and implementation of **SLD-LLM**, a clean, well-architected utility wrapper for lightweight Hugging Face causal language models designed specifically for fast prototyping, educational exploration, and low-memory experimentation.

## Description

The `Small_LLM_Model` class encapsulates boilerplate code to provide a streamlined, high-performance interface for working with causal language models on consumer hardware.

### Key Architectural Features

* **Device & Precision Management:** The constructor features smart auto-detection for hardware accelerators, prioritizing Apple Silicon (`mps`) followed by NVIDIA GPUs (`cuda`), with a safe fallback to `cpu`. It automatically configures numerical precision—opting for `float16` on GPUs and MPS to drastically reduce memory usage and speed up inference, while keeping `float32` on CPUs to ensure maximum compatibility.
* **Robust Initialization & Safety Checks:** The setup handles common Hugging Face edge cases smoothly. If the tokenizer lacks a designated padding token (`pad_token_id`), it safely assigns the end-of-sequence token (`eos_token_id`) to prevent batching errors downstream. Furthermore, it prepares the model for pure inference by invoking `self._model.eval()` and explicitly setting `p.requires_grad = False` across all model parameters, cutting off gradient computation to save memory.

### Core Utility Methods

* `encode(text)`: Transforms a raw input string into a 2D PyTorch tensor of token IDs (`[1, sequence_length]`) and immediately dispatches it to the active computation device.
* `decode(ids)`: Reverses the tokenization process, accepting either a PyTorch tensor or a Python list of integers and decoding them back into clean text while stripping out special tokens.
* `get_logits_from_input_ids(input_ids)`: Executes a forward pass under a `torch.no_grad()` context manager, isolates the raw, unnormalized prediction logits for the final token in the sequence, and casts them into a standard Python list of floats.

### Example Usage

```python
    def example(self) -> None:
        model = Small_LLM_Model()
        prompt_str = "hello word"
            
        # Ensure prompt_ids is a flat list of integers
        prompt_tensor = model.encode(prompt_str)
        prompt_ids = prompt_tensor[0].tolist()  # Flattens tensor to [id1, id2, ...]
        
        logit = model.get_logits_from_input_ids(prompt_ids)
        
        for token_id, _ in enumerate(logit):
            if token_id in prompt_ids:
                decoded_text = model.decode([token_id])
                print(f"'{decoded_text}' this token and token_id {token_id} this index")

```
[Finite-state machine](https://en.wikipedia.org/wiki/Finite-state_machine)
[Trie](https://www.geeksforgeeks.org/dsa/trie-insert-and-search/)
[Constrained Decoding: Forcing LLMs to Respect Your Taxonomy](https://pub.towardsai.net/constrained-decoding-forcing-llms-to-respect-your-taxonomy-3aaaf13329f9)
