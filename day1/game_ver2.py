#ゲーム
#ver2.
##ver1からの変更点は，
#・アナグラムであったかどうかを判定する関数 have_same_alphabet_counts を定義 => indexをなくした
#・temp_dict => dict_word, temp_len => dict_word_len, temp_counts  => dict_word_counts に名称変更
#・dictの初期化をdefaultdictによる実装に変更
#・'qu'を'q'としてそのまま処理する実装に変更
#・テスト入力が面倒だったので，入力形式を簡単な方法に変更

##入力の形式は，文字ベクトル(サイトからコピー&ペーストでOK)
##例
#B U L T S Qu X A H Y O E G V Y D

import time
from collections import defaultdict

start = time.time()

#与えられた辞書の読み込み
#今回は大文字と小文字を区別しなくてよいので，全て小文字に変換した．
f = open('txt/dictionary.txt')
eng_dict = f.read()
f.close()
eng_dict = eng_dict.split("\n")
eng_dict = list(map(str.lower, eng_dict))

#入力単語に対し文字の出現回数を数える辞書
alphabet_counts = defaultdict(int)

#文字と点数の対応
points = defaultdict(int)
for string in ['a', 'b', 'd', 'e', 'g', 'i', 'n', 'o', 'r', 's', 't', 'u']:
    points[string] = 1
for string in ['c', 'f', 'h', 'l', 'm', 'p', 'v', 'w', 'y']:
    points[string] = 2
for string in ['j', 'k', 'q', 'x', 'z']:
    points[string] = 3

#入力の受け取り
word_len = 16
input_str = input().split()
input_str = list(map(str.lower, input_str))
for i in range(16):
    if input_str[i] == 'qu':
        alphabet_counts['q'] += 1
        word_len += 1
    else:
        alphabet_counts[input_str[i]] += 1

#全てのアルファベットについて，入力単語と辞書内の単語で同じ個数かチェックする関数を定義
#つまり，アナグラムであるかどうか確認する関数
def have_same_alphabet_counts(alphabet_counts, dict_word_counts):
    for k in range(ord('a'), ord('z')+1):
        if alphabet_counts[chr(k)] < dict_word_counts[chr(k)]:
            return False
    return True

found = []
#アナグラムになっている単語を全列挙する部分
for i in range(len(eng_dict)):
    dict_word = eng_dict[i]
    dict_word_len = len(dict_word)
    #辞書内の単語の頭文字が入力文字列に含まれるか，文字列の長さが等しいかで絞込み
    if (alphabet_counts[dict_word[0]]>0) and (dict_word_len<=word_len):
        dict_word_counts = defaultdict(int)
        #辞書内の単語についてもアルファベットの出現回数を調べる
        for j in range(dict_word_len):
            if dict_word[j] == 'q':
                dict_word_counts['q'] += 1
                dict_word_counts['u'] -= 1
            else:
                dict_word_counts[dict_word[j]] += 1
        #全てのアルファベットについて，入力単語と辞書内の単語で同じ個数かチェック，アナグラムになっているかの確認
        if have_same_alphabet_counts(alphabet_counts, dict_word_counts):
            found.append(dict_word)

#辞書の中の文字列の点数を算出する関数
def calc(word, points):
    score = points[word[0]]
    for i in range(1, len(word)):
        if ((word[i]!='u')or(word[i-1]!='q')):
            score += points[word[i]]
    return score

#見つかったアナグラムから点数の高い文字列を探す部分
max_point = 0
best_str = ''
for word in found:
    temp_point = calc(word, points)
    if (temp_point > max_point):
        max_point = temp_point
        best_str = word

finish = time.time()

print("実行時間：", finish-start)
print("見つかったアナグラム：", best_str)
