import ply.yacc as yacc
import sys
from lexer import tokens
import types
body =""
filename = sys.argv[1]

precedence = (
    ('right','EQUAL', 'NOT'),
    ('left', 'LOGICAL_OR'),
    ('left', 'LOGICAL_AND'),
    ('left', 'BINARY_OR'),
    ('left', 'BINARY_XOR'),
    ('left', 'BINARY_AND'),
    ('left', 'EQUAL', 'NOT_EQUALS'),
    ('left', 'LESS_THAN', 'GREATER_THAN','LESS_THAN_EQ','GREATER_THAN_EQ'),
    ('left', 'BINARY_LSHIFT', 'BINARY_RSHIFT'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE','REMAINDER'),
)

def p_program(p):
	'''program : compstmt'''
	p[0]=["program"]
	for i in range(1,len(p)):
		p[0].append(p[i])

def p_compstmt(p):
	'''compstmt : stmts opt_terminals'''
	p[0]=["compstmt"]
	for i in range(1,len(p)):
		p[0].append(p[i])

def p_stmts(p):
	'''stmts : stmt opt_terminals
			 | stmts terminals stmt'''
	p[0]=["stmts"]
	for i in range(1,len(p)):
		p[0].append(p[i])

##edited last rule removed compstmt end
def p_stmt(p):
	'''stmt : call DO compstmt END
			| stmt IF expr
			| stmt WHILE expr
			| stmt UNLESS expr
			| stmt UNTIL expr
			| BEGIN LCBRACKET compstmt RBRACKET
			| END LCBRACKET compstmt RBRACKET
			| expr'''
	p[0]=["stmt"]
	for i in range(1,len(p)):
		p[0].append(p[i])

def p_expr(p):
	'''expr : mlhs EQUAL mrhs
			| RETURN call_args
			| expr AND expr
			| expr OR expr
			| NOT expr
			| command
			| LOGICAL_NOT command
			| args'''
	p[0]=["expr"]
	for i in range(1,len(p)):
		p[0].append(p[i])

def p_call(p):
	'''call : function
			| command'''
	p[0]=["call"]
	for i in range(1,len(p)):
		p[0].append(p[i])

def p_command(p):
	'''command : VARIABLE call_args
			   | primary DOT VARIABLE call_args'''
	p[0]=["command"]
	for i in range(1,len(p)):
		p[0].append(p[i])

def p_function(p):
	'''function : VARIABLE LPARENTHESIS call_args RPARENTHESIS
				| primary DOT VARIABLE LPARENTHESIS call_args RPARENTHESIS
				| primary DOT VARIABLE
				| primary DOUBLECOLON VARIABLE'''
	p[0]=["function"]
	for i in range(1,len(p)):
		p[0].append(p[i])

def p_arg(p):
	'''arg : lhs EQUAL arg
		   | lhs op_asgn arg
		   | arg DOUBLEDOT arg
		   | arg PLUS arg
		   | arg MINUS arg
		   | arg MULTIPLY arg
		   | arg DIVIDE arg
		   | arg REMAINDER arg
		   | arg EXPONENT arg
		   | PLUS arg
		   | MINUS arg
		   | arg BINARY_OR arg
		   | arg BINARY_XOR arg
		   | arg BINARY_AND arg
		   | arg COMPARISON arg
		   | arg GREATER_THAN arg
		   | arg GREATER_THAN_EQ arg
		   | arg LESS_THAN arg
		   | arg LESS_THAN_EQ arg
		   | arg EQUALS arg
		   | arg NOT_EQUALS arg
		   | arg LOGICAL_NOT arg
		   | arg BINARY_LSHIFT arg
		   | arg BINARY_RSHIFT arg
		   | arg LOGICAL_AND arg
		   | arg LOGICAL_OR arg
		   | primary'''
	p[0]=["arg"]
	for i in range(1,len(p)):
		p[0].append(p[i])

def p_opt_elsifstmt(p):
	'''opt_elsifstmt : ELSIF expr then compstmt opt_elsifstmt
					 | none'''
	p[0]=["opt_elsifstmt"]
	for i in range(1,len(p)):
		p[0].append(p[i])

def p_opt_elsestmt(p):
	'''opt_elsestmt : ELSE compstmt
					| none'''
	p[0]=["opt_elsestmt"]
	for i in range(1,len(p)):
		p[0].append(p[i])

def p_primary(p):
	'''primary : LPARENTHESIS compstmt RPARENTHESIS
				 | VARIABLE
				 | literal
				 | primary LBRACKET opt_args RBRACKET
				 | LBRACKET opt_args RBRACKET
				 | LCBRACKET opt_args RCBRACKET
				 | RETURN 
				 | RETURN LPARENTHESIS call_args RPARENTHESIS
				 | function
				 | IF expr then compstmt opt_elsifstmt opt_elsestmt END
				 | UNLESS expr then compstmt opt_elsestmt END
				 | WHILE expr do compstmt END
				 | UNTIL expr do compstmt END
				 | CASE compstmt WHEN when_args then compstmt opt_when_args opt_elsestmt END
				 | FOR block_var IN expr DO compstmt END
				 | BEGIN compstmt END
				 | CLASS VARIABLE compstmt END
				 | DEF fname argdecl compstmt END'''
	p[0]=["primary"]
	for i in range(1,len(p)):
		p[0].append(p[i])


def p_opt_when_args(p):
	'''opt_when_args  : WHEN when_args then compstmt opt_when_args
					  | none'''
	p[0]=["opt_when_args"]
	for i in range(1,len(p)):
		p[0].append(p[i])

def p_opt_argstuff(p):
	'''opt_argstuff : COMMA MULTIPLY arg
					| none'''
	p[0]=["opt_argstuff"]
	for i in range(1,len(p)):
		p[0].append(p[i])

def p_when_args(p):
	'''when_args : args opt_argstuff
				 | MULTIPLY arg'''
	p[0]=["when_args"]
	for i in range(1,len(p)):
		p[0].append(p[i])

def p_then(p):
	'''then : terminals
	        | THEN
	        | terminals THEN'''
	p[0]=["then"]
	for i in range(1,len(p)):
		p[0].append(p[i])

def p_do(p):
	'''do : terminals
	        | DO
	        | terminals DO'''
	p[0]=["do"]
	for i in range(1,len(p)):
		p[0].append(p[i])

def p_block_var(p):
	'''block_var : mlhs'''
	p[0]=["block_var"]
	for i in range(1,len(p)):
		p[0].append(p[i])
#########################################
def p_opt_mlhs(p):
	'''opt_mlhs : COMMA mlhs_item opt_mlhs
				| none'''
	p[0]=["opt_mlhs"]
	for i in range(1,len(p)):
		p[0].append(p[i])

def p_mlhs(p):
	'''mlhs : mlhs_item opt_mlhs'''
	p[0]=["mlhs"]
	for i in range(1,len(p)):
		p[0].append(p[i])

#########################################


def p_mlhs_item(p):
	'''mlhs_item : lhs'''
	p[0]=["mlhs_item"]
	for i in range(1,len(p)):
		p[0].append(p[i])

def p_lhs(p):
	'''lhs : VARIABLE
	       | primary DOT VARIABLE
	       | NIL'''
	p[0]=["lhs"]
	for i in range(1,len(p)):
		p[0].append(p[i])

def p_mrhs(p):
	'''mrhs : args opt_argstuff
			| MULTIPLY arg'''
	p[0]=["mrhs"]
	for i in range(1,len(p)):
		p[0].append(p[i])

def p_opt_call_args(p):
	'''opt_call_args : call_args
					 | none'''
	p[0]=["opt_call_args"]
	for i in (1,len(p)):
		p[0].append(p[i])

# def p_opt_bcall_args(p):
# 	'''opt_bcall_args : LPARENTHESIS call_args RPARENTHESIS
# 					  | none'''
# 	p[0]=["opt_bacll_args"]
# 	for i in range(1,len(p)):
# 		p[0].append(p[i])

def p_opt_argstuff2(p):
	'''opt_argstuff2 : COMMA BINARY_AND arg
	                | none'''
	p[0]=["opt_argstuff2"]
	for i in range(1,len(p)):
		p[0].append(p[i])

def p_call_args(p):
	'''call_args : args
				 | args opt_argstuff opt_argstuff2
				 | MULTIPLY arg opt_argstuff2
				 | BINARY_AND arg
				 | call_args'''
	p[0]=["call_args"]
	for i in range(1,len(p)):
		p[0].append(p[i])



def p_opt_args(p):
	'''opt_args : args
	            | none'''
	p[0]=["opt_args"]
	for i in range(1,len(p)):
		p[0].append(p[i])


def p_args(p):
	'''args : arg
			| arg COMMA args'''
	p[0]=["args"]
	for i in range(1,len(p)):
		p[0].append(p[i])

def p_argdecl(p):
	'''argdecl : LPARENTHESIS arglist RPARENTHESIS
			   | arglist terminals'''
	p[0]=["argdecl"]
	for i in range(1,len(p)):
		p[0].append(p[i])

def p_opt_variables(p):
	'''opt_variables : COMMA VARIABLE opt_variables
			   | COMMA MULTIPLY VARIABLE opt_variables
			   | COMMA BINARY_AND VARIABLE opt_variables
			   | none'''
	p[0]=["opt_variables"]
	for i in range(1,len(p)):
		p[0].append(p[i])

def p_arglist(p):
	'''arglist : VARIABLE opt_variables
			   | MULTIPLY VARIABLE opt_variables
			   | BINARY_AND VARIABLE opt_variables'''
	p[0]=["arglist"]
	for i in range(1,len(p)):
		p[0].append(p[i])


# def p_variable(p):
# 	'''variable : varname'''
# 	p[0]=["variable"]
# 	for i in range(1,len(p)):
# 		p[0].append(p[i])

def p_literal(p):
	'''literal : INTNUMBER
			   | FLOATNUMBER
			   | STRING'''
	p[0]=["literal"]
	for i in range(1,len(p)):
		p[0].append(p[i])

def p_op_asgn(p):
	'''op_asgn : PLUS_EQ
			   | MINUS_EQ
			   | MULTIPLY_EQ
			   | DIVIDE_EQ
	           | REMAINDER_EQ
               | EXPONENT_EQ
               | BINARY_OR_EQ
               | BINARY_XOR_EQ
               | BINARY_AND_EQ
               | BINARY_LSHIFT_EQ
               | BINARY_RSHIFT_EQ
               | LOGICAL_AND_EQ
               | LOGICAL_OR_EQ'''
	p[0]=["op_asgn"]
	for i in range(1,len(p)):
		p[0].append(p[i])

def p_fname(p):
	'''fname : VARIABLE'''
	p[0]=["fname"]
	for i in range(1,len(p)):
		p[0].append(p[i])

# def p_operation(p):
# 	'''operation : VARIABLE'''
# 	p[0]=["operation"]
# 	for i in range(1,len(p)):
# 		p[0].append(p[i])

# def p_varname(p):
# 	'''varname : global
# 			   | VARIABLE'''
# 	p[0]=["varname"]
# 	for i in range(1,len(p)):
# 		p[0].append(p[i])

def p_global(p):
	'''global : DOLLAR_VARIABLE'''
	p[0]=["global"]
	for i in range(1,len(p)):
		p[0].append(p[i])

def p_none(p):
	'''none :
	'''
	p[0]=["none"]


def p_terminals(p):
	'''terminals : SEMICOLON
				 | NEWLINE'''
	p[0]=["terminals"]
	for i in range(1,len(p)):
		p[0].append(p[i])

def p_opt_terminals(p):
	'''opt_terminals : terminals
					 | none'''
	p[0]=["opt_terminals"]
	for i in range(1,len(p)):
		p[0].append(p[i])
		 


# def p_error(p):
# 	print "Syntax error in input!"

yacc.yacc()

data = ""
with open(filename,'r') as myfile:
	for line in myfile.readlines():
		if line!='\n':
			data = data + line
print "check"
print data
print "check"
result = yacc.parse(data)

# for item in result:
# 	for item1 in item:
# 		print item1
# 		print "\n"
# 	print "\n"
# printRightDeriv(result)
print result