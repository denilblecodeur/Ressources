trie = [-1] * (27 * 1000000) # 10^6 for 10^5 words, 5*10^5 seems to work too
j = 27
#insert list of words
for w in words:
    i = 0
    for char in w:
        c = ord(char) - 97 # if char lowercase
        if trie[i + c] == -1:
            trie[i + c] = j
            j += 27
        i = trie[i + c]
    trie[i + 26] = 1
#check if w in trie
i = 0
for char in w:
    c = ord(char) - 97 # if char lowercase
    i = trie[i + c]
    if i == -1:
        break
    if trie[i + 26] == 1:
        # this is a valid word
        pass

### SIMPLER

n = int(input())
trie = {}
for _ in range(n):
    w = input()
    root = trie
    for c in w:
        if c not in root:
            root[c] = {}
        root = root[c]

def check(root, d):
    good = d%2
    for l in root.keys():
        if d%2:
            good &= check(root[l], d+1)
        else:
            good |= check(root[l], d+1)
    return good

### BS

class TrieNode:
    def __init__(self):
        self.children = [None] * 26
        self.isEndOfWord = False
 
class Trie:
    def __init__(self):
        self.root = TrieNode()
    def _charToIndex(self, ch):
        return ord(ch) - 97
    def insert(self, key):
        # If not present, inserts key into trie
        # If the key is prefix of trie node,
        # just marks leaf node
        node = self.root
        length = len(key)
        for level in range(length):
            index = self._charToIndex(key[level])
            # if current character is not present
            if not node.children[index]:
                node.children[index] = TrieNode()
            node = node.children[index]
        # mark last node as leaf
        node.isEndOfWord = True