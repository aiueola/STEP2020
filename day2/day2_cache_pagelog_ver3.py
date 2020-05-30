def process(cache, url, contents, length, x):
    #データ構造は辞書に紐づけて，cache[url] = [contents, ひとつ前に閲覧したurl，ひとつ後に閲覧したurl]の順で保持
    #また，一番古い閲覧履歴と一番新しい閲覧履歴を，flag = [一番古い閲覧url, 一番新しい閲覧url]として保持
    global head
    global tail
    found_contents = None
    if x==1:
        if url in cache:
            return length, cache[url]
        else:
            cache.clear()
            cache[url] = contents
            return length, found_contents
    if url not in cache:
        #訪れたurlがcacheになく，かつcacheが全て埋まっていたら，古いcacheを一つ捨てるようにする．
        cache[url] = [contents, "head", "tail"] #前後のページは0で初期化
        length += 1
        if length == 1:
            head = url
            tail = url
            return length, found_contents
        else:
            if length > x:
                next_head = cache[head][2]
                del cache[head]
                head = next_head
                cache[head][1] = "head" #一番最初になったら"head"に初期化
                length -= 1
            cache[tail][2] = url
    else:
        #訪れたurlがcache内に存在していたら，その部分を抜き取って前後のcacheを繋げるようにする．
        found_contents = cache[url][0]
        #cacheが先頭だった場合，場合分けが必要
        if cache[url][1] == "head":
            head = cache[head][2]
            cache[head][1] = "head" #一番最初になったら0に初期化
        #cacheの末尾だった場合も，場合分けが必要(なにもしない)
        elif cache[url][2] == "tail":
            return length, found_contents
        else:
            before = cache[url][1]
            after = cache[url][2]
            cache[before][2] = after
            cache[after][1] = before
            cache[tail][2] = url
    #訪れたurlの部分をデータ構造の最後に追加する．
    cache[url][1] = tail
    tail = url
    return length, found_contents

print('input the numbers of cache:')
x = int(input())
print()
#以下，初期化
cache = dict()
head = "head"
tail = "tail"
length = 0

print('input <url contents>')
for i in range(6):
    inp = input().split()
    length, found_contents = process(cache, inp[0], inp[1], length, x)
    if (found_contents):
        print('cache exists, ', inp[0])
    else:
        print('cache did not exist, and added to cache, ', inp[0])
    print('current cache are, ', list(cache.keys()))
    print()

###################################################################################################
#input the numbers of cache:
#3

#input <url contents>
#a.com aaa
#cache did not exist, and added to cache,  a.com
#current cache are,  ['a.com']

#b.com bbb
#cache did not exist, and added to cache,  b.com
#current cache are,  ['a.com', 'b.com']

#c.com ccc
#cache did not exist, and added to cache,  c.com
#current cache are,  ['a.com', 'b.com', 'c.com']

#a.com aaa
#cache exists,  a.com
#current cache are,  ['a.com', 'b.com', 'c.com']

#d.com ddd
#cache did not exist, and added to cache,  d.com
#current cache are,  ['a.com', 'c.com', 'd.com']

#a.com aaa
#cache exists,  a.com
#current cache are,  ['a.com', 'c.com', 'd.com']
