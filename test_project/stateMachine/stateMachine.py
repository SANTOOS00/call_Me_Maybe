from typing import List, Optional


class Node:
    def __init__(self) -> None:
        self.childern: List[Optional[Node]]= [None] * 255
        self.isLeaf: bool = False


class Trie:
    def __init__(self) -> None:
        self.RootTrie = Node()

    def insert(self, string: str) -> None:
        root_node = self.RootTrie
        for c in string:
            index = ord(c)
            if root_node.childern[index] is None:
                root_node.childern[index] = Node()
            root_node = root_node.childern[index]
        root_node.isLeaf = True



def main() -> None:
    # print(chr(ord('È') + ord('8')))
    # print(chr(ord("1") + ord("z") + ord("z")))


    # ss = ["edew", "egwt","aaaa"]
    # print(max([len(st) for st in ss]))

 
    # function = ["and", "ant", "dad", "do"]
    # trie = Trie()
    # for fu in function:
    #     trie.insert(fu)

    string = "sim santoos"

    for ch in string:
        print(ch)
        string = string.replace(ch , "", 1)
    print(string)
            

# print(s[:i] + s[i+1:])
if __name__ == "__main__":
    main()
