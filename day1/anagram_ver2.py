#1.純粋なアナグラムを探す
#最初のひとつのみを返すバージョン
#version2(フィードバックを基に改善)
##version1からの変更点は．
#・アナグラムであったかどうかを判定する関数 have_same_alphabet_counts を定義 => indexをなくした
#・temp_dict => dict_word, temp_len => dict_word_len, temp_counts  => dict_word_counts に名称変更
#・dictの初期化をdefaultdictによる実装に変更

import time
from collections import defaultdict

#与えられた辞書の読み込み
#今回は大文字と小文字を区別しなくてよいので，全て小文字に変換した
f = open('txt/dictionary.txt')
eng_dict = f.read()
f.close()
eng_dict = eng_dict.split("\n")
eng_dict = list(map(str.lower, eng_dict))

#入力単語に対し文字の出現回数を数える辞書
alphabets = [chr(i) for i in range(ord('a'), ord('z')+1)]
alphabet_counts = defaultdict(int)

#入力文字を小文字にしてから，長さ取得とアルファベットの出現回数を調べる
#スペースが途中に入っていても大丈夫なようにした
given_word = input().split(" ")
given_word = "".join(list(map(str.lower, given_word)))
word_len = len(given_word)
for i in range(word_len):
    alphabet_counts[given_word[i]] += 1

#ある程度範囲を絞り込んで辞書の中を探していく
#今回は見つかった内一つだけ返せばよいので，全部関数にしてしまう
def find_ans(alpabet_counts, eng_dict):
    #全てのアルファベットについて，入力単語と辞書内の単語で同じ個数かチェックする関数を定義
    #つまり，アナグラムであるかどうか確認する関数
    def have_same_alphabet_counts(alphabet_counts, dict_word_counts):
        for k in range(ord('a'), ord('z')+1):
            #入力文字のアルファベットを全部使わなくても良い場合は，"alphabet_counts[chr(k)] < temp_counts[chr(k)]"にする
            if alphabet_counts[chr(k)] != dict_word_counts[chr(k)]:
                return False
        return True
    
    for i in range(len(eng_dict)):
        dict_word = eng_dict[i]
        dict_word_len = len(dict_word)
        #辞書内の単語の頭文字が入力文字列に含まれるか，文字列の長さが等しいかで絞込み
        #入力文字のアルファベットを全部使わなくても良い場合は，"dict_word_len<=word_len"にする
        if (alphabet_counts[dict_word[0]]>0) and (dict_word_len==word_len):
            dict_word_counts = defaultdict(int)
            #辞書内の単語についてもアルファベットの出現回数を調べる
            for j in range(dict_word_len):
                dict_word_counts[dict_word[j]] += 1
            #全てのアルファベットについて，入力単語と辞書内の単語で同じ個数かチェックする関数を定義
            if have_same_alphabet_counts(alphabet_counts, dict_word_counts):
                return dict_word

start = time.time()

found = find_ans(alphabet_counts, eng_dict) 

finish = time.time()

#実行時間はfind_ansの部分で測る
print("実行時間：", finish-start)
print("見つかったアナグラム：", found)
