# from typing import List, Optional


# class Node:
#     def __init__(self) -> None:
#         self.childern: List[Optional[Node]]= [None] * 255
#         self.isLeaf: bool = False


# class Trie:
#     def __init__(self) -> None:
#         self.RootTrie = Node()

#     def insert(self, string: str) -> None:
#         root_node = self.RootTrie
#         for c in string:
#             index = ord(c)
#             if root_node.childern[index] is None:
#                 root_node.childern[index] = Node()
#             root_node = root_node.childern[index]
#         root_node.isLeaf = True



def main() -> None:
    ss = ["sssss", "sssssss"]
    print("".join([s for s in ss]))


if __name__ == "__main__":
    main()
