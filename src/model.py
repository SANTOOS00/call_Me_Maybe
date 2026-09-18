from llm_sdk import Small_LLM_Model
from typing import cast
import torch
from json import load


class Model(Small_LLM_Model):
    """Wrapper around Small_LLM_Model providing convenience methods for
    encoding and decoding."""

    def ft_encode(self, text: str) -> list[int]:
        """Encode text to token IDs.

        Args:
            text: The text to encode.

        Returns:
            List of token IDs.
        """
        token_ids: torch.Tensor = self.encode(text)
        list_token_ids: list[int] = cast(
            list[int], token_ids.squeeze(0).tolist()
        )  # list of token
        return list_token_ids

    def ft_decode(self, list_ids: list[int]) -> str:
        """Decode token IDs to text.

        Args:
            list_ids: List of token IDs to decode.

        Returns:
            The decoded text.
        """
        return self.decode(list_ids)

    def ft_get_logits_from_input_ids(
        self, input_ids: list[int]
    ) -> list[float]:  # get logits from input ids
        """Get logits for the next token given input token IDs.

        Args:
            input_ids: List of input token IDs.

        Returns:
            List of logits for all tokens in the vocabulary.
        """
        logits: list[float] = self.get_logits_from_input_ids(input_ids)
        return logits

    def get_vocab(self) -> dict[str, int]:
        """Load the model vocabulary from file.

        Returns:
            Dictionary mapping tokens to their IDs.
        """
        with open(self.get_path_to_vocab_file(), "r") as f:
            vocab: dict[str, int] = load(f)
        return vocab
