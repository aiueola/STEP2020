class CustomDict:
    def __init__(self, n):
        self.n = n
        self.custom_dict = [[] for i in range(self.n)]
        pass

    def hash_converter(self, flag):
        return ord(str(flag)[0])%self.n  #今回はごく簡単なhash関数

    def add_to_dict(self, flag, content):
        if [flag, content] in self.custom_dict[self.hash_converter(flag)]:
            print('the content for "{}" has already existed in dict'.format(flag))
        else:
            self.custom_dict[self.hash_converter(flag)].append([flag, content])
            print('successfully added content for "{}" in c_dict'.format(flag))
        pass

    def remove_from_dict(self, flag, content):
        if [flag, content] in self.custom_dict[self.hash_converter(flag)]:
            self.custom_dict[self.hash_converter(flag)].remove([flag, content])
            print('successfully removed content for "{}" in c_dict'.format(flag))
        else:
            print('could not remove content for "{}" in dict, because "{}" did not exist in dict'.format(flag, flag))
        pass

    def find_in_dict(self, flag):
        for stored_in_dict in self.custom_dict[self.hash_converter(flag)]:  #ここもO(N)
            if stored_in_dict[0] == flag:
               print('contents for "{}" found in c_dict, '.format(flag), stored_in_dict[1])
               return
        print('contents for "{}" did not exist in c_dict'.format(flag))
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
#successfully added content for "a" in c_dict
#[[], [['a', 'A']], [], []]
#successfully added content for "b" in c_dict
#[[], [['a', 'A']], [['b', 'B']], []]
#successfully added content for "c" in c_dict
#[[], [['a', 'A']], [['b', 'B']], [['c', 'C']]]
#successfully added content for "e" in c_dict
#[[], [['a', 'A'], ['e', 'E']], [['b', 'B']], [['c', 'C']]]
#successfully added content for "i" in c_dict
#[[], [['a', 'A'], ['e', 'E'], ['i', 'I']], [['b', 'B']], [['c', 'C']]]
#successfully removed content for "e" in c_dict
#[[], [['a', 'A'], ['i', 'I']], [['b', 'B']], [['c', 'C']]]
#successfully removed content for "b" in c_dict
#[[], [['a', 'A'], ['i', 'I']], [], [['c', 'C']]]
#could not remove content for "d" in dict, because "d" did not exist in dict
#[[], [['a', 'A'], ['i', 'I']], [], [['c', 'C']]]
#contents for "a" found in c_dict,  A
#contents for "e" did not exist in c_dict
#contents for "z" did not exist in c_dict
#OK!
