# Compiler for Jack programming language, for Nand to Tetris wk11
import sys
import re

# Jack code file -> XML file with identifiers
# Initializes and uses Tokenizer and Parser Objects
def main():
    # Intializes the parser object
    jfile = sys.argv[1]

    # makes tokenizer list to hold final tokens
    tokens = []

    t = Tokenizer(jfile)
    while t.hasMoreTokens() == True:
        TT = t.tokenType()
        if (main_helper(TT,t) in [None,"","\n"," "]):
            t.advance()
        else:
            tokens.append([(str(main_helper(TT,t))).strip(), TT.lower()])
            t.advance()
    if (main_helper(t.tokenType(),t) in [None,"","\n"," "]):
        print("ignore")
    else:
        tokens.append([(str(main_helper(t.tokenType(),t))).strip(), TT.lower()])

    #tfilename = ((jfile.split(".")[0]) +"TC.xml")
    #tfiles = open(tfilename, "w")
    #for x in range(0,len(tokens)):
    #    tfiles.write(str(tokens[x][0]) + " " + tokens[x][1] + "\n")
    #tfiles.close()

    c = CompEngine(sys.argv[1],tokens)
    v = VMWriter(sys.argv[1])
    c.compileClass()

    c.Close()

# Simplifies the main function, may not be needed
def main_helper(TT,t):
    if TT == "KEYWORD":
        return (t.keyWord())
    elif TT == "SYMBOL":
        return (t.symbol())
    elif TT == "IDENTIFIER":
        return (t.indentifier())
    elif TT == "INT_CONST":
        return (t.intVal())
    elif TT == "STRING_CONST":
        return (t.stringVal())
    else:
        return None

def filtfunc(x):
    if (x == " ") or (x == ""):
        return False
    else:
        return True


# Breaks down the input file and outputs a stream of individual tokens which
# are classified into lexical categories
class Tokenizer:
    # opens input .jack file and gets ready to tokenize it
    def __init__(self,filearg):
        file = open(filearg, "r")
        self.lines = file.readlines()
        file.close()
        self.lcounter = 0
        self.line = (self.lines)[self.lcounter]
        self.line = list(filter(filtfunc, re.split(r"(\;|\,|\.|[ ]|\[|\]|\(|\)|\n|\/|\t|\"|\-|\~)", self.line)))
        self.tcounter = 0
        while ((((self.line)[self.tcounter]) == "/") and (((self.line)[(self.tcounter)+1]) == "/")) or ((((self.line)[self.tcounter]) == "/") and (((self.line)[(self.tcounter)+1]) == "**")):
            self.lcounter += 1
            self.line = (self.lines)[self.lcounter]
            self.line = list(filter(filtfunc, re.split(r"(\;|\,|\.|[ ]|\[|\]|\(|\)|\n|\/|\t|\"|\-|\~)", self.line)))
            self.tcounter = 0
        self.tcounter = 0
        self.token = (self.line)[self.tcounter]

    # checks if there are more tokens in the input file
    def hasMoreTokens(self):
        if (self.lcounter == (len(self.lines)-1)):
            if (self.tcounter == (len(self.line)-1)):
                return False
            else:
                return True
        else:
            return True

    # gets next token from input and makes it current token
    def advance(self):
        if ((self.token == "\n") or
            ((self.line[(self.tcounter)+1] == "/") and (self.line[(self.tcounter)+2] == "/")) or
            ((self.line[(self.tcounter)] == "/") and (self.line[(self.tcounter)+1] == "/")) or
            ((self.token == "/") and (self.line[(self.tcounter)+1] == "**")) or
            (re.match(r"\/\w+",self.token)) or
            ((self.token == "*") and (self.line[(self.tcounter)+1] == "/")) or
            (self.line[0] == "*")):
            self.lcounter += 1
            self.line = (self.lines)[self.lcounter]
            self.line = list(filter(filtfunc, re.split(r"(\;|\,|\.|[ ]|\[|\]|\(|\)|\n|\/|\t|\"|\-|\~)",self.line)))
            self.tcounter = 0
            while (((((self.line)[self.tcounter]) == "/") and (((self.line)[(self.tcounter)+1]) == "/")) or
                   ((((self.line)[self.tcounter]) == "/") and (((self.line)[(self.tcounter)+1]) == "**")) or
                   (self.line[0] == "*")):
                self.lcounter += 1
                self.line = (self.lines)[self.lcounter]
                self.line = list(filter(filtfunc, re.split(r"(\;|\,|\.|[ ]|\[|\]|\(|\)|\n|\/|\t|\"|\-|\~)", self.line)))
                self.tcounter = 0
            self.tcounter = 0
            self.token = (self.line)[self.tcounter]
            return
        if (self.token == '"'):
            self.tcounter += 1
            self.token = (self.line)[self.tcounter]
            tokenholder = ""
            while (self.token != '"'):
                tokenholder = tokenholder + (self.token + " ")
                self.tcounter += 1
                self.token = (self.line)[self.tcounter]
            self.token = tokenholder
            return
        if (self.tcounter == (len(self.line)-1)):
            self.lcounter += 1
            self.line = (self.lines)[self.lcounter]
            self.line = list(filter(filtfunc, re.split(r"(\;|\,|\.|[ ]|\[|\]|\(|\)|\n|\/|\t|\"|\-|\~)",self.line)))
            self.tcounter = 0
            while (((((self.line)[self.tcounter]) == "/") and (((self.line)[(self.tcounter)+1]) == "/")) or
                   ((((self.line)[self.tcounter]) == "/") and (((self.line)[(self.tcounter)+1]) == "**")) or
                   (self.line[0] == "*")):
                self.lcounter += 1
                self.line = (self.lines)[self.lcounter]
                self.line = list(filter(filtfunc, re.split(r"(\;|\,|\.|[ ]|\[|\]|\(|\)|\n|\/|\t|\"|\-|\~)", self.line)))
                self.tcounter = 0
            self.tcounter = 0
            self.token = (self.line)[self.tcounter]
            return
        else:
            self.tcounter += 1
            self.token = (self.line)[self.tcounter]
            return

    # Returns the type of the current token as a constant
    def tokenType(self):
        lexEle = {"class":"KEYWORD","constructor":"KEYWORD","function":"KEYWORD",
                  "method":"KEYWORD","field":"KEYWORD","static":"KEYWORD","var":"KEYWORD",
                  "int":"KEYWORD","char":"KEYWORD","boolean":"KEYWORD","void":"KEYWORD",
                  "true":"KEYWORD","false":"KEYWORD","null":"KEYWORD","this":"KEYWORD",
                  "let":"KEYWORD","do":"KEYWORD","if":"KEYWORD","else":"KEYWORD"
                  ,"while":"KEYWORD","return":"KEYWORD","{":"SYMBOL","}":"SYMBOL",
                  "(":"SYMBOL",")":"SYMBOL","[":"SYMBOL","]":"SYMBOL",".":"SYMBOL",
                  ",":"SYMBOL",";":"SYMBOL","+":"SYMBOL","-":"SYMBOL","*":"SYMBOL",
                  "/":"SYMBOL","&":"SYMBOL","|":"SYMBOL","<":"SYMBOL",">":"SYMBOL",
                  "=":"SYMBOL","~":"SYMBOL",}
        try:
            return lexEle[(str(self.token)).strip()]
        except:
            if (self.token == "//") or (self.token == "/**") or (self.token == "") or (self.token == "\n") or (re.match(r"\/\w*",self.token)):
                return None
            elif (re.match('\d+',self.token)):
                return "INT_CONST"
            elif ((re.match('^([A-Z]|[a-z])\w*',self.token)) and (not(bool(re.search('\s+',self.token))))):
                return "IDENTIFIER"
            else:
                return "STRING_CONST"

    # Returns the keyword associated with the current token
    def keyWord(self):
       # kWords = {"class":"CLASS","constructor":"CONSTRUCTOR","function":"FUNCTION",
       #           "method":"METHOD","field":"FIELD","static":"STATIC","var":"VAR",
       #           "int":"INT","char":"CHAR","boolean":"BOOLEAN","void":"VOID",
       #           "true":"TRUE","false":"FALSE","null":"NULL","this":"THIS",
       #           "let":"LET","do":"DO","if":"IF","else":"ELSE"
       #           ,"while":"WHILE","return":"RETURN"}
        return self.token

    # Returns the character which is the current token
    def symbol(self):
        symd = {"<":"&lt;",">":"&gt;","&":"&amp;"}
        if (self.token in ["<",">","&"]):
            return symd[self.token]
        else:
            return self.token

    # Returns the indentifier which is the current token
    def indentifier(self):
        return self.token

    # Returns the int value of the current token
    def intVal(self):
        return int(self.token)

    # Returns the string value of the current token (without enclosing double
    # quotes)
    def stringVal(self):
        if (re.match(r"\w+",self.token)):
            return (self.token)
        else:
            return None




# Takes the list of individual tokens and compiles a XML output file that
# creates a token tree with indentifiers
class CompEngine:
    # Creates new comp engine with given input and output files
    def __init__(self,filename,tokens):
        nfilename = ((filename.split(".")[0]) +".xml")
        print(nfilename)
        self.newfile = open(nfilename, "w")
        self.count = 0
        self.tokens = tokens

    # Compiles a complete class
    def compileClass(self):
        self.newfile.write("<class>\n")
        self.classname = (self.tokens[(self.count)+1][0])
        while (self.tokens[(self.count)][0] != "{"):
            self.newfile.write("<"+(self.tokens[self.count][1])+"> " + (self.tokens[self.count][0]) + " </"+(self.tokens[self.count][1])+">\n")
            self.count += 1
        self.newfile.write("<"+(self.tokens[self.count][1])+"> " + (self.tokens[self.count][0]) + " </"+(self.tokens[self.count][1])+">\n")
        self.count += 1
        self.ST = SymbolTable()
        while ((self.count) < (len(self.tokens)-1)):
            if (self.tokens[self.count][0] in ["static","field"]):
                self.compileClassVarDec()
            if (self.tokens[self.count][0] in ["function","method","constructor"]):
                self.compileSubroutineDec()
            if (self.tokens[self.count][0] == "{"):
                self.compileSubroutineBody()
        self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
        self.count += 1
        self.newfile.write("</class>")

    # Compiles a stateic variable declaration or field declaration
    def compileClassVarDec(self):
        self.newfile.write("<classVarDec>\n")
        while (self.tokens[(self.count)][0] != ";"):
            if ((self.tokens[(self.count)][1] == "identifier") and (self.tokens[(self.count)-2][0] in ["static","field"])):
                ttype = self.tokens[(self.count)-1][0]
                kind = self.tokens[(self.count)-2][0]
                self.ST.define((self.tokens[self.count][0]), ttype, kind)
                self.newfile.write(self.tokens[self.count][0] + " " + kind + " " + (self.ST.IndexOf((self.tokens[self.count][0]))) + " defined\n")
            elif ((self.tokens[(self.count)][1] == "identifier") and (self.tokens[(self.count)-1][0] == ",")):
                self.ST.define((self.tokens[self.count][0]), ttype, kind)
                self.newfile.write(self.tokens[self.count][0] + " " + kind + " " + (self.ST.IndexOf((self.tokens[self.count][0]))) + " defined\n")
            self.count += 1
        self.count += 1
        self.newfile.write("</classVarDec>\n")
        return

    # Compiles a complete method, funciton, or constructor
    def compileSubroutineDec(self):
        self.newfile.write("<subroutineDec>\n")
        self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
        self.count += 1
        self.ST.startSubroutine()
        if ((self.tokens[(self.count)-1][0]) == "method"):
            self.ST.define("this",self.classname,"argument")
            self.newfile.write("this " + "argument" + " " + (self.ST.IndexOf("this")) + " defined\n")
        while (self.tokens[self.count][1] != "symbol"):
            self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
            self.count += 1
        if (self.tokens[self.count][0] == "("):
            self.compileParameterList()
        if (self.tokens[self.count][0] == "{"):
            self.compileSubroutineBody()
        self.newfile.write("</subroutineDec>\n")
        return

    # Compiles a (maybe empty) paramter list (ignores enclosing ())
    def compileParameterList(self):
        self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
        self.count += 1
        self.newfile.write("<parameterList>\n")
        while (self.tokens[self.count][0] != ")"):
            if ((self.tokens[(self.count)][1] == "identifier") and (self.tokens[(self.count)-2][0] in ["(",","])):
                ttype = self.tokens[(self.count)-1][0]
                kind = "argument"
                self.ST.define((self.tokens[self.count][0]), ttype, kind)
                self.newfile.write(self.tokens[self.count][0] + " " + kind + " " + (self.ST.IndexOf((self.tokens[self.count][0]))) + " defined\n")
            self.count += 1
        self.newfile.write("</parameterList>\n")
        self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
        self.count += 1
        return

    # Compiles a subroutine's body
    def compileSubroutineBody(self):
        self.newfile.write("<subroutineBody>\n")
        self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
        self.count += 1
        while (self.tokens[(self.count)][0] != "}"):
            if (self.tokens[self.count][0] == "var"):
                self.compileVarDec()
            if (self.tokens[self.count][0] in ["let","if","while","do","return"]):
                self.compileStatements()
            if (self.tokens[(self.count)][0] in ["method","constructor","function"]):
                    break
        self.newfile.write("</subroutineBody>\n")
        return

    # Compiles a var declaration
    def compileVarDec(self):
        self.newfile.write("<varDec>\n")
        src = 0
        while ((self.tokens[(self.count)-1][0] != ";") or (self.tokens[self.count][0] == "var")) and (src < 1):
            if ((self.tokens[(self.count)][1] == "identifier") and (self.tokens[(self.count)-2][0] == "var")):
                ttype = self.tokens[(self.count)-1][0]
                kind = self.tokens[(self.count)-2][0]
                self.ST.define((self.tokens[self.count][0]), ttype, kind)
                self.newfile.write(self.tokens[self.count][0] + " " + kind + " " + (self.ST.IndexOf((self.tokens[self.count][0]))) + " defined\n")
            elif ((self.tokens[(self.count)][1] == "identifier") and (self.tokens[(self.count)-1][0] == ",")):
                self.ST.define((self.tokens[self.count][0]), ttype, kind)
                self.newfile.write(self.tokens[self.count][0] + " " + kind + " " + (self.ST.IndexOf((self.tokens[self.count][0]))) + " defined\n")
            self.count += 1
            if ((self.tokens[(self.count)-1][0] == ";") and (self.tokens[self.count][0] == "var")):
                  src += 1
        self.newfile.write("</varDec>\n")
        return

    # Compiles a sequence of statements (ignores enclosing {})
    def compileStatements(self):
        self.newfile.write("<statements>\n")
        while (self.tokens[self.count][0] != "}"):
            if (self.tokens[self.count][0] == "let"):
                self.compileLet()
            if (self.tokens[self.count][0] == "if"):
                self.compileIf()
            elif (self.tokens[self.count][0] == "while"):
                self.compileWhile()
            elif (self.tokens[self.count][0] == "do"):
                self.compileDo()
            elif (self.tokens[self.count][0] == "return"):
                self.compileReturn()
        self.newfile.write("</statements>\n")
        self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
        self.count += 1
        return

    # Compiles a let statement
    def compileLet(self):
        self.newfile.write("<letStatement>\n")
        src = 0
        while ((self.tokens[(self.count)-1][0] != ";") or (self.tokens[(self.count)][0] == "let")) and (src < 1):
            if (self.tokens[(self.count)][1] == "identifier"):
                self.newfile.write((self.tokens[self.count][0]) + " " + (self.ST.KindOf((self.tokens[self.count][0]))) + " " + (self.ST.IndexOf((self.tokens[self.count][0]))) + " used\n")
                self.count += 1
            if (self.tokens[self.count][0] in ["["]) :
                self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
                self.count += 1
                self.compileExpression()
            if (self.tokens[self.count][0] in ["="]) :
                self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
                self.count += 1
                self.compileExpression()
                src += 1
            else:
                self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
                self.count += 1
        self.newfile.write("</letStatement>\n")
        return

    # Compiles an if statement (matbe with trailing else)
    def compileIf(self):
        self.newfile.write("<ifStatement>\n")
        src = 0
        if (self.tokens[self.count][0] == "if"):
            while ((self.tokens[(self.count)-1][0] != "}") or (self.tokens[self.count][0] == "if")) and (src < 1):
                if (self.tokens[self.count][0] != ("(" and "{")):
                    self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
                    self.count += 1
                if (self.tokens[self.count][0] == "("):
                    self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
                    self.count += 1
                    self.compileExpression()
                if (self.tokens[self.count][0] == "{"):
                    self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
                    self.count += 1
                    self.compileStatements()
                    src += 1
        if (self.tokens[self.count][0] == "else"):
            while (self.tokens[(self.count)-1][0] != "}") or (self.tokens[self.count][0] == "else"):
                self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
                self.count += 1
                if (self.tokens[self.count][0] == "{"):
                     self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
                     self.count += 1
                     self.compileStatements()
        self.newfile.write("</ifStatement>\n")
        return

    # Compiles a while statement
    def compileWhile(self):
        self.newfile.write("<whileStatement>\n")
        src = 0
        while ((self.tokens[(self.count)-1][0] != "}") or (self.tokens[(self.count)][0] == "while")) and (src < 1):
             if (not(self.tokens[self.count][0] in ["(","{"])):
                self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
                self.count += 1
             elif (self.tokens[self.count][0] == "("):
                self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
                self.count += 1
                self.compileExpression()
             if (self.tokens[self.count][0] == "{"):
                self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
                self.count += 1
                self.compileStatements()
                src += 1
        self.newfile.write("</whileStatement>\n")
        return

    # Compiles a do statement
    def compileDo(self):
        self.newfile.write("<doStatement>\n")
        src = 0
        while ((self.tokens[(self.count)-1][0] != ";") or (self.tokens[(self.count)][0] == "do")):
            if (self.tokens[self.count][0] != "("):
                if ((self.tokens[self.count][1] == "identifier") and (self.tokens[(self.count)-1][0] != ".")):
                    self.newfile.write(self.tokens[self.count][0] + " " + (self.ST.KindOf((self.tokens[self.count][0]))) + " " + (self.ST.IndexOf((self.tokens[self.count][0]))) + " used\n")
                    self.count += 1
                elif ((self.tokens[self.count][1] == "identifier") and (self.tokens[(self.count)-1][0] == ".")):
                    self.newfile.write(self.tokens[self.count][0] + " " + "subroutine" + " used\n")
                    self.count += 1
                else:
                    self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
                    self.count += 1
            else:
                self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
                self.count += 1
                self.compileExpressionList()
                src += 1
            if ((self.tokens[(self.count)-1][0] == ";") and (self.tokens[(self.count)][0] == "do") and (src == 1)):
                break
        self.newfile.write("</doStatement>\n")
        return

    # Compiles a return statement
    def compileReturn(self):
        self.newfile.write("<returnStatement>\n")
        src = 0
        while (self.tokens[(self.count)-1][0] != ";") or (self.tokens[(self.count)][0] == "return"):
            if ((self.tokens[self.count][1] == "identifier") or ((self.tokens[self.count][1] == "keyword") and (self.tokens[self.count][0] != "return"))):
                self.compileExpression()
            else:
                self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
                self.count += 1
        self.newfile.write("</returnStatement>\n")
        return

    # Compiles an expression
    def compileExpression(self):
        self.newfile.write("<expression>\n")
        while (not(self.tokens[self.count][0] in [";",")","]",","])):
            if (self.tokens[self.count][1] != "symbol"):
                self.compileTerm()
            if (self.tokens[self.count][0] == "*"):
                self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
                self.count += 1
                self.compileTerm()
            if (self.tokens[self.count][0] == "(") or ((self.tokens[self.count][0] in ["-","~"]) and (self.tokens[(self.count)-1][0] == "(")):
                self.compileTerm()
            if (self.tokens[self.count][0] in [";",")","]",","]):
                break
            else:
                self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
                self.count += 1
        self.newfile.write("</expression>\n")
        self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
        self.count += 1
        return

    # Compiles a term (will likelu need to lookahead 1 token to distinguish
    # between possiblilities
    def compileTerm(self):
        self.newfile.write("<term>\n")
        while (not(self.tokens[(self.count)-1][0] in [";",")","]"])):
            if (self.tokens[(self.count)][0] in [")","]",";",","]):
                break
            # id then [
            if (self.tokens[(self.count)+1][0] == "[") and (self.tokens[(self.count)][1] == "identifier"):
                self.newfile.write(self.tokens[self.count][0] + " " + (self.ST.KindOf((self.tokens[self.count][0]))) + " " + (self.ST.IndexOf((self.tokens[self.count][0]))) + " used\n")
                self.count += 1
                self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
                self.count += 1
                self.compileExpression()
                break
            # id then (
            elif (self.tokens[(self.count)+1][0] == "(") and (self.tokens[(self.count)][1] == "identifier"):
                self.newfile.write(self.tokens[self.count][0] + " " + (self.ST.KindOf((self.tokens[self.count][0]))) + " " + (self.ST.IndexOf((self.tokens[self.count][0]))) + " used\n")
                self.count += 1
                self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
                self.count += 1
                self.compileExpressionList()
                break
            # id then symbol
            elif (self.tokens[(self.count)+1][0] in ["&lt;","&gt;","&amp;","+","-","*","/","|","=","~"]) and (self.tokens[(self.count)][1] == "identifier"):
                self.newfile.write(self.tokens[self.count][0] + " " + (self.ST.KindOf((self.tokens[self.count][0]))) + " " + (self.ST.IndexOf((self.tokens[self.count][0]))) + " used\n")
                self.count += 1
                break
            # ( then - or ~ | ( then id
            elif ((self.tokens[self.count][0] == "(") and ((self.tokens[(self.count)+1][0] in ["-","~"]))) or ((self.tokens[self.count][0] == "(") and (self.tokens[(self.count)+1][1] == "identifier")):
                self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
                self.count += 1
                self.compileExpression()
                break
            # ( then (
            elif (self.tokens[self.count][0] == "(") and (self.tokens[(self.count)+1][0] == "("):
                self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
                self.count += 1
                self.compileExpression()
                break
            # just - or ~
            elif (self.tokens[self.count][0] in ["~","-"]):
                self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
                self.count += 1
                self.compileTerm()
                break
            # id then .
            elif (self.tokens[(self.count)+1][0] == ".") and (self.tokens[(self.count)][1] == "identifier"):
                self.newfile.write(self.tokens[self.count][0] + " " + (self.ST.KindOf((self.tokens[self.count][0]))) + " " + (self.ST.IndexOf((self.tokens[self.count][0]))) + " used\n")
                self.count += 1
                self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
                self.count += 1
            # just id
            elif (self.tokens[(self.count)][1] == "identifier"):
                self.newfile.write(self.tokens[self.count][0] + " " + (self.ST.KindOf((self.tokens[self.count][0]))) + " " + (self.ST.IndexOf((self.tokens[self.count][0]))) + " used\n")
                self.count += 1
            else:
                self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
                self.count += 1
        self.newfile.write("</term>\n")
        return

    # Compiles a (maybe empty) comma-separated list of expressions
    def compileExpressionList(self):
        self.newfile.write("<expressionList>\n")
        while (self.tokens[(self.count)-1][0] != ")"):
            if (self.tokens[(self.count)][1] != "symbol") or (self.tokens[(self.count)][0] == "("):
                self.compileExpression()
            else:
                self.newfile.write("<"+self.tokens[self.count][1]+"> " + self.tokens[self.count][0] + " </"+self.tokens[self.count][1]+">\n")
                self.count += 1
        self.newfile.write("</expressionList>\n")
        return

    # closes the output file
    def Close(self):
        self.newfile.close()

# creates, stores, and updates the symbol tables needed to write the VM code
class SymbolTable:
    # initializes the class level symbol tables
    def __init__(self):
        self.stdic = {}
        return

    # initializes the subroutine level symbol table
    def startSubroutine(self):
        self.substdic = {}
        return

    # creates a symbol table entry for the given variable
    def define(self, name, ttype, kind):
        if (kind in ["static","field"]):
            self.stdic[name] = (ttype + "," + kind + "," + str(self.VarCount(kind) + 1))
        else:
            self.substdic[name] = (ttype + "," + kind + "," + str((self.VarCount(kind) + 1)))
        return

    # counts how many of the current var kind already exist within the relevant
    # symbol table
    def VarCount(self, kind):
        count = -1
        if (kind in ["static","field"]):
            for x in self.stdic:
                if ((((self.stdic[x]).split(","))[1]) == kind):
                    count += 1
        else:
            for x in self.substdic:
                if ((((self.substdic[x]).split(","))[1]) == kind):
                    count += 1
        return count

    # returns the kind of the requested var
    def KindOf(self, name):
        try:
            kkind = ((((self.substdic)[name]).split(","))[1])
            if ((name in self.substdic) and (kkind != None)):
                return kkind
            elif (name in self.stdic):
                return ((((self.stdic)[name]).split(","))[1])
        except:
            if (name in self.stdic):
                return ((((self.stdic)[name]).split(","))[1])
            else:
                return "subroutine"

    # returns the type of the requested var
    def TypeOf(self, name):
        try:
            ttype = ((((self.substdic)[name]).split(","))[0])
            if ((name in self.substdic) and (ttype != None)):
                return ttype
            elif (name in self.stdic):
                return ((((self.stdic)[name]).split(","))[0])
        except:
            if (name in self.stdic):
                return ((((self.stdic)[name]).split(","))[0])
            else:
                return "NONE"

    # returns the index of the requested var
    def IndexOf(self, name):
        try:
            iindex = ((((self.substdic)[name]).split(","))[2])
            if ((name in self.substdic) and (iindex != None)):
                return iindex
            elif (name in self.stdic):
                return ((((self.stdic)[name]).split(","))[2])
        except:
            if (name in self.stdic):
                return ((((self.stdic)[name]).split(","))[2])
            else:
                return "NONE"


class VMWriter:
    # creates a new output .vm file and prepares it for writing
    def __init__(self, filename):
        nfilename = ((filename.split(".")[0]) +".vm")
        print(nfilename)
        self.newfile = open(nfilename, "w")

    # Writes a VM push command to the output file with the given segment and
    # index
    def writePush(self, segment, index):
        self.newfile.write("push " + segment + " " + index + "\n")
        return

    # Same as the push but for a pop command
    def writePop(self, segment, index):
        self.newfile.write("pop " + segment + " " + index + "\n")
        return

    # Writes the given command as a VM command (ADD, SUB, NEG, EQ, GT, LT, AND,
    # OR, NOT) to the output file
    def writeArithmetic(self, command):
        self.newfile.write(command.lower() + "\n")
        return

    # Writes a VM label command with the given label
    def writeLabel(self, label):
        self.newfile.write("label " + label + "\n")
        return

    # Writes a VM goto command with the given label
    def writeGoto(self, label):
        self.newfile.write("goto " + label + "\n")
        return

    # writes a VM if-goto command with the given label
    def writeIf(self, label):
        self.newfile.write("if-goto " + label + "\n")
        return

    # writes a VM call command with the given name and arg number
    def writeCall(self, name, nArgs):
        self.newfile.write("call " + name + " " + nArgs + "\n")
        return

    # writes a VM function command with the given name and local number
    def writeFunction(self, name, nLocals):
        self.newfile.write("function " + name + " " + nLocals + "\n")
        return

    # writes a VM return command
    def writeReturn(self):
        self.newfile.write("return\n")
        return

    # closes the output file
    def close(self):
        self.newfile.close()


# Starts the program
if __name__== "__main__":
    main()
