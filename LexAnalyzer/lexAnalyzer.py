import warnings
class Analyzer:

    def __init__(self,txt):
        self.ch = ''
        self.strToken = ''
        self.txt = ''
        self.idx = 0
        self.txt = txt;
        self.keyWordList = ['begin', 'end' ,'if' ,'then', 'while', 'do', 'const', 'var','call','procedure'];
        self.operatorList = [ '+', '-', '*', '/', ]
        self.delimiterList = ['(',')' ,',' ,'.',';']
        self.identList = []
        self.constList = []
        self.txtLen = len(self.txt)

    def getChar(self):
        self.ch = self.txt[self.idx]
        self.idx += 1

    def is_blank(self):  # 回车、空格、制表
        if self.ch == "\n" or self.ch == "\t" or self.ch == " ":
            return True
        else:
            return False

    def is_delimiter(self):  # 界符
        if self.ch in self.delimiterList:
            return True
        else:
            return False

    def is_operator(self):  # “单元”操作符，多元的通过状态转移判断
        if self.ch in self.operatorList:
            return True
        else:
            return False

    def is_letter(self):
        if self.ch >= 'a' and self.ch <= 'z':
            return True
        else:
            return False

    def concat(self):
        self.strToken += self.ch


    def is_digit(self):
        try:
            int(self.ch)
            return True
        except:
            return False

    def reserve(self): #strToken是保留字则返回编码，否则返回0；
        if self.strToken in self.keyWordList:
            return self.keyWordList.index(self.strToken)+1
        else:
            return 0

    def getBC(self):
        while(self.is_blank()):
            self.getChar()

    def retract(self):
        self.ch = ''
        self.idx -= 1
        return self.idx

    def insertId(self,strToken):
        self.identList.append(self.strToken)
        return self.identList.index(self.strToken)

    def insertConst(self):
        self.constList.append(self.strToken)
        return self.constList.index(self.strToken)

    def processError(self):
        warnings.simplefilter('error',UserWarning)
        s = '词法分析过程出错，未能识别的符号下标:'+ str(self.idx)
        warnings.warn(s)


    def scanner(self):
        code = -1
        value = -1
        self.strToken = ''
        self.getChar()
        self.getBC()
        if self.ch == 'o':
            self.concat()
            self.getChar()
            if self.ch == 'd':
                self.concat()
                self.getChar()
                if self.ch == 'd':
                    self.concat()
                    self.getChar()
                    return self.strToken,'-'
                else:
                    while self.is_letter() or self.is_digit():
                        self.concat()
                        self.getChar()
                    self.retract()
                    code = self.reserve()
                    if code == 0:
                        value = self.insertId(self.strToken)
                        return self.strToken, value
                    else:
                        return code, '-'
            else:
                while self.is_letter() or self.is_digit():
                    self.concat()
                    self.getChar()
                self.retract()
                code = self.reserve()
                if code == 0:
                    value = self.insertId(self.strToken)
                    return self.strToken, value
                else:
                    return code, '-'

        elif self.is_letter():
            while self.is_letter() or self.is_digit():
                self.concat()
                self.getChar()
            self.retract()
            code = self.reserve()
            if code == 0:
                value = self.insertId(self.strToken)
                return self.strToken,value
            else :
                return self.strToken,'-'

        elif self.is_digit():
            while self.is_digit():
                self.concat()
                self.getChar()
            self.retract()
            value = self.insertConst()
            return self.strToken,

        elif self.ch == ':':
            self.concat()
            self.getChar()
            if self.ch =='=':
                self.concat()
                return self.strToken,'-'
            else:
                self.retract()

                self.processError()

        elif self.ch == '<':
            self.concat()
            self.getChar()
            if self.ch == '>' or self.ch== '=':
                self.concat()
                return self.strToken,'-'
            else:
                self.retract()
                return self.strToken,'-'

        elif self.ch == '>':
            self.concat()
            self.getChar()
            if self.ch == '=':
                self.concat()
                return self.strToken,'-'
            else:
                self.retract()
                return self.strToken,'-'

        elif self.is_delimiter() or self.is_operator():
            return self.ch,'-'
        else:
            self.processError()

    def run(self):
        while(self.idx<self.txtLen):
            code,value = self.scanner()
            print('<{},{}>'.format(str(code),str(value)))

'''
调用词法分析器
'''
import pathlib
f = pathlib.Path('src.txt')
with f.open('r') as src:
    txt = src.read()
    la = Analyzer(txt)
    la.run()