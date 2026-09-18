from typing_extensions import override


class TokensValid:
    """Represents a node in a token tree structure for valid token sequences.

    Attributes:
        curent_token: The token ID at this node.
        children: Dictionary of child nodes keyed by token ID.
    """

    def __init__(self, curent_token: None | int = None) -> None:
        """Initialize a token tree node.

        Args:
            curent_token: The token ID for this node.
        """
        self.curent_token: int | None = curent_token
        self.children: dict[int, "TokensValid"] = {}

    @override
    def __eq__(self, value: object) -> bool:
        """Check equality based on token value.

        Args:
            value: The object to compare.

        Returns:
            True if both objects have the same token value.
        """
        if isinstance(value, TokensValid):
            return value.curent_token == self.curent_token
        return False


class GuideModel:
    """Constrained token generation guide using a tree of valid token sequences

    Attributes:
        tokens_valid: List of valid token sequences.
        head_tokens: Root node of the token tree.
    """

    def __init__(self, tokens_valid: list[list[int]]) -> None:
        """Initialize the guide model with valid token sequences.

        Args:
            tokens_valid: List of valid token sequences to constrain generation
        """
        self.tokens_valid: list[list[int]] = tokens_valid
        self.head_tokens: TokensValid = TokensValid()
        self.__implement_tree_of_tokens()

    def __add_or_get_head(self, value: int) -> TokensValid:
        """Get or create a head token node.

        Args:
            value: The token ID.

        Returns:
            The head token node for the given value.
        """
        for token_id, _ in self.head_tokens.children.items():
            if token_id == value:
                return self.head_tokens.children[token_id]
        new_token: TokensValid = TokensValid(value)
        self.head_tokens.children[value] = new_token
        return new_token

    def __get_children(
        self, head: TokensValid, children_value: int
    ) -> TokensValid:  # get children
        """Get or create a child token node.

        Args:
            head: The parent token node.
            children_value: The token ID for the child.

        Returns:
            The child token node.
        """
        for key, children in head.children.items():
            if key == children_value:
                return children
        new_children: TokensValid = TokensValid(children_value)
        head.children[children_value] = new_children
        return new_children

    def __implement_tree_of_tokens(self) -> None:
        """Build a tree structure from valid token sequences."""
        for row in self.tokens_valid:
            head: TokensValid = self.__add_or_get_head(row[0])
            for item in row[1:]:
                head = self.__get_children(head, item)

    def __get_object(self, value: list[int]) -> TokensValid:
        """Get a token node from a sequence of token IDs.

        Args:
            value: Sequence of token IDs.

        Returns:
            The token node at the end of the sequence.
        """
        if len(value) == 1:
            return self.__add_or_get_head(value[0])

        head_token: TokensValid = self.__add_or_get_head(value[0])
        for token in value[1:]:
            head_token = head_token.children[token]

        return head_token

    def get_the_valid_tokens(self, token_ids: list[int] | None) -> list[int]:
        """Get valid next tokens based on the sequence generated so far.

        Args:
            token_ids: The sequence of token IDs generated so far.

        Returns:
            List of valid token IDs for the next position.
        """
        if not token_ids:
            return [value for value, _ in self.head_tokens.children.items()]
        head_token: TokensValid = self.__get_object(token_ids)
        return [key for key, _ in head_token.children.items()]
