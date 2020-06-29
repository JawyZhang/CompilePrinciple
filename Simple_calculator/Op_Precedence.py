'''
四则运算文法：
E→TE'
E'→+TE'| -TE' |ε
T→FT'
T'→*FT'| /FT' |ε
F→(E) | id |num

'''

import warnings

Vt_list = ['+', '-', '*', '/', '(', ')', '#']

'''
op_list为优先表
从上至下，从左至右顺序：+ - * / ( ) #
0表小于，1表等于，2表大于，3表出错
'''
op_list = [[2, 2, 0, 0, 0, 2, 2],
           [2, 2, 0, 0, 0, 2, 2],
           [2, 2, 2, 2, 0, 2, 2],
           [2, 2, 2, 0, 0, 2, 2],
           [0, 0, 0, 0, 0, 1, 3],
           [2, 2, 2, 2, 3, 2, 2],
           [0, 0, 0, 0, 0, 3, 1]
           ]
stack = ['#']  # 符号栈
k = 0  # 指向栈顶空区的指针
inStr = ""
inStack = []
a = ""


def a_getCh():  # 将下一字符读进a，a是输入串的缓冲，还未进入符号栈
    global a
    global inStack
    global k
    global stack
    while is_vt(a) == False:
        try:  # 拼接多位数，书本伪代码未讲
            temp1 = int(stack[-1])
            try:
                temp2 = int(a)
                temp = temp1 * 10 + temp2
                a = str(temp)
                stack.pop()
                k -= 1
            except:
                pass
        except:
            pass
        stack.append(a)
        print("移进", a, ",符号栈：", stack)
        a = inStack.pop(0)
        k += 1


def error():
    warnings.simplefilter('error', UserWarning)
    s = '语法分析过程出错，未能识别的符号下标:' + str(k) + ",符号：" + a
    warnings.warn(s)


def is_vt(item):
    if item in Vt_list:
        return True
    else:
        return False


def judge_op(op1, op2):
    if op1 == "+":
        id1 = 0
    elif op1 == "-":
        id1 = 1
    elif op1 == "*":
        id1 = 2
    elif op1 == "/":
        id1 = 3
    elif op1 == "(":
        id1 = 4
    elif op1 == ")":
        id1 = 5
    elif op1 == "#":
        id1 = 6
    else:
        print("无法识别：", op1, ",", op2)
        error()
    if op2 == "+":
        id2 = 0
    elif op2 == "-":
        id2 = 1
    elif op2 == "*":
        id2 = 2
    elif op2 == "/":
        id2 = 3
    elif op2 == "(":
        id2 = 4
    elif op2 == ")":
        id2 = 5
    elif op2 == "#":
        id2 = 6
    else:
        print("无法识别：", op1, ",", op2)
        error()
    return op_list[id1][id2]


def run():
    global stack
    global a
    global inStr
    global inStack
    global k
    inStr = input("请输入需要计算的数学式：")
    inStack = list(inStr)
    inStack.append('#')
    a = inStack.pop(0)  # 将a初始化为输入串首字符
    k = 0  # 书本上是1，但是那个是1开头
    stack = ['#']  # 初始化符号栈
    c = 0
    while True:
        c += 1
        print('第', c, '轮符号栈：', stack, "。", '第', c, '轮输入串：', inStack, "\n")
        a_getCh()
        print("结束移进")
        j = k
        while is_vt(stack[j]) == False:  # 使j一直指向最靠近栈顶的终结符，和书本不一样
            j -= 1
        while judge_op(stack[j], a) == 2:  # 0小于，1等于，2大于，3出错
            while True:
                Q = stack[j]
                if is_vt(stack[j - 1]):
                    j -= 1
                else:
                    j -= 2
                if judge_op(stack[j], Q) == 0:
                    break
            '''
            开始规约
            '''
            # print('开始规约：j=',j,',k=',k,'len=',len(stack))
            s = ""
            for i in range(j + 1, k + 1):
                s += stack.pop(j + 1)
            print("规约：" + s)
            try:
                N = eval(s)
            except:
                print("不可规约！")
                error()
            print('结束规约。规约为', s, '=', N)
            '''
            结束规约
            '''
            k = j + 1
            stack.append(str(N))
        if judge_op(stack[j], a) == 0 or judge_op(stack[j], a) == 1:
            print(stack[j], '优先级小于', a, ',移进', a)
            stack.append(a)
            k += 1
            if len(inStack) > 0:
                a = inStack.pop(0)
        else:
            error()
        if a == "#":
            break
    print(stack)
    print("结果为", stack[1])


run()
