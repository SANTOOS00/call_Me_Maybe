from typing import List, Optional


class Node:
    def __init__(self) -> None:
        self.childern: List[Node]= [] * 255
        self.isLeaf: bool = False


class Trie:
    def __init__(self) -> None:
        self.RootTrie = Node()

    def insert(self, string: str) -> None:
        root_node = self.RootTrie
        for c in string:
            index = ord(c) - ord('\0')
            if not root_node.childern[index]:
                root_node.childern[index] = Node()
            root_node = root_node.childern[index]
        root_node.isLeaf = True



def main() -> None:
    function = ["and", "ant", "dad", "do"]
    trie = Trie()
    for fu in function:
        trie.insert(fu)

if __name__ == "__main__":
    main()
