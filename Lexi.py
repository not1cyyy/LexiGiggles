import re
import os



CONST = [
            'INTEGER_CONSTANT',
            'STRING_CONSTANT', 'FLOAT_CONSTANT', 'CHAR_CONSTANT', 'BoolConstT'
        ]

TOKENS = [
    'KEYWORD', 'IDENTIFIER', 'INTEGER_CONSTANT',
    'OPERATOR', 'SEPARATOR', 'STRING_CONSTANT', 'FLOAT_CONSTANT', 'CHAR_CONSTANT', 'DataType' , 'BoolConstT'
]

input_code = """#include <iostream>

using namespace std;

void main()
{
    if (a < b)
    {
        return i++;
    }
    else
    {
        i = 0;
    }
    switch (a)
    {
    case 'A':
        cin >> input;
        cout << "hello world";
    default:
        break;
    }
}"""

print("INPUT CODE:\n", input_code)


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


Integers = re.findall('^[0-9]+$|[0-9]+', input_code)
Floats = re.findall(r'[0-9]+\.[0-9]+', input_code)
Chars = re.findall(r'\'[^\'\\\.]\'', input_code)

TOKENS_DEF = {
    '=': 'ASSIGN',
    '&': 'ADDRESS',
    '<': 'LT',
    '>': 'GT',
    '++': 'SELF_PLUS',
    '--': 'SELF_MINUS',
    '+': 'PLUS',
    '-': 'MINUS',
    '*': 'MUL',
    '/': 'DIV',
    '>=': 'GET',
    '<=': 'LET',
    '(': 'L_PAREN',
    ')': 'R_PAREN',
    '{': 'L_BRACE',
    '}': 'R_BRACE',
    '[': 'LS_Bracket',
    ']': 'RS_Bracket',
    ',': 'COMMA',
    '"': 'DOUBLE_QUOTE',
    '\'': 'SINGLE_QUOTE',
    ';': 'SEMICOLON',
    '#': 'SHARP',
    '&&': 'AND',
    '!': 'NOT',
    '||': 'OR',
    '<<': 'L_SHIFT',
    '>>': 'R_SHIFT',
    '==':'EQUALITY',
    ':':'COLON'
    
}

Keyword = ["if", "else", "while", "for", "cout", "cin", "return", "switch", "case", "break", "function",
           "using", "namespace", "include", "endl","default"]
Bracket = ['(', ')', '{', '}', '[', ']']
DataType = ['int', 'float', 'char', 'string', 'bool','void']
Punctuator = [',', ';', ':', ',']
ArithOP = ['-', '+', '*', '/', '%']
LogOP = ['||', '&&']
NegOP = ['!']
AssOP = ['=']
CompOP = ['<', '>']
RelOP = ['<=', '>=', '!=', '==', "<<", ">>"]
Incr = ['++', '--']
BoolConst = ['True','False']


class Node:

    # Function to initialise the node object
    def __init__(self, value, line_numbers, type):
        self.data = {
            "value": value,
            "LINE_NUMBERS": line_numbers,
            "TYPE": type
        }  # Assign data
        self.next = None  # Initialize next as null

# Node of a doubly linked list
class Symbol_table_Node:
    def __init__(self, name, line_numbers, type,scope):
        self.data = {
            "Name": name,
            "LINE_NUMBERS": line_numbers,
            "TYPE": type,
            "Scope": scope
        }  # Assign data
        self.next = None  # Initialize next as null
        self.prev = None
class SymbolTable:
    def __init__(self):
        self.head = None
    def push(self, name, line_numbers, type,scope):
            new_node = Symbol_table_Node(name, line_numbers, type,scope)


            new_node.next = self.head
            new_node.prev = None


            if self.head is not None:
                self.head.prev = new_node


            self.head = new_node

    def printList(self):
        node = self.head
        while (node != None):

            print(node.data)
            last = node
            node = node.next

    def FindData(self, name):
        flag = False
        node = self.head

        while (node != None):

            if (node.data['Name'] == name):
                return node.data
            last = node
            node = node.next
        if (flag == False):
            return False


class Tokens:

    # Function to initialize head
    def __init__(self):
        self.head = None

    # This function is defined in Linked List class
    # Appends a new node at the end. This method is
    # defined inside LinkedList class shown above */
    def append(self, value, line_numbers, type):

        # 1. Create a new node
        # 2. Put in the data
        # 3. Set next as None
        new_node = Node(value, line_numbers, type)

        # 4. If the Linked List is empty, then make the
        # new node as head
        if self.head is None:
            self.head = new_node
            return

        # 5. Else traverse till the last node
        last = self.head
        while (last.next):
            last = last.next

        # 6. Change the next of last node
        last.next = new_node

    # Utility function to print the linked list
    def printList(self):
        temp = self.head
        while (temp):
            print(temp.data),
            temp = temp.next

class Token(object):

    def __init__(self, pos, value, linenumber):
        self.type = TOKENS_DEF[value] if (
                pos == 3 or pos == 4
        ) else TOKENS[pos]
        self.value = value
        self.line_number = linenumber

class Lexer(object):

    def __init__(self):
        self.tokens = []
        self.count = 1
        self.temp = ''
        self.sym = SymbolTable()

    def is_blank(self, index):
        return (
                input_code[index] == ' '
        )

    def is_Escape(self, index):
        return (

                input_code[index] == '\t' or
                input_code[index] == '\n' or
                input_code[index] == '\r'
        )

    def line_break(self, index):
        return (
                input_code[index] == '\n' or
                input_code[index] == '\t' or
                input_code[index] == '\b' or
                input_code[index] == ' '

        )

    def skip_blank(self, index, stringflag):
        while index < len(input_code) and self.is_blank(index):
            index += 1
        return index

    def print_log(self, style, value):
        print(style, value)

    def checkforiden(self):
        if (self.temp != ''):

            i = re.findall('[a-zA-Z_][a-zA-Z_0-9]*', self.temp)

            if (self.temp in i):

                self.tokens.append(Token(1, self.temp, self.count))


                self.sym.push(self.temp, self.count, "NOT DEFINED", "NOT DEFINED")
                self.temp = ''


            else:
                print(
                    f"...{bcolors.BOLD}{bcolors.FAIL} {bcolors.FAIL}ERROR: UNABLE TO RUN FILE {bcolors.OKBLUE} {os.path.abspath('sample.cpp')} {bcolors.FAIL} \n INVALID IDENTIFIER IN LINE NUMBER: {self.count} {bcolors.WARNING} {self.temp} {bcolors.ENDC}")

                exit()
                # {bcolors.FAIL}ERROR handler
            self.temp = ''
        else:
            return 0;

    def is_keyword(self, value):
        for item in Keyword:
            if value in item:
                return True
        return False

    def main(self):
        i = 0
        strf = False

        while i < len(input_code):

            if (input_code[i] == ' '):
                self.checkforiden()
                i = i + 1
                continue
            if input_code[i] == '\n':
                self.checkforiden()
                self.count = self.count + 1
                i = i + 1
                continue
            if input_code[i] == '#':
                self.checkforiden()
                self.tokens.append(Token(3, input_code[i], self.count))
                i = i + 1
                continue
            elif input_code[i:i + 2] in LogOP:
                self.checkforiden()
                self.tokens.append(Token(3, input_code[i:i + 2], self.count))
                i = i + 1
            elif input_code[i:i + 2] in RelOP:
                self.checkforiden()
                self.tokens.append(Token(3, input_code[i:i + 2], self.count))
                i = i + 1
            elif input_code[i:i + 2] in Incr:
                self.checkforiden()
                self.tokens.append(Token(3, input_code[i:i + 2], self.count))
                i = i + 1
            elif input_code[i] in Bracket:
                self.checkforiden()
                self.tokens.append(Token(3, input_code[i], self.count))

            elif input_code[i] in Punctuator:

                self.checkforiden()
                self.tokens.append(Token(3, input_code[i], self.count))

            elif input_code[i] in CompOP:
                self.checkforiden()
                self.tokens.append(Token(3, input_code[i], self.count))

            elif input_code[i] in AssOP:

                self.checkforiden()
                self.tokens.append(Token(3, input_code[i], self.count))

            elif input_code[i] in NegOP:
                self.checkforiden()
                self.tokens.append(Token(3, input_code[i], self.count))
            elif input_code[i] in ArithOP:
                self.checkforiden()
                self.tokens.append(Token(3, input_code[i], self.count))
            else:
                self.temp = self.temp + input_code[i]

                if (input_code[i] == '"'):
                    #self.tokens.append(Token(3, input_code[i], self.count))
                    if (self.temp == '"'):
                        self.temp = ''
                        i = i + 1
                        strf = True
                        while i < len(input_code) and input_code[i] != '"':

                            if (input_code[i:i + 2] == "\\t"):
                                self.temp = self.temp + '\t'
                                i = i + 2
                            elif (input_code[i:i + 2] == "\\n"):

                                self.temp = self.temp + '\n'
                                i = i + 2
                            else:
                                self.temp = self.temp + input_code[i]
                                i = i + 1

                            if (i == len(input_code) or i > len(input_code)):
                                print(
                                    f"...{bcolors.BOLD}{bcolors.FAIL} {bcolors.FAIL}ERROR: UNABLE TO RUN FILE {bcolors.OKBLUE} {os.path.abspath('sample.cpp')} {bcolors.FAIL} \n STRING QUOTES NOT CLOSED IN LINE NUMBER: {self.count} {bcolors.WARNING} {self.temp} {bcolors.ENDC}")
                                exit()

                        if (len(self.temp) > 0):
                            self.tokens.append(Token(5, self.temp, self.count))
                            strf = False
                            self.temp = ''
                        #self.tokens.append(Token(3, input_code[i], self.count))
                        i = i + 1
                        continue

                if (self.temp in Integers):

                    if (input_code[i + 1] != '.' and input_code[i+1] not in re.findall('[0-9]',input_code)):

                        j = re.findall('[a-zA-Z_][a-zA-Z_0-9]*', input_code[i + 1]);

                        if (input_code[i + 1] not in j):

                            self.tokens.append(Token(2, self.temp, self.count))
                            Integers.pop(Integers.index(self.temp))
                            
                            self.temp = ''


                elif (self.temp in Keyword):
                    self.tokens.append(Token(0, self.temp, self.count))
                    self.temp = ''



                elif (self.temp in DataType):
                    self.tokens.append(Token(8, self.temp, self.count))
                    self.temp = ''

                elif (self.temp in BoolConst):
                	self.tokens.append(Token(9,self.temp,self.count))
                	self.temp=''
                elif (self.temp in Floats):
                    self.tokens.append(Token(6, self.temp, self.count))
                    self.temp = ''

                if (input_code[i] == '\''):
                    #self.tokens.append(Token(3, input_code[i], self.count))
                    self.temp = ''
                    i = i + 1

                    if (input_code[i] == '\''):
                        #self.tokens.append(Token(3, input_code[i], self.count))
                        self.temp = ''
                        i = i + 1
                        continue
                    elif (input_code[i:i + 2] == '\\n' or input_code[i:i + 2] == '\\t' or ord(input_code[i])):
                        if (input_code[i:i + 2] == '\\n' or input_code[i:i + 2 == '\\t']):
                            if (input_code[i + 2] == '\''):
                                self.tokens.append(Token(7, input_code[i:i + 2], self.count))
                                self.temp = ''
                                i = i + 2
                                #self.tokens.append(Token(3, input_code[i], self.count))
                                i = i + 1
                                continue
                            else:
                                print(
                                    f"...{bcolors.BOLD}{bcolors.FAIL} {bcolors.FAIL}ERROR: UNABLE TO RUN FILE {bcolors.OKBLUE} {os.path.abspath('sample.cpp')} {bcolors.FAIL} \n CHARACTER QUOTES NOT CLOSED IN LINE NUMBER: {self.count} {bcolors.WARNING} {input_code[i]} {bcolors.ENDC}")
                                exit()
                        else:

                            if (input_code[i + 1] == '\''):
                                self.tokens.append(Token(7, input_code[i], self.count))
                                self.temp = ''
                                i = i + 1
                                #self.tokens.append(Token(3, input_code[i], self.count))
                                #i = i + 1
                            else:
                                print(
                                    f"...{bcolors.BOLD}{bcolors.FAIL} {bcolors.FAIL}ERROR: UNABLE TO RUN FILE {bcolors.OKBLUE} {os.path.abspath('sample.cpp')} {bcolors.FAIL} \n CHARACTER QUOTES NOT CLOSED IN LINE NUMBER: {self.count} {bcolors.WARNING} {input_code[i]} {bcolors.ENDC}")
                                exit()

                    else:
                        print(
                            f"...{bcolors.BOLD}{bcolors.FAIL} {bcolors.FAIL}ERROR: UNABLE TO RUN FILE {bcolors.OKBLUE} {os.path.abspath('sample.cpp')} {bcolors.FAIL} \n CHARACTER DECLARATION NOT VALID IN LINE NUMBER: {self.count} {bcolors.WARNING} {input_code[i]} {bcolors.ENDC}")
                        exit()

            i = i + 1
            continue


class Parser:

    def __init__(self,tok):
        self.tok=tok.head
        self.lookahead=None

    def nextToken(self):
        if(self.lookahead==None):
            return self.tok
        else:
            self.tok=self.tok.next
            return self.tok

    def includestmt(self):
        data = self.lookahead.data['value'];
        if (data == '#'):
            self.match("#")
            self.match("include")
            self.match("<")
            self.matchID(self.lookahead.data['TYPE'])
            self.match('>')
        else:
            print(f"{bcolors.FAIL}ERROR IN INCLUDE STMT ")
    def includelist_(self):
        data = self.lookahead.data['value'];
        if (data == '#'):
            self.includestmt()
            self.includelist_()
        elif(data in ['$',"using"]):
            return
        else:
            print(f"{bcolors.FAIL}ERROR IN INCLUDE LIST _")


    def includelist(self):
        data = self.lookahead.data['value'];
        if (data == '#'):
            self.includestmt()
            self.includelist_()
        else:
            print(f"{bcolors.FAIL}ERROR IN INCLUDE LIST")

    def namespace(self):
        data = self.lookahead.data['value'];
        if(data == 'using'):
            self.match('using')
            self.match('namespace')
            self.matchID(self.lookahead.data["TYPE"])
            self.match(';')
        else:
            print(f"{bcolors.FAIL}ERROR IN NAMESPACE")
    def start(self):
        data = self.lookahead.data['value'];
        if(data == '#'):
            self.includelist()
            self.namespace()
            self.program()
        elif(data == "$"):
            return
        else:
            print(f"{bcolors.FAIL}ERROR IN START")



    def vardeclist_(self):
        data = self.lookahead.data['value'];
        if (data == ','):
            self.match(',')
            self.vardecinit()
            self.vardeclist_()
        elif (data == ';'):
            return
        else:
            print(f"{bcolors.FAIL}ERROR IN VARRAIBLE dec list _")
    def vardecid(self):
        data = self.lookahead.data['value']

        if ( self.lookahead.data["TYPE"]=="IDENTIFIER"):
            self.matchID(self.lookahead.data["TYPE"])
            self.vardecid_()
        else:
            print(f"{bcolors.FAIL}ERROR IN VARDEC ID")

    def vardecid_(self):
        data = self.lookahead.data['value'];

        if ( data == '['):
            self.match('[')
            if(self.lookahead.data['TYPE']=='INTEGER_CONSTANT'):
                self.lookahead = self.nextToken()
                self.match(']')
            else:
                print(f"{bcolors.FAIL}ERROR: NOT A CONST")
        elif ( data == ',' or data == ';' or data == '='):
            return
        else:
            print("EROR")
    def RelOP(self):
        data = self.lookahead.data['value'];

        if( data == '<='):
            self.match('<=')
        elif ( data == '<'):
            self.match('<')
        elif ( data == '>'):
            self.match('>')
        elif ( data == '>='):
            self.match('>=')
        elif (data == '=='):
            self.match('==')
        elif ( data == '!='):
            self.match('!=')
        else:
            print(f"{bcolors.FAIL}ERROR IN RelOP !")


    def expression(self):
        data = self.lookahead.data['value'];

        CONST = [
            'INTEGER_CONSTANT',
            'STRING_CONSTANT', 'FLOAT_CONSTANT', 'CHAR_CONSTANT', 'BoolConstT'
        ]
        data_next = self.lookahead.next
        if (self.lookahead.data["TYPE"] == "IDENTIFIER" and data_next.data["value"] == "++"):
        	self.matchID(self.lookahead.data["TYPE"])
        	self.match("++")
        	
        elif(self.lookahead.data["TYPE"] == "IDENTIFIER" and data_next.data["value"] == "--"):
        	self.matchID(self.lookahead.data["TYPE"])
        	self.match("--")
        elif(self.lookahead.data["TYPE"] == "IDENTIFIER" and data_next.data["value"] == "="):
        	self.matchID(self.lookahead.data["TYPE"])
        	self.match("=")
        	self.expression()
        elif (data == '!' or self.lookahead.data['TYPE'] == 'IDENTIFIER'or data == '(' or self.lookahead.data['TYPE'] in CONST):
            self.simpleExp()
        else:
            print(f"{bcolors.FAIL}ERROR IN EPRESSION")


    def arglist_(self):
        data = self.lookahead.data['value'];
        if(data == ','):
            self.match(',')
            self.expression()
            self.arglist_()
        elif (data ==')'):
            return
        else:
            print(f"{bcolors.FAIL}ERROR IN ARG LIST _")

    def arglist(self):
        data = self.lookahead.data['value'];
        CONST = [
            'INTEGER_CONSTANT',
            'STRING_CONSTANT', 'FLOAT_CONSTANT', 'CHAR_CONSTANT', 'BoolConstT'
        ]
        if (data == '!' or self.lookahead.data['TYPE'] == 'IDENTIFIER' or data == '(' or self.lookahead.data['TYPE'] in CONST):
            self.expression()
            self.arglist_()
        else:
            print(f"{bcolors.FAIL}ERROR IN  ARG LIST")

    def args(self):
        data = self.lookahead.data['value'];

        CONST = [
            'INTEGER_CONSTANT',
            'STRING_CONSTANT', 'FLOAT_CONSTANT', 'CHAR_CONSTANT', 'BoolConstT'
        ]
        if (data == '!' or self.lookahead.data['TYPE'] == 'IDENTIFIER' or data == '(' or self.lookahead.data['TYPE'] in CONST):
            self.arglist()
        elif ( data == ')'):
            return
        else:
            print(f"{bcolors.FAIL}ERROR IN  ARGS")
    def constants(self):
        data = self.lookahead.data['value']
        CONST = [
            'INTEGER_CONSTANT',
            'STRING_CONSTANT', 'FLOAT_CONSTANT', 'CHAR_CONSTANT', 'BoolConstT'
        ]
        if(self.lookahead.data['TYPE'] in CONST):
            self.lookahead=self.nextToken()
        else:
            print(f"{bcolors.FAIL}ERROR IN CONSTANTS ")
    def factor_(self):
        data = self.lookahead.data['value']

        if(data == '('):
            self.match('(')
            self.args()
            self.match(')')
        elif ( data == '*' or data == '/' or data == '%' or data == '+' or data == '-' or data == '<=' or data == '<' or data == '>' or data == '>=' or data == '==' or data == '!=' or data == '&&' or data=="||" or data == ',' or data == ';' or data == ')' or data == "<<"):
            return
        else:
            print(f"{bcolors.FAIL}ERROR IN FACTOR _ " + data)
    def factor(self):
        data = self.lookahead.data['value'];
        CONST = [
            'INTEGER_CONSTANT',
            'STRING_CONSTANT', 'FLOAT_CONSTANT', 'CHAR_CONSTANT', 'BoolConstT'
        ]
        if (self.lookahead.data['TYPE'] == 'IDENTIFIER'):
            self.matchID(self.lookahead.data['TYPE'])
            self.factor_()
        elif (data == '('):
            self.match('(')
            self.expression()
            self.match(')')
        elif (self.lookahead.data['TYPE'] in CONST):
            self.constants()
        else:
            print(f"{bcolors.FAIL}ERROR IN  FACTOR")



    def unaryExp(self):
        data = self.lookahead.data['value'];
        CONST = [
            'INTEGER_CONSTANT',
            'STRING_CONSTANT', 'FLOAT_CONSTANT', 'CHAR_CONSTANT', 'BoolConstT'
        ]
        if (self.lookahead.data['TYPE'] == 'IDENTIFIER' or data == '(' or self.lookahead.data['TYPE'] in CONST):
            self.factor()
        else:
            print(f"{bcolors.FAIL}ERROR IN UNARY EXP")

    def mulOp(self):
        data = self.lookahead.data['value']
        if (data =='*'):
            self.match('*')
        elif (data=='/'):
            self.match('/')
        elif (data=='%'):
            self.match('%')
        else:
            print(f"{bcolors.FAIL}ERROR WITH MULOP")
    def mulExp_(self):
        data = self.lookahead.data['value']
        
        if ( data == '*' or data == '/' or data == '%'):
            self.mulOp()
            self.unaryExp()
            self.mulExp_()
        elif ( data == '+' or data == '-' or data == '<=' or data == '<' or data == '>' or data == '>=' or data == '==' or data == '!=' or data == '&&' or data=="||" or data == ',' or data == ';' or data == ')' or data=="<<"):
            return
        else:
            print(f"{bcolors.FAIL}ERROR IN MUL EXP _")
    def sumOP(self):
        data = self.lookahead.data['value']
        if( data == '+'):
            self.match('+')
        elif( data == '-'):
            self.match('-')
        else:
            print(f"{bcolors.FAIL}ERROR IN SUM OP")
    def sumExp_(self):
        data = self.lookahead.data['value'];
        if (data == '+' or data == '-'):
            self.sumOP()
            self.mulExp()
            self.sumExp_()
        elif (data == '<=' or data == '<' or data == '>' or data == '>=' or data == '==' or data == '!=' or data == '&&' or data=="||" or data == ',' or data == ';' or data == ')' or data=="<<"):
            return
        else:
            print(f"{bcolors.FAIL}ERROR IN SUM EXP_")
    def mulExp(self):
        data = self.lookahead.data['value'];
        CONST = [
            'INTEGER_CONSTANT',
            'STRING_CONSTANT', 'FLOAT_CONSTANT', 'CHAR_CONSTANT', 'BoolConstT'
        ]
        if (self.lookahead.data['TYPE'] == 'IDENTIFIER' or data == '(' or self.lookahead.data['TYPE'] in CONST):
            self.unaryExp()
            self.mulExp_()
        else:
            print(f"{bcolors.FAIL}ERROR IN SUM EXP_")
    def sumExp(self):
        data = self.lookahead.data['value'];
        CONST = [
            'INTEGER_CONSTANT',
            'STRING_CONSTANT', 'FLOAT_CONSTANT', 'CHAR_CONSTANT', 'BoolConstT'
        ]
        if (self.lookahead.data['TYPE'] == 'IDENTIFIER' or data == '(' or self.lookahead.data['TYPE'] in CONST):
            self.mulExp()
            self.sumExp_()
        else:
            print(f"{bcolors.FAIL}ERROR IN SUM EXP")
    def relExp_(self):
        data = self.lookahead.data['value'];
        if (data == '<=' or data == '<' or data == '>' or data == '>=' or data == '==' or data == '!='):
            self.RelOP()
            self.sumExp()
            self.relExp_()
        elif (data == '||' or data == '&&' or data ==',' or data == ';' or data == ')' or data=="<<"):
            return
        else:
            print(f"{bcolors.FAIL}ERROR IN REL EXP !")
    def relExp(self):
        data = self.lookahead.data['value'];
        CONST = [
            'INTEGER_CONSTANT',
            'STRING_CONSTANT', 'FLOAT_CONSTANT', 'CHAR_CONSTANT', 'BoolConstT'
        ]
        if (self.lookahead.data['TYPE'] == 'IDENTIFIER' or data == '(' or self.lookahead.data['TYPE'] in CONST):
            self.sumExp()
            self.relExp_()
        else:
            print(f"{bcolors.FAIL}ERROR IN REL EXP !")
    def unaryRelExp(self):
        data = self.lookahead.data['value'];
        CONST = [
            'INTEGER_CONSTANT',
            'STRING_CONSTANT', 'FLOAT_CONSTANT', 'CHAR_CONSTANT', 'BoolConstT'
        ]
        if (data == '!'):
            self.match('!')
            self.unaryRelExp()
        elif (self.lookahead.data['TYPE'] == 'IDENTIFIER' or data == '(' or self.lookahead.data['TYPE'] in CONST ):
            self.relExp()
        else:
            print(f"{bcolors.FAIL}ERROR IN UNARY REL EXP")


    def andExp_(self):
        data = self.lookahead.data['value'];
        if( data == '&&'):
            self.match("&&")
            self.unaryRelExp()
            self.andExp_()
        elif (data == '||' or data == ',' or data == ';' or data == ')' or data == "<<"):
            return
        else:
            print(f"{bcolors.FAIL}ERROR IN AND EXP _")
    def andExp(self):
        data = self.lookahead.data['value'];
        CONST = [
            'INTEGER_CONSTANT',
            'STRING_CONSTANT', 'FLOAT_CONSTANT', 'CHAR_CONSTANT', 'BoolConstT'
        ]
        if (data == '!' or self.lookahead.data['TYPE'] == 'IDENTIFIER' or data == '(' or self.lookahead.data['TYPE'] in CONST):
            self.unaryRelExp()
            self.andExp_()
        else:
            print(f"{bcolors.FAIL}ERROR IN and EXP")

    def SimpleExp_(self):
        data = self.lookahead.data['value'];
        if ( data == '||'):
            self.match('||')
            self.andExp()
            self.SimpleExp_()
        elif (data == ',' or data == ';' or data == ')' or data == "<<"):
            return
        else:
            print(f"{bcolors.FAIL}ERROR IN SIMPLE EXP _")
    def simpleExp(self):
        data = self.lookahead.data['value'];
        CONST = [
            'INTEGER_CONSTANT',
            'STRING_CONSTANT', 'FLOAT_CONSTANT', 'CHAR_CONSTANT', 'BoolConstT'
        ]
        if(data == '!' or self.lookahead.data['TYPE'] == 'IDENTIFIER' or  data == '(' or self.lookahead.data['TYPE'] in CONST):
            self.andExp()
            self.SimpleExp_()
        else:
            print(f"{bcolors.FAIL}ERROR IN SIMPLE EXP")


    def vardecinit_(self):
        data = self.lookahead.data['value'];

        if(data == '='):
            self.match('=')
            self.simpleExp()
        elif(data == ',' or data == ';' ):
            return
        else:
            print(f"{bcolors.FAIL}ERROR IN VARDECINIT_")

    def vardecinit(self):
        data = self.lookahead.data['value'];

        if (self.lookahead.data["TYPE"] == "IDENTIFIER"):
            self.vardecid()
            self.vardecinit_()
        else:
            print(f"{bcolors.FAIL}ERROR IN VARRAIBLE INIT")

    def vardeclist(self):
        data = self.lookahead.data['value'];

        if (self.lookahead.data["TYPE"] == "IDENTIFIER"):
            self.vardecinit()
            self.vardeclist_()
        else:
            print(f"{bcolors.FAIL}ERROR IN VARRAIBLE DECLIST")

    def varriable(self):
        data = self.lookahead.data['value'];

        if(self.lookahead.data["TYPE"] == "IDENTIFIER"):
            self.vardeclist()
            self.match(';')
        else:
            print(f"{bcolors.FAIL}ERROR IN VARRAIBLE ONLY")

    def declaration__(self):
        data = self.lookahead.data['value'];
        data_next = self.lookahead.next
        if (self.lookahead.data['TYPE'] == "IDENTIFIER" and data_next.data['value'] == '('):
            self.function()
        elif (self.lookahead.data['TYPE'] == "IDENTIFIER"):
            self.varriable()
        else:
            print(f"{bcolors.FAIL}ERROR IN DELARATION__")
    def declaration(self):
        data = self.lookahead.data['value'];

        if (data in DataType):
            self.typeid()
            self.declaration__()
        else:
            print(f"{bcolors.FAIL}ERROR:  IN declaration FUNCTION")
    def declaration_(self):
        data = self.lookahead.data['value'];

        if (data in DataType):
            self.declaration()
            self.declaration_()
        elif (data == '$'):
            return
        else:
            print(f"{bcolors.FAIL}ERROR:  IN declaration_ FUNCTION")

    def declist(self):
        data = self.lookahead.data['value'];

        if (data in DataType):
            self.declaration()
            self.declaration_()
        else:
            print(f"{bcolors.FAIL}ERROR:  IN declist FUNCTION")

    def program(self):
        data = self.lookahead.data['value'];

        if ( data in DataType):
            self.declist()
        elif (data == '$'):
            return
        else:
            print(f"{bcolors.FAIL}ERROR:  IN PROGRAM FUNCTION")
    def function(self):
        data = self.lookahead.data['value'];
        if(self.lookahead.data['TYPE'] == 'IDENTIFIER'):
            self.matchID(self.lookahead.data['TYPE'])
            self.match('(')
            self.paramas()
            self.match(')')
            self.match('{')
            self.stmtlist()
            self.match('}')
        elif(data == '$'):
            return
        else:
            print(f"{bcolors.FAIL}ERROR IN FUNCTION SYNTAX TOKEN: ",self.lookahead.data)
            exit()
    def stmtlist(self):
        data = self.lookahead.data['value'];
        
        CONST = [
            'INTEGER_CONSTANT',
            'STRING_CONSTANT', 'FLOAT_CONSTANT', 'CHAR_CONSTANT', 'BoolConstT'
        ]
        if(data in ['!','(','if','cout','cin','while','for','switch','return','break'] or data in DataType or self.lookahead.data["TYPE"] in ["IDENTIFIER" , CONST]):
            self.statment()
            self.stmtlist_()
        else:
            print(f"{bcolors.FAIL}ERROR IN STMTLIST")
    def iteration(self):
        data = self.lookahead.data['value'];
        if(data == 'for'):
            self.match('for')
            self.match('(')
            self.vardecinit()
            self.match(';')
            self.simpleExp()
            self.match(';')
            self.expression()
            self.match(')')
            self.match('{')
            self.stmtlist()
            self.match('}')
        elif(data == "while"):
        	self.match("while")
        	self.match("(")
        	self.simpleExp()
        	self.match(")")
        	self.match("{")
        	self.stmtlist()
        	self.match("}")
        else:
            print('{bcolors.FAIL}ERROR IN ITERATION')
    def switch(self):
    	data=self.lookahead.data["value"]
    	if(data =="switch"):
    		self.match("switch")
    		self.match("(")
    		self.simpleExp()
    		self.match(")")
    		self.match("{")
    		self.caselist()
    		self.default()
    		self.match("}")
    	else:
    		print(f"{bcolors.FAIL}ERROR in SWITCH")
    def caselist(self):
    	data = self.lookahead.data["value"]
    	if(data=="case"):
    		self.onecase()
    		self.caselist()
    	elif(data=="default" or data == "}"):
    		return
    	else:
    		print(f"{bcolors.FAIL}ERROR IN CASELIST")
    		
    def onecase(self):
    		data = self.lookahead.data["value"]
    		if(data=="case"):
    			self.match("case")
    			if(self.lookahead.data["TYPE"] in CONST):
    				self.lookahead =self.nextToken()
    				self.match(":")
    				self.stmtlist()
    			else:
    				print(f"{bcolors.FAIL}ERROR IN CONSTANTS IN SWITCH CASE")
    		else: 
    		     print(f"{bcolors.FAIL}ERROR IN ONE CASE")
    		
    	 	
    def default(self):
    	data=self.lookahead.data["value"]
    	if(data == "default"):
    		self.match("default")
    		self.match(":")
    		self.stmtlist()
    	elif(data == "}"):
    		return
    	else:
    		print(f"{bcolors.FAIL}ERROR IN DEFAULT")
    def selection(self):
    	data =self.lookahead.data["value"]
    	if(data == "if"):
    		self.match("if")
    		self.match("(")
    		self.simpleExp()
    		self.match(")")
    		self.match("{")
    		self.stmtlist()
    		self.match("}")
    		self.selection_()
    	else:
    		print(f"{bcolors.FAIL}ERROR IN SELECTION: "+data)
    def selection_(self):
    	data = self.lookahead.data["value"]
    	if(data == ";"):
    		self.match(";")
    	elif(data =="else"):
    		self.match("else")
    		self.match("{")
    		self.stmtlist()
    		self.match("}")
    	else:
    		print(f"{bcolors.FAIL}ERROR IN IF CONDITION: TOKEN "+data)
    		exit()
    
    def statment(self):
        data = self.lookahead.data['value'];
        if(data in ['for','while']):
            self.iteration()
        elif(data in ['return']):
            self.returnstmt()
        elif(data in ['if']):
            self.selection()
        elif(data in ['switch']):
            self.switch()
        elif(data in ['break']):
            self.match("break")
            self.match(";")
        elif(data == "continue"):
        	self.match("continue")
        	self.match(";")
        elif(data in ["cin","cout"]):
        	self.input_output()
        elif(data in DataType):
            self.declaration()
        elif (data in ['!','('] or self.lookahead.data["TYPE"] in ["IDENTIFIER", CONST]):
            self.expression()
            self.match(";")
        else:
            print(f"{bcolors.FAIL}ERROR IN STATEMENT")

    def printlist(self):
    	data= self.lookahead.data["value"]
    	if(data == "<<"):
    		self.single()
    		self.printlist_()
    	else:
    		print(f"{bcolors.FAIL}ERROR IN PRINTLIST :")
    def single(self):
    	data=self.lookahead.data["value"]
    	if(data == "<<"):
    		self.match("<<")
    		self.expression()
    	else:
    		print(f"{bcolors.FAIL}ERROR IN SINGLE: ")
    def printlist_(self):
    	data =self.lookahead.data["value"]
    	data_next = self.lookahead.next
    	if(data == "<<" and data_next.data["value"] not in ["endl"]):
    		self.single()
    		self.printlist_()
    	elif(data == "<<" or data == ";" ):
    		return 
    	else:
    		print(f"{bcolors.FAIL}ERROR IN PRINTLIST_")
    def endstmt(self):
    	data = self.lookahead.data["value"]
    	if(data == "<<"):
    		self.match("<<")
    		self.match("endl")
    		self.match(";")
    	elif(data == ";"):
    		self.match(";")
    	else:
    		print(f"{bcolors.FAIL}ERROR IN ENDSTMT")
    def input_output(self):
    	data = self.lookahead.data["value"]
    	if(data == "cout"):
    		self.match("cout")
    		self.printlist()
    		self.endstmt()
    	elif(data == "cin"):
    		self.match("cin")
    		self.inputlist()
    		self.match(";")
    	else:
    		print(f"{bcolors.FAIL}ERROR IN INPUT_OUTPUT TOKEN: "+self.lookahead.data)
    def inputlist(self):
    	data = self.lookahead.data["value"]
    	if(data == ">>"):
    		self.singleinput()
    		self.inputlist_()
    	else:
    		print(f"{bcolors.FAIL}ERROR IN INPUTLIST")
    def inputlist_(self):
    	data = self.lookahead.data["value"]
    	if(data==">>"):
    		self.singleinput()
    		self.inputlist_()
    	elif(data == ";"):
    		return;
    	else:
    		print(f"{bcolors.FAIL}ERROR IN INPUTLIST_")
    def singleinput(self):
    	data=self.lookahead.data["value"]
    	if(data == ">>"):
    		self.match(">>")
    		self.matchID(self.lookahead.data["TYPE"])
    	else:
    		print(f"{bcolors.FAIL}ERROR IN SINGLEINPUT:")
    def stmtlist_(self):
        data = self.lookahead.data['value'];

        if (data in ['!', '(','cout','cin','if', 'while', 'for', 'switch', 'return', 'break'] or data in DataType or self.lookahead.data["TYPE"] in ["IDENTIFIER", CONST]):
            self.statment()
            self.stmtlist_()
        elif(data in ['}'] or data == "default"):
            return
        else:
            print(f"{bcolors.FAIL}ERROR IN STMTLIST_" + data)

    def returnstmt(self):
        data = self.lookahead.data['value'];
        if(data == 'return'):
            self.match('return')
            self.expression()
            self.match(';')
        elif(data == '}'):
            return
        else:
            print(f"{bcolors.FAIL}ERROR IN STATEMENT: ",self.lookahead.data)
            exit()
    def data(self):
        value = self.lookahead.data['TYPE'];
        data = self.lookahead.data['value'];
        conslist = ['INTEGER_CONSTANT','STRING_CONSTANT', 'FLOAT_CONSTANT', 'CHAR_CONSTANT','BoolConstT']
        if(value in conslist):
            self.lookahead = self.nextToken()

        elif (data == ';'):
            return
        else:
            print(f"{bcolors.FAIL}ERROR IN RETURN DATA: ",self.lookahead.data)
            exit()
    def paramas(self):
        data = self.lookahead.data['value'];
        if (data in DataType):
            self.paralist()
        elif (data == ')'):
            return
        else:
            print(f"{bcolors.FAIL}ERROR WITH PARAMETERS: ",self.lookahead.data)
            exit()
    def paralist(self):
        data = self.lookahead.data['value'];
        if(data in DataType):
            self.parameter()
            self.paralist_()
        else:
            print(f"{bcolors.FAIL}ERROR WITH PARALIST: ", self.lookahead.data)
            exit()
    def paralist_(self):
        data = self.lookahead.data['value'];
        if(data == ','):
            self.match(',')
            self.parameter()
            self.paralist_()
        elif(data == ')'):
            return
        else:
            print(f"{bcolors.FAIL}ERROR WITH PARALIST_: ", self.lookahead.data)
            exit()
    def parameter(self):
        data = self.lookahead.data['value'];
        if( data in DataType):
            self.vartypeid()
            self.paraid()
        else:
            print(f"{bcolors.FAIL}ERROR WITH PARAMETERS: ", self.lookahead.data)
            exit()
    def paraid(self):
        type = self.lookahead.data['TYPE'];
        if(type == 'IDENTIFIER'):
            self.matchID(type)
            self.paraid_()
        else:
            print(f"{bcolors.FAIL}ERROR IN PARAMETERS IDENTIFIER: ",self.lookahead.data)
            exit()
    def paraid_(self):
        data = self.lookahead.data['value'];
        if(data == '['):
            self.match('[')
            self.match(']')
        elif (data == ')' or data == ','):
            return
        else:
            print(f"{bcolors.FAIL}ERROR IN PARAMETERS IDENTIFIER: ", self.lookahead.data)
            exit()

    def match(self,t):
        if(self.lookahead.data['value'] == t):
            self.lookahead= self.nextToken()

        else:
            print(f"SYNTAX {bcolors.FAIL}ERROR NEAR TOKEN: ",self.lookahead.data['value'] , " IN LINE NUMBER: ", self.lookahead.data['LINE_NUMBERS'])
            exit()
    def matchID(self,type):

        if(type=='IDENTIFIER'):
            self.lookahead = self.nextToken()
        else:
            print(f"{bcolors.FAIL}ERROR IN TOKEN: " , self.lookahead.data)
            print("EXPECTED TO BE IDENTIFIER ...")
            exit()

    def typeid(self):
        data = self.lookahead.data['value'];
        type = self.lookahead.data['TYPE'];
        if(data == 'int'):
            self.match('int')
        elif(data == 'float'):
            self.match('float')
        elif(data == 'string'):
            self.match('string')
        elif(data == 'char'):
            self.match('char')
        elif(data == 'bool'):
            self.match('bool')
        elif (data == 'void'):
            self.match('void')
        else:
            print(f"{bcolors.FAIL}ERROR WITH TYPE IN TOKEN: " , self.lookahead.data)
            exit()

    def vartypeid(self):
        data = self.lookahead.data['value'];
        type = self.lookahead.data['TYPE'];
        if (data == 'int'):
            self.match('int')
        elif (data == 'float'):
            self.match('float')
        elif (data == 'string'):
            self.match('string')
        elif (data == 'char'):
            self.match('char')
        elif (data == 'bool'):
            self.match('bool')
        else:
            print(f"{bcolors.FAIL}ERROR WITH TYPE IN TOKEN: ", self.lookahead.data)
            exit()


def lexer():
    lexer = Lexer()
    lexer.main()
    tok = Tokens()
    for token in lexer.tokens:
        tok.append(token.value, token.line_number, token.type)
    tok.append('$', token.line_number + 1, "EOF")
    tok.printList()
    #print("\nSYMBOL TABLE: \n")
    #lexer.sym.printList()
    #print("\n")
    check = Parser(tok)
    check.lookahead = check.nextToken()
    check.start()


    if check.lookahead.data['value']  == '$':
        print(f"{bcolors.OKGREEN}SYNTAX IS CORRECT... ")



if __name__ == '__main__':
    lexer()