class Node:
    def __init__(self, value: int | None = None) -> None:
        self.children: dict[int, Node] = dict()
        self.value: int | None = value
        self.isLeaf: bool = False
        self.is_end: bool = True


class Trie:
    def __init__(self) -> None:
        self.__root_node: Node = Node()

    def __insert(self, ids: list[int]) -> None:
        current_node: Node = self.__root_node
        for id in ids:
            if id not in current_node.children.keys():
                current_node.children[id] = Node(id)
            current_node = current_node.children[id]
        current_node.isLeaf = True

    def get_children(self, ids: list[int]) -> list[int]:
        current_node: Node = self.__root_node
        for id in ids:
            if id not in current_node.children.keys():
                return []
            current_node = current_node.children[id]
        return list(current_node.children.keys())

    def insert_many(self, ids: list[list[int]]) -> None:
        for ids_row in ids:
            self.__insert(ids_row)


if __name__ == "__main__":
    ids: list[list[int]] = [[12, 434, 434, 5343], [12, 4343242, 4231231, 321321]]
    trie: Trie = Trie()
    trie.insert_many(ids)
    print(trie.get_children([12, 333213, 32321]))
