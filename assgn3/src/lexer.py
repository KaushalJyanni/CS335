#!/usr/bin/python2
import ply.lex as lex
import sys
reserved = {
   'BEGIN' : 'BEGIN',
   'end' : 'END',
   'and' : 'AND',
   'begin' : 'begin',
   'break' : 'BREAK',
   'case' : 'CASE',
   'class' : 'CLASS',
   'def' : 'DEF',
   'do' : 'DO',
   'else' : 'ELSE',
   'elsif' : 'ELSIF',
   'false' : 'FALSE',
   'for' : 'FOR',
   'if' : 'IF',
   'in' : 'IN',
   'next' : 'NEXT',
   'nil' : 'NIL',
   'not' : 'NOT',
   'or' : 'OR',
   'return' : 'RETURN',
   'then' : 'THEN',
   'true' : 'TRUE',
   'unless' : 'UNLESS',
   'until' : 'UNTIL',
   'when' : 'WHEN',
   'while' : 'WHILE'
}

arithmetic = [
'EQUAL','PLUS','MINUS','MULTIPLY','DIVIDE','REMAINDER','EXPONENT','BINARY_OR','BINARY_XOR','BINARY_AND','COMPARISON','GREATER_THAN','GREATER_THAN_EQ','LESS_THAN','LESS_THAN_EQ','EQUALS','NOT_EQUALS','LOGICAL_NOT','BINARY_1COMPLEMENT','BINARY_LSHIFT','BINARY_RSHIFT','LOGICAL_AND','LOGICAL_OR','PLUS_EQ','MINUS_EQ','MULTIPLY_EQ','DIVIDE_EQ','REMAINDER_EQ','EXPONENT_EQ','BINARY_OR_EQ','BINARY_XOR_EQ','BINARY_AND_EQ','BINARY_LSHIFT_EQ','BINARY_RSHIFT_EQ','LOGICAL_AND_EQ','LOGICAL_OR_EQ'
]

symbols=[
'LPARENTHESIS','RPARENTHESIS','LBRACKET','RBRACKET','LCBRACKET','RCBRACKET','DOT','DOUBLEDOT','COMMA','SEMICOLON','SINGLEQUOTES','DOUBLEQUOTES','COLON','DOUBLECOLON','DOLLAR','BACKSLASH'
]

tokens=list(reserved.values())+arithmetic+symbols+['VARIABLE','DOLLAR_VARIABLE','FLOATNUMBER','INTNUMBER','STRING','COMMENT','IGNORED', 'NEWLINE']#,'STRING'
#arithmetic
t_EQUAL = r'='
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'/'
t_REMAINDER  = r'%'
t_EXPONENT  = r'\*\*'
t_BINARY_OR  = r'\|'
t_BINARY_XOR  = r'\^'
t_BINARY_AND  = r'&'
t_COMPARISON  = r'<=>'
t_GREATER_THAN  = r'>'
t_GREATER_THAN_EQ  = r'>='
t_LESS_THAN = r'<'
t_LESS_THAN_EQ = r'<='
t_EQUALS = r'=='
t_NOT_EQUALS = r'{!}='
t_LOGICAL_NOT = r'!'
t_BINARY_1COMPLEMENT = r'~'
t_BINARY_LSHIFT = r'<<'
t_BINARY_RSHIFT = r'>>'
t_LOGICAL_AND = r'&&'
t_LOGICAL_OR = r'\|\|'
t_PLUS_EQ = r'\+='
t_MINUS_EQ = r'-='
t_MULTIPLY_EQ = r'\*='
t_DIVIDE_EQ = r'/='
t_REMAINDER_EQ = r'%='
t_EXPONENT_EQ = r'\*\*='
t_BINARY_OR_EQ = r'\|='
t_BINARY_XOR_EQ = r'\^='
t_BINARY_AND_EQ = r'&='
t_BINARY_LSHIFT_EQ = r'<<='
t_BINARY_RSHIFT_EQ = r'>>='
t_LOGICAL_AND_EQ = r'&&='
t_LOGICAL_OR_EQ = r'\|='
#symbols
t_LPARENTHESIS = r'\('
t_RPARENTHESIS = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r']'
t_LCBRACKET = r'{'
t_RCBRACKET = r'}'
t_DOUBLEDOT = r'\.\.'
t_DOT = r'\.'
t_COMMA = r','
t_SEMICOLON = r';'
t_SINGLEQUOTES = r'\''
t_DOUBLEQUOTES = r'\"'
t_COLON = r':'
t_DOUBLECOLON = r'::'
t_DOLLAR = r'\$'
t_BACKSLASH=r'\\'
t_NEWLINE = r'[\n]+'

def t_VARIABLE(t):
   r'[A-Za-z_][A-Za-z0-9_]*'
   t.type = reserved.get(t.value,"VARIABLE")
   return t

def t_DOLLAR_VARIABLE(t):
   r'$[A-Za-z_][A-Za-z0-9_]*'
   t.type = reserved.get(t.value,"DOLLAR_VARIABLE")
   return t


def t_FLOATNUMBER(t):
   r'\d+\.\d+'
   t.value=str(float(t.value))
   return t

def t_INTNUMBER(t):
   r'\d+'
   t.value = str(int(t.value))
   return t

def t_STRING(t):
   r'"[^\"]*"| \'[^\']*\'|\`[^\`]*\`'
   t.value=str(t.value)[1:-1]
   return t


#comments are ignored
def t_COMMENT(t):
   r'=begin(.|\n)*=end | \#.*'
   
   
def t_IGNORED(t):
   r'[ \t]'
   pass

# def t_NEWLINE(t):
#     r'\n+'
#     t.value = str(t.value)
#     # t.lexer.lineno += len(t.value)
#     return t



def t_error(t):
   print("ERROR: Unknown character '%s'" % t.value[0])
   t.lexer.skip(1)
   return ""



lexer = lex.lex()
file = sys.argv[1]
try:
   with open(file) as f:
      data=f.read()
except IOError:
   print "unable to open file"
   sys.exit()
# print "data = ",str(data)
lexer.input(str(data))
token = lexer.token() 
results=dict()
while token:
   print token
   if token.type in results:
      results[token.type][0]+=1
      if token.value in results[token.type][1:]:
         token = lexer.token()
         continue
      else:
         results[token.type].append(token.value)
   else:
      results[token.type]=[0]
      results[token.type][0]+=1
      results[token.type].append(token.value)
   token = lexer.token()
# print results
print "\n"
print "TOKEN".ljust(25),"Occurences".ljust(15),"Lexemes"
print "-------------------------------------------------"
keys = list(reserved.values())+['VARIABLE','DOLLAR_VARIABLE','FLOATNUMBER','INTNUMBER','STRING','COMMENT','IGNORED', 'NEWLINE']+arithmetic+symbols
# print keys
for item in keys:
   if item in results.keys():
      print str(item).ljust(25),str(results[item][0]).ljust(15),str(results[item][1])
      for value in results[item][2:]:
         print "".ljust(41),value
