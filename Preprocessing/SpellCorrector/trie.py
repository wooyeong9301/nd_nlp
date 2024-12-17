# class Node(object):
#     def __init__(self, key, data=None):
#         self.key = key
#         self.data = data
#         self.children = {}
#
# class Trie(object):
#     def __init__(self):
#         self.head = Node(None)
#
#     def insert(self, string):
#         curr_node = self.head
#
#         for char in string:
#             if char not in curr_node.children:
#                 curr_node.children[char] = Node(char)
#
#             curr_node = curr_node.children[char]
#
#         curr_node.data = string
#
#     def search(self, string):
#         curr_node = self.head
#
#         for char in string:
#             if char in curr_node.children:
#                 curr_node = curr_node.children[char]
#             else:
#                 return False
#
#         if curr_node.data is not None:
#             return True


class Node:
    def __init__(self):
        self.word = False
        self.children = {}

class Trie:
    def __init__(self):
        self.root = Node()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = Node()
            node = node.children[char]
        node.word = True

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.word

    def startswith(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True

trie = Trie()
trie.insert('abcd')
trie.insert('ab')
trie.insert('abdegs')
trie.insert('power')
trie.insert('superpower')
print(trie.search('abcd'))
print(trie.search('abc'))
print(trie.startswith('ab'))


hash_table = [0 for i in range(26)]
print(hash_table, len(hash_table))

def hash_func(key):
    return key % 52

data1 = 'Abraham'
data2 = 'hello'
data3 = 'war'
data4 = 'home'

print('1', ord(data1[0]), ord(data2[0]), ord(data3[0]), ord(data4[0]))
print('2', ord(data1[0]), hash_func(ord(data1[0])))
print('3', ord(data2[0]), hash_func(ord(data2[0])))
print('4', ord('A'), ord('Z'), ord('a'))


def storage_data(data, value):
    key = ord(data[0])
    hash_address = hash_func(key)
    hash_table[hash_address] = value


storage_data(data1, '01010001')
storage_data(data2, '01010002')
storage_data(data3, '01010003')
storage_data(data4, '01010004')

print(hash_table)


def get_data(data):
    key = ord(data[0])
    hash_address = hash_func(key)
    return hash_table[hash_address]

print(get_data(data2))









# for _ in range(65,123):
#     print(_, _ % 52)

# upper_chr = list(range(65,91))
# lower_chr = list(range(97,123))
#
# for i in lower_chr:
#     print(chr(i), end=' ')
#
# print('\n')


# test_dict = {('a','address'):14}
# print(test_dict)