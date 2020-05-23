#入力は，
#<page_name url>
#例
#a.com aaa

from collections import deque, defaultdict

order = deque()
cache = defaultdict(str)

def process(order, cache, new_page, url, x):
    if len(cache[new_page])==0:
        if len(order) >= x:
            del cache[order.popleft()]
        cache[new_page] = url
        print('there was no cache, and added a new cache')
    else:
        found = cache[new_page]
        order.remove(new_page)
        print('cache exists, ', found)
    order.append(new_page)

print('input the numbers of cache:')
x = int(input())
print('input <page_name url>')
for i in range(6):
    inp = input().split()
    process(order, cache, inp[0], inp[1], x)
    print(order)
    print(cache)

########################################################################################

#outputs are like this:

#input the numbers of cache:
#3

#input <page_name url>
#a.com aaa
#there was no cache, and added a new cache
#deque(['a.com'])
#defaultdict(<class 'str'>, {'a.com': 'aaa'})

#b.com bbb
#there was no cache, and added a new cache
#deque(['a.com', 'b.com'])
#defaultdict(<class 'str'>, {'a.com': 'aaa', 'b.com': 'bbb'})

#c.com ccc
#there was no cache, and added a new cache
#deque(['a.com', 'b.com', 'c.com'])
#defaultdict(<class 'str'>, {'a.com': 'aaa', 'b.com': 'bbb', 'c.com': 'ccc'})

#d.com ddd
#there was no cache, and added a new cache
#deque(['b.com', 'c.com', 'd.com'])
#defaultdict(<class 'str'>, {'b.com': 'bbb', 'c.com': 'ccc', 'd.com': 'ddd'})

#a.com aaa
#there was no cache, and added a new cache
#deque(['c.com', 'd.com', 'a.com'])
#defaultdict(<class 'str'>, {'c.com': 'ccc', 'd.com': 'ddd', 'a.com': 'aaa'})

#d.com ddd
#cache exists,  ddd
#deque(['c.com', 'a.com', 'd.com'])
#defaultdict(<class 'str'>, {'c.com': 'ccc', 'd.com': 'ddd', 'a.com': 'aaa'})
