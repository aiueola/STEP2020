import sys

#数字を小数点以下含めて最後まで読み取る
def readNumber(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        keta = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * keta
            keta /= 10
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index

#演算子を読み取る
def readOperator(line, index):
    if line[index] == '+':
        token = {'type': 'OPERATOR', 'operator':'PLUS'}
    elif line[index] == '-':
        token = {'type': 'OPERATOR', 'operator':'MINUS'}
    elif line[index] == '*':
        token = {'type': 'OPERATOR', 'operator':'MULTIPLE'}
    elif line[index] == '/':
        token = {'type': 'OPERATOR', 'operator':'DIV'}
    return token, index + 1

#括弧を読み取る
def readBracket(line, index):
    if line[index] == '(':
        token = {'type': 'leftB'}
    else:
        token = {'type': 'rightB'}
    return token, index + 1

#入力を 数字，演算子，括弧 に分割
def tokenize(line):
  tokens = []
  index = 0
  while index < len(line):
      if line[index].isdigit():
          (token, index) = readNumber(line, index)
      elif line[index] in ['+', '-', '*', '/']:
          (token, index) = readOperator(line, index)
      elif line[index] in ['(', ')']:
          (token, index) = readBracket(line, index)
      else:
          print('Invalid character found: ' + line[index])
          sys.exit(1)
      tokens.append(token)
  return tokens

#入力された計算式が数学のルールに従うかチェックする
def check_syntax(tokens):
    #左括弧は +1, 右括弧は -1 とし，左括弧と右括弧の出現回数のバランスを見る変数
    bracket_balance = 0
    #数字か左括弧で始まり，
    if tokens[0]['type'] not in ['NUMBER', 'leftB']:
        return False
    #数字か右括弧で終わる
    if tokens[-1]['type'] not in ['NUMBER', 'rightB']:
        return False
    #index=0はfor文回せないので処理しておく
    if tokens[0]['type'] == 'leftB':
        bracket_balance += 1
    for index in range(1, len(tokens)):
        if tokens[index]['type'] == 'NUMBER':
            #数字の前に右括弧は来ないし，数字が連続もNG
            if tokens[index - 1]['type'] in ['NUMBER', 'rightB']:
                return False
        elif tokens[index]['type'] == 'OPERATOR':
            #演算子の前に左括弧は来ないし，演算子が連続もNG
            if tokens[index - 1]['type'] in ['OPERATOR', 'leftB']:
                return False
        elif tokens[index]['type'] == 'leftB':
            #左括弧の前に数字は来ないし，右括弧と左括弧が連続はNG
            if tokens[index - 1]['type'] in ['NUMBER', 'rightB']:
                return False
            bracket_balance += 1
        elif tokens[index]['type'] == 'rightB':
            #右括弧の前に演算子は来ないし，右括弧と左括弧が連続はNG
            if tokens[index - 1]['type'] in ['OPERATOR', 'leftB']:
                return False
            bracket_balance -= 1
            #常に左括弧>=右括弧の大小関係がなりたっていないとNG
            if bracket_balance < 0:
                return False
      #最終的に，右括弧と左括弧の数が等しくないとNG
    if bracket_balance != 0:
        return False
    else:
        return True

#加減のみになった状態で演算
def evaluate_plus_minus(tokens, begin_index, end_index):
    result = 0
    index = begin_index + 1
    tokens.insert(begin_index, {'type': 'OPERATOR', 'operator': 'PLUS'})
    while index < end_index + 2:
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['operator'] == 'PLUS':
                result += tokens[index]['number']
            elif tokens[index - 1]['operator'] == 'MINUS':
                result -= tokens[index]['number']
        index += 2
    tokens.insert(begin_index, {'type': 'NUMBER', 'number': result})
    del tokens[begin_index+1:end_index+3]

#乗算記号の前後の数字を掛け合わせる
def evaluate_multiple(tokens, index):
    result = tokens[index-1]['number'] * tokens[index+1]['number']
    tokens.insert(index-1, {'type': 'NUMBER', 'number': result})
    del tokens[index:index+3]

#徐算記号前後の数字を掛け合わせる
def evaluate_div(tokens, index):
    if tokens[index+1]['number'] == 0:
        print('warning: division by 0')
        sys.exit(1)
    result = tokens[index-1]['number'] / tokens[index+1]['number']
    tokens.insert(index-1, {'type': 'NUMBER', 'number': result})
    del tokens[index:index+3]

#一番最初に計算すべき乗除の計算箇所を見つける
def find_first_multiple_div_to_eval(tokens, begin_index, end_index):
    for index in range(begin_index, end_index+1):
        if tokens[index]['type'] == 'OPERATOR':
            if tokens[index]['operator'] == 'MULTIPLE':
                return index, 'MULTIPLE'
            elif tokens[index]['operator'] == 'DIV':
                return index, 'DIV'
    return None, None

#一番最初に計算すべき括弧の位置を見つける
def find_first_bracket_to_eval(tokens):
    begin_index = None
    end_index = None
    for index in range(len(tokens)):
        if tokens[index]['type'] == 'leftB':
            begin_index = index
        elif tokens[index]['type'] == 'rightB':
            end_index = index
            return begin_index, end_index
    return begin_index, end_index

#括弧内を計算する
def evaluate_in_bracket(tokens, begin_index, end_index):
    #最初に括弧内の乗除を全て計算してしまう
    while True:
        index, operator = find_first_multiple_div_to_eval(tokens, begin_index, end_index)
        if index == None:
            break
        if operator == 'MULTIPLE':
            evaluate_multiple(tokens, index)
        elif operator == 'DIV':
            evaluate_div(tokens, index)
        end_index -= 2
    #乗除がない状態で加減の計算を行う
    evaluate_plus_minus(tokens, begin_index, end_index)

#トークン化された計算式の演算
def evaluate(tokens):
    #トークン化された計算式が答えの数字のみになるまでループ
    while len(tokens) > 1:
        #最初に計算すべき括弧を見つける
        bracket_begin_index, bracket_end_index = find_first_bracket_to_eval(tokens)
        #括弧がないとき
        if bracket_begin_index == None:
            evaluate_in_bracket(tokens, 0, len(tokens)-1)
        #括弧が見つかった時
        else:
            del tokens[bracket_begin_index]
            del tokens[bracket_end_index-1]
            evaluate_in_bracket(tokens, bracket_begin_index, bracket_end_index-2)
    #最後に残った数字を返す
    return tokens[0]['number']

def test(line):
    tokens = tokenize(line)
    if not check_syntax(tokens):
        print('Invalid syntax')
        sys.exit(1)
    actualAnswer = evaluate(tokens)
    expectedAnswer = eval(line)
    if abs(actualAnswer - expectedAnswer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expectedAnswer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expectedAnswer, actualAnswer))

# Add more tests to this function :)
def runTest():
    print("==== Test started! ====")
    test("1+2")
    test("1.0+2.1-3")
    test("1*2")
    test("1/2")
    test("1+(1+2)")
    test("4*(1+3)")
    test("(2+3)/3")
    test("1+(1+2)+(1+3)")
    test("(5)")
    test("((5))")
    test("1+((1+2)+3)")
    test("1+2*(1+2*(1+2))")
    test("2*(2*(1+2)+1)+1")
    test("((1+2)*4+(2+3))")
    #error_case: system shutdown
    #test("1/0")
    #test("1++")
    #test("1,")
    #test("1*/")
    #test("(1+(2)")
    #test("i+2")
    #test("1/(2-2)")
    #test("2(1+2)")
    #test("*1")
    #test("1(+2)")
    #test("1+(1*)")
    #test(")1(")
    print("==== Test finished! ====\n")

runTest()

print("電卓の使い方")
print("1. 入力形式は，1 + 2 + ( 2 * (1 + 2)) / 3 など一般的な方法で行い，半角のみ対応．")
print("   すなわち，演算子は +,-,*,/ を使用し，括弧を用いた演算も対応可能．")
print("   なお，2 (1 + 2) のような演算は認められないので，2 * (1 + 2)とする．")
print("2. 明示的な計算式を使用するように注意．")
print("   すなわち，1 * 2 / 3 など，計算順序が分からない入力をしてはいけない．")
print("   なお，このような入力に対しては，(1 * 2) / 3 のように左から逐次的に計算される．")
print("3. 電卓を終了したいときは，fを入力")
print("4. また，入力した計算式に入力・文法のミスがある場合や0割が起こった場合，プログラムは強制終了する．")
print()

while True:
    print('> ', end="")
    line = input()
    if line == 'f':
        break
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)

###########################################################################################
#==== Test started! ====
#PASS! (1+2 = 3.000000)
#PASS! (1.0+2.1-3 = 0.100000)
#PASS! (1*2 = 2.000000)
#PASS! (1/2 = 0.500000)
#PASS! (1+(1+2) = 4.000000)
#PASS! (4*(1+3) = 16.000000)
#PASS! ((2+3)/3 = 1.666667)
#PASS! (1+(1+2)+(1+3) = 8.000000)
#PASS! ((5) = 5.000000)
#PASS! (((5)) = 5.000000)
#PASS! (1+((1+2)+3) = 7.000000)
#PASS! (1+2*(1+2*(1+2)) = 15.000000)
#PASS! (2*(2*(1+2)+1)+1 = 15.000000)
#PASS! (((1+2)*4+(2+3)) = 17.000000)
#==== Test finished! ====
#
#電卓の使い方
#1. 入力形式は，1 + 2 + ( 2 * (1 + 2)) / 3 など一般的な方法で行い，半角のみ対応．
#   すなわち，演算子は +,-,*,/ を使用し，括弧を用いた演算も対応可能．
#   なお，2 (1 + 2) のような演算は認められないので，2 * (1 + 2)とする．
#2. 明示的な計算式を使用するように注意．
#   すなわち，1 * 2 / 3 など，計算順序が分からない入力をしてはいけない．
#   なお，このような入力に対しては，(1 * 2) / 3 のように左から逐次的に計算される．
#3. 電卓を終了したいときは，fを入力
#4. また，入力した計算式に入力・文法のミスがある場合や0割が起こった場合，プログラムは強制終了する．
#
#> 1+2+3
#answer = 6.000000
#
#> 4*5+(1*(2+3))
#answer = 25.000000
#
#> f
