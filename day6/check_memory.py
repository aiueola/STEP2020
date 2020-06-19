def print_id(x, str_x):
    print('id({}): %#08x'.format(str_x) % id(x))
    for i in range(len(x)):
        print('id({}[{}]): %#08x'.format(str_x, i) % id(x[i]))
    print()

def foo(b):
    b.append(2)
    print('b:', b)
    print_id(b, 'b')

    b = b + [3]
    b.append(4)
    print('b:', b)
    print_id(b, 'b')

a = [1]
print('before foo()')
print('a:', a)
print_id(a, 'a')

print('while in foo()')
foo(a)

print('after foo()')
print('a:', a)
print_id(a, 'a')

# ============================================================
# before foo()
# a: [1]
# id(a): 0x7fc2a191c348
# id(a[0]): 0xa68ac0
#
# while in foo()
# b: [1, 2]
# id(b): 0x7fc2a191c348
# id(b[0]): 0xa68ac0
# id(b[1]): 0xa68ae0
# 
# b: [1, 2, 3, 4]
# id(b): 0x7fc2a191c3c8
# id(b[0]): 0xa68ac0
# id(b[1]): 0xa68ae0
# id(b[2]): 0xa68b00
# id(b[3]): 0xa68b20
# 
# after foo()
# a: [1, 2]
# id(a): 0x7fc2a191c348
# id(a[0]): 0xa68ac0
# id(a[1]): 0xa68ae0
