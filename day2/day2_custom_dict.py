class CustomDict:
    def __init__(self, n):
        self.n = n
        self.custom_dict = [[] for i in range(self.n)]
        pass

    def hash_converter(self, key):
        return ord(str(key)[0])%self.n  #今回はごく簡単なhash関数

    def add_to_dict(self, key, value):
        if [key, value] in self.custom_dict[self.hash_converter(key)]:
            print('the value for "{}" has already existed in dict'.format(key))
        else:
            self.custom_dict[self.hash_converter(key)].append([key, value])
            print('successfully added value for "{}" in c_dict'.format(key))
        pass

    def remove_from_dict(self, key, value):
        if [key, value] in self.custom_dict[self.hash_converter(key)]:  #ここはO(N)
            self.custom_dict[self.hash_converter(key)].remove([key, value])
            print('successfully removed value for "{}" in c_dict'.format(key))
        else:
            print('could not remove value for "{}" in dict, because "{}" did not exist in dict'.format(key, key))
        pass

    def find_in_dict(self, key):
        for stored_in_dict in self.custom_dict[self.hash_converter(key)]:  #ここもO(N)
            if stored_in_dict[0] == key:
               print('value for "{}" found in c_dict, '.format(key), stored_in_dict[1])
               return
        print('value for "{}" did not exist in c_dict'.format(key))
        return
        pass

def test():
    c_dict = CustomDict(4)
    print(c_dict.custom_dict)
    c_dict.add_to_dict('a', 'A')
    print(c_dict.custom_dict)
    c_dict.add_to_dict('b', 'B')
    print(c_dict.custom_dict)
    c_dict.add_to_dict('c', 'C')
    print(c_dict.custom_dict)
    c_dict.add_to_dict('e', 'E')
    print(c_dict.custom_dict)
    c_dict.add_to_dict('i', 'I')
    print(c_dict.custom_dict)
    c_dict.remove_from_dict('e', 'E')
    print(c_dict.custom_dict)
    c_dict.remove_from_dict('b', 'B')
    print(c_dict.custom_dict)
    c_dict.remove_from_dict('d', 'D')
    print(c_dict.custom_dict)
    c_dict.find_in_dict('a')
    c_dict.find_in_dict('e')
    c_dict.find_in_dict('z')
    print('OK!')

if __name__ == "__main__":
    test()

########################################################################
#[[], [], [], []]
#successfully added value for "a" in c_dict
#[[], [['a', 'A']], [], []]
#successfully added value for "b" in c_dict
#[[], [['a', 'A']], [['b', 'B']], []]
#successfully added value for "c" in c_dict
#[[], [['a', 'A']], [['b', 'B']], [['c', 'C']]]
#successfully added value for "e" in c_dict
#[[], [['a', 'A'], ['e', 'E']], [['b', 'B']], [['c', 'C']]]
#successfully added value for "i" in c_dict
#[[], [['a', 'A'], ['e', 'E'], ['i', 'I']], [['b', 'B']], [['c', 'C']]]
#successfully removed value for "e" in c_dict
#[[], [['a', 'A'], ['i', 'I']], [['b', 'B']], [['c', 'C']]]
#successfully removed value for "b" in c_dict
#[[], [['a', 'A'], ['i', 'I']], [], [['c', 'C']]]
#could not remove value for "d" in dict, because "d" did not exist in dict
#[[], [['a', 'A'], ['i', 'I']], [], [['c', 'C']]]
#value for "a" found in c_dict,  A
#value for "e" did not exist in c_dict
#value for "z" did not exist in c_dict
#OK!
