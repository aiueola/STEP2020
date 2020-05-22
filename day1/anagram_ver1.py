#1.純粋なアナグラムを探す
#最初のひとつのみを返すバージョン

import time
start = time.time()

#与えられた辞書の読み込み
#今回は大文字と小文字を区別しなくてよいので，全て小文字に変換した
f = open('txt/dictionary.txt')
eng_dict = f.read()
f.close()
eng_dict = eng_dict.split("\n")
eng_dict = list(map(str.lower, eng_dict))

#入力単語に対し文字の出現回数を数える辞書
alphabets = [chr(i) for i in range(ord('a'), ord('z')+1)]
alphabet_counts = dict.fromkeys(alphabets, 0)

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
    for i in range(len(eng_dict)):
        index = 1 #辞書の単語がアナグラムだったかどうか
        temp_dict = eng_dict[i]
        temp_len = len(temp_dict)
        #辞書内の単語の頭文字が入力文字列に含まれるか，文字列の長さが等しいかで絞込み
        #入力文字のアルファベットを全部使わなくても良い場合は，"temp_len<=word_len"にする
        if (alphabet_counts[temp_dict[0]]>0) and (temp_len==word_len):
            temp_counts = dict.fromkeys(alphabets, 0)
            #辞書内の単語についてもアルファベットの出現回数を調べる
            for j in range(temp_len):
                temp_counts[temp_dict[j]] += 1
            #全てのアルファベットについて，入力単語と辞書内の単語で同じ個数かチェックする
            for k in range(ord('a'), ord('z')+1):
                #入力文字のアルファベットを全部使わなくても良い場合は，"alphabet_counts[chr(k)] < temp_counts[chr(k)]"にする
                if alphabet_counts[chr(k)] != temp_counts[chr(k)]:
                    index = 0
                    break
            if index == 1:
                return temp_dict

found = find_ans(alphabet_counts, eng_dict) 

finish = time.time()

print("実行時間：", finish-start)
print("見つかったアナグラム：", found)
