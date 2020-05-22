#ゲーム
##入力の形式は，文字のマトリックス
##例
#O A N G
#K Qu S B
#G H D T
#L C Y J

import time
start = time.time()

#与えられた辞書の読み込み
#今回は大文字と小文字を区別しなくてよいので，全て小文字に変換した．
f = open('txt/dictionary.txt')
eng_dict = f.read()
f.close()
eng_dict = eng_dict.split("\n")
eng_dict = list(map(str.lower, eng_dict))

#入力単語に対し文字の出現回数を数える辞書
alphabets = [chr(i) for i in range(ord('a'), ord('z')+1)]
alphabet_counts = dict.fromkeys(alphabets, 0)

#文字と点数の対応
points = dict.fromkeys(alphabets, 1)
for string in ['c', 'f', 'h', 'l', 'm', 'p', 'v', 'w', 'y']:
    points[string] += 1
for string in ['j', 'k', 'q', 'x', 'z']:
    points[string] += 2

#入力の受け取り
word_len = 16
given_str = []
for i in range(4):
    str_matrix = input().split()
    str_matrix = list(map(str.lower, str_matrix))
    given_str.extend(str_matrix)
    for j in range(4):
        if str_matrix[j] == "qu":
            alphabet_counts['q'] += 1
            alphabet_counts['u'] += 1
            word_len += 1
        else:
            alphabet_counts[str_matrix[j]] += 1

#ある程度範囲を絞り込んで辞書の中を探していく．
found = []
for i in range(len(eng_dict)):
    index = 1 #辞書の単語がアナグラムだったかどうか．
    temp_dict = eng_dict[i]
    temp_len = len(eng_dict[i])
    #辞書内の単語の頭文字が入力文字列に含まれるか，文字列の長さが入力文字列より短いかで絞込み
    if (alphabet_counts[temp_dict[0]]>0) and (temp_len<=word_len):
        temp_counts = dict.fromkeys(alphabets, 0)
        #辞書内の単語についてもアルファベットの出現回数を調べる
        for j in range(temp_len):
            temp_counts[temp_dict[j]] += 1
        #全てのアルファベットについて入力単語と辞書内の単語で同じ個数かチェックする
        for k in range(ord('a'), ord('z')+1):
            if alphabet_counts[chr(k)] < temp_counts[chr(k)]:
                index = 0
                break
        if index==1:
            found.append(temp_dict)

#辞書の中の文字列の点数を算出する関数
def calc(word, points):
    score = points[word[0]]
    for i in range(1, len(word)):
        if ((word[i]!='u')or(word[i-1]!='q')):
            score += points[word[i]]
    return score

#点数の高い文字列を探す
max_point = 0
best_str = ''
for word in found:
    judge = 1 #本当に使ってよい文字列化どうかの判定，"Qu"対策
    temp_point = calc(word, points)
    if (temp_point > max_point):
        if 'u' in word:
            available_u = alphabet_counts['u'] - alphabet_counts['q']
            only_u = 0
            if word[0]=='u':
                only_u+=1
            for i in range(1, len(word)):
                if word[i]=='u' and word[i-1]!='q':
                    only_u += 1
            if only_u > available_u:
                judge = 0
        if judge == 1:
            max_point = temp_point
            best_str = word

finish = time.time()

print("実行時間：", finish-start)
print("見つかったアナグラム：", best_str)
