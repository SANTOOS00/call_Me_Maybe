from llm_sdk import Small_LLM_Model
from typing import cast


class ManagerLLM(Small_LLM_Model):
    """Adapt the language model interface used by the generators."""

    def __init__(
        self,
        model_name: str = "Qwen/Qwen3-0.6B",
    ) -> None:
        """Initialize the model manager.

        Args:
            model_name: Name of the language model to load.
        """
        super().__init__(model_name)

    def custom_encoder(self, prompt: str) -> list[int]:
        """Encode a prompt into integer token identifiers.

        Args:
            prompt: Text to encode.

        Returns:
            Encoded token identifiers.
        """
        return [int(p_id) for p_id in cast(list[int], self.encode(prompt)[0])]

    def get_logits(self, generator_ids: list[int]) -> list[float]:
        """Return logits for a sequence of token identifiers.

        Args:
            generator_ids: Input token identifiers.

        Returns:
            Logit scores for the next token.
        """
        return self.get_logits_from_input_ids(generator_ids)

    def decode_token(self, token_id: int) -> str:
        """Decode one token identifier into text.

        Args:
            token_id: Token identifier to decode.

        Returns:
            Decoded token text.
        """
        return self.decode([token_id])

    def mask_logits(
        self, context_ids: list[int], hight_socres: list[int] | None = None
    ) -> list[float]:
        """Return logits restricted to selected high-scoring tokens.

        Args:
            context_ids: Context token identifiers.
            hight_socres: Allowed token identifiers, if restricting scores.

        Returns:
            Logits for the next token, with disallowed values masked.
        """
        logits = self.get_logits_from_input_ids(context_ids)
        if hight_socres is None:
            return logits
        for token_id, _ in enumerate(logits):
            if token_id not in hight_socres:
                logits[token_id] = float("-inf")
        return logits

    def encoder_chr_by_chr(self, prompt: list[str]) -> list[int]:
        """Encode each supplied text fragment and take its first token.

        Args:
            prompt: Text fragments to encode.

        Returns:
            The first token identifier for each fragment.
        """
        token_ids: list[int] = []
        for character in prompt:
            token_ids.append(self.custom_encoder(character)[0])
        return token_ids
