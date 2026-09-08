from typing import List, Optional
from ..custom_error import Call_Error


class Node:
    def __init__(self) -> None:
        self.childern: List[Optional["Node"]]= [None] * 255
        self.isLeaf: bool = False


class Trie:
    def __init__(self) -> None:
        self.RootTrie = Node()

    def insert(self, key: str) -> None:
        root_node = self.RootTrie
        for c in key:
            index = ord(c)
            if root_node is None:
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
            if root is None:
                return False
            if root.childern[index] is None:
                return False
            root = root.childern[index]
        if root is None:
            return False
        return root.isLeaf

    def isPrefix(self, key) -> bool:
        root = self.RootTrie
        for c in key:
            index = ord(c)
            if root is None:
                return False
            if root.childern[index] is None:
                return False
            root = root.childern[index]
        return True

    def clean_trie(self) -> None:
        self.RootTrie = Node()
