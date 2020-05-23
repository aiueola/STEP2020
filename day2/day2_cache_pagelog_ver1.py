#入力は，
#<url contents>
#例
#a.com aaa

from collections import deque, defaultdict

order = deque()
cache = defaultdict(str)

def process(order, cache, url, contents, x):
    if len(cache[url])==0:
        if len(order) >= x:
            del cache[order.popleft()]
        cache[url] = contents
        print('there was no cache, and added a new cache')
    else:
        found = cache[url]
        order.remove(url)
        print('cache exists, ', found)
    order.append(url)

print('input the numbers of cache:')
x = int(input())
print()
print('input <url contents>')
for i in range(6):
    inp = input().split()
    process(order, cache, inp[0], inp[1], x)
    print(order)
    print(cache)
    print()
    
##################################################################################
#input the numbers of cache:
#3

#input <url contents>
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

#a.com aaa
#cache exists,  aaa
#deque(['b.com', 'c.com', 'a.com'])
#defaultdict(<class 'str'>, {'a.com': 'aaa', 'b.com': 'bbb', 'c.com': 'ccc'})

#d.com ddd
#there was no cache, and added a new cache
#deque(['c.com', 'a.com', 'd.com'])
#defaultdict(<class 'str'>, {'a.com': 'aaa', 'c.com': 'ccc', 'd.com': 'ddd'})

#a.com aaa
#cache exists,  aaa
#deque(['c.com', 'd.com', 'a.com'])
#defaultdict(<class 'str'>, {'a.com': 'aaa', 'c.com': 'ccc', 'd.com': 'ddd'})
