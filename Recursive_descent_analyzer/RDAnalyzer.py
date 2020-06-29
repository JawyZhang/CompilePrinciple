'''
E→TE'
E'→+TE'| -TE' |ε
T→FT'
T'→*FT'| /FT' |ε
F→(E) | id |num


求得FIRST集和FOLLOW集
FIRST(E) = {(,id,num}
FIRST(E') = {+,-,空}
FIRST(T) = {(,i,num}
FIRST(T')= {*,/,空}
FIRST(F) = {(,id,num}

FOLLOW(E)={#,)}
FOLLOW(E')={#,)}
FOLLOW(T)={+,-,#,)}
FOLLOW(T')={+,-,#,)}
FOLLOW(F)={+,-,*,/,#}
'''
import warnings

ip = 0 # 输入串指示器，总是指向下一个未处理的符号
#s = "(num/id)-id" #测试串1，匹配成功
s = "(num+id)-id" #测试串1，匹配成功
sym = s[ip]
isTrue = True

follow = {
    'E': ['#', ')'],
    'E_': ['#', ')'],
    'T': ['+', '-', '#', ')'],
    'T_': ['+', '-', '#', ')'],
    'F': ['+', '-', '*', '/', '#', ')']
}


def advance():  # 使IP进一位
    global ip
    global sym
    if ip<len(s)-1:
        print(sym, end='')
        ip += 1
        sym = s[ip]


def error():
        warnings.simplefilter('error', UserWarning)
        s = '语法分析过程出错，未能识别的符号下标:' + str(ip)+",符号："+sym
        warnings.warn(s)


def E():  # E→TE'
    T()
    E_()


def E_():  # E'→+TE'| -TE' |ε
    if sym == "+":
        advance()
        T()
        E_()
    elif sym == "-":
        advance()
        T()
        E_()
    else :
        if ip < len(s) - 1:
            judge_follow("E_")


def T():  # T→FT'
    F()
    T_()


def T_():  # T'→*FT'| /FT' |ε
    if sym == "*":
        advance()
        F()
        T_()
    elif sym == "/":
        advance()
        F()
        T_()
    else:
        if ip < len(s) - 1:
            judge_follow("T_")


def F():  # F→(E) | id |num
    if sym == "(":
        advance()
        E()
        if sym == ")":
            advance()
        else:
            print("应该是)")
            error()
    elif sym == "i":
        advance()
        if sym == "d":
            advance()
        else:
            print("应该是d")
            error()
    elif sym == "n":
        advance()
        if sym == "u":
            advance()
            if sym == "m":
                advance()
            else:
                print("应该是m")
                error()
        else:
            error()
    else:
        error()


def judge_follow(node):  # 对候选匹配有空串的进行判断接收字符是否是当前结点的FOLLOW
    if sym not in follow[node]:
        print(sym+"不在FOLLOW("+node+")中")
        error()


def run():
    global isTrue
    E()
    if isTrue:
        print(sym, end='')
        print("\n匹配成功")
    else:
        print("\n匹配失败")


run()
