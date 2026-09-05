from typing import List, Optional, Self
from ..custom_error import Call_Error


class Node:
    def __init__(self) -> None:
        self.childern: List[Optional["Node"]]= [None] * 255
        self.isLeaf: bool = False


class Trie:
    _instance = None
    def __new__(cls) -> Self:
        if cls._insert is None:
            cls._insert = super().__new__(cls)
        return cls._insert

    def __init__(self) -> None:
        self.RootTrie = Node()

    def insert(self, key: str) -> None:
        root_node = self.RootTrie
        for c in key:
            index = ord(c)
            if index > 255 or root_node is None:
                raise Call_Error("")
            if root_node.childern[index] is None:
                root_node.childern[index] = Node()
            root_node = root_node.childern[index]
        if root_node is not None:
            root_node.isLeaf = True

    def search(self, key) -> bool:
        root = self.RootTrie
        for c in key:
            index = ord(c)
            if index > 255 or root is None:
                return False
            if root.childern[index] is None:
                return False
            root = root.childern[index]
        if root is None:
            return False
        return root.isLeaf
    