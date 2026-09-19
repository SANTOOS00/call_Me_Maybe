class Node:
    """Represent one node in a token prefix tree.

    Args:
        value: Token value stored at this node, if any.
    """

    def __init__(self, value: int | None = None) -> None:
        """Initialize a trie node."""
        self.children: dict[int, Node] = dict()
        self.isLeaf: bool = False


class Trie:
    """Store and query sequences of token identifiers."""

    def __init__(self) -> None:
        """Initialize an empty trie."""
        self.__root_node: Node = Node()

    def __insert(self, ids: list[int]) -> None:
        """Insert one token sequence into the trie.

        Args:
            ids: Token identifiers forming the sequence.
        """
        current_node: Node = self.__root_node
        for id in ids:
            if id not in current_node.children.keys():
                current_node.children[id] = Node(id)
            current_node = current_node.children[id]
        current_node.isLeaf = True

    def get_children(self, ids: list[int]) -> list[int]:
        """Return tokens that can follow a token prefix.

        Args:
            ids: Token prefix to inspect.

        Returns:
            Child token identifiers, or an empty list if the prefix is absent.
        """
        current_node: Node = self.__root_node
        for id in ids:
            if id not in current_node.children.keys():
                return []
            current_node = current_node.children[id]
        return list(current_node.children.keys())

    def insert_many(self, ids: list[list[int]]) -> None:
        """Insert multiple token sequences.

        Args:
            ids: Token sequences to insert.
        """
        for ids_row in ids:
            self.__insert(ids_row)

    def search(self, token_id: list[int]) -> bool:
        """Check whether a token sequence is stored as a complete entry.

        Args:
            token_id: Token sequence to search for.

        Returns:
            Whether the sequence terminates at a leaf node.
        """
        current_node: Node = self.__root_node
        for id in token_id:
            current_node = current_node.children[id]
        return current_node.isLeaf
