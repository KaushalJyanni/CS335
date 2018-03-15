import ply.yacc as yacc
import sys
from lexer import tokens

def p_program(p):
	'''program : compstmt'''
	p[0]=["program",p[1]]

def p_terminals(p):
	'''terminals : SEMICOLON
				 | NEWLINE'''
	p[0]=["terminals"]
	for i in (1,len(p)):
		p[0].append(p[i])

def p_opt_terminals(p):
	'''opt_terminals : terminals
					 | none'''
	p[0]=["opt_terminals"]
	for i in (1,len(p)):
		p[0].append(p[i])

def p_compstmt(p):
	'''compstmt : stmt texpr opt_terminals'''
	p[0]=["compstmt"]
	for i in (1,len(p)):
		p[0].append(p[i])

def p_texpr(p):
	'''texpr : terminals expr texpr
			| none'''
	p[0]=["texpr"]
	for i in (1,len(p)):
		p[0].append(p[i])

def p_stmt(p):
	'''stmt : CALL do compstmt end
			| stmt IF expr
			| stmt WHILE expr
			| stmt UNLESS expr
			| stmt UNTIL expr
			| BEGIN LCBRACKET compstmt RCBRACKET
			| END LCBRACKET compstmt RCBACKET
			| lhs EQUAL command compstmt end
			| expr'''
	p[0]=["stmt"]
	for i in (1,len(p)):
		p[0].append(p[i])

def p_expr(p):
	'''expr : mlhs EQUAL mrhs
			| RETURN call_args
			| expr AND expr
			| expr OR expr
			| NOT expr
			| command
			| LOGICAL_NOT command
			| arg'''
	p[0]=["expr"]
	for i in (1,len(p)):
		p[0].append(p[i])

def p_call(p):
	'''call : function
			| command'''
	p[0]=["call"]
	for i in (1,len(p)):
		p[0].append(p[i])

def p_command(p):
	'''command : operation call_args
			   | primary DOT operation call_args'''
	p[0]=["command"]
	for i in (1,len(p)):
		p[0].append(p[i])

def p_function(p):
	'''function : operation opt_bcallargs
				| primary DOT operation LPARENTHESIS call_args RPARENTHESIS
				| primary DOT operation
				| primary DOUBLECOLON operation'''
	p[0]=["function"]
	for i in (1,len(p)):
		p[0].append(p[i])

def p_arg(p):
	'''arg : lhs EQUAL arg
		   | lhs op_asgn arg
		   | arg PLUS arg | arg MINUS arg | arg MULTIPLY arg | arg DIVIDE arg
		   | arg REMAINDER arg | arg EXPONENT arg
		   | PLUS arg | MINUS arg
		   | arg BINARY_OR arg | arg BINARY_XOR arg | arg BINARY_AND arg
		   | arg COMARISON arg | arg GREATER_THAN arg | arg GREATER_THAN_EQ arg
		   | arg LESS_THAN arg | arg LESS_THAN_EQ arg | arg EQUALS arg
		   | arg NOT_EQUALS arg | arg LOGICAL_NOT arg
		   | arg BINARY_LSHIFT arg | arg BINARY_RSHIFT arg
		   | arg LOGICAL_AND arg | arg LOGICAL_OR arg
		   | LOGICAL | VARIABLE | FUNCTION'''
	p[0]=["arg"]
	for i in (1,len(p)):
		p[0].append(p[i])

def p_primary(p):
	'''primary : | LPARENTHESIS compstmt RPARENTHESIS
				 | literal
				 | variable
				 | primary LBRACKET opt_args RBRACKET
				 | RETURN opt_bcall_args
				 | function
				 | IF expr then
				      compstmt
				   opt_elsifstmt
				   opt_elsestmt
				   END
				 | UNLESS expr then
				 	  compstmt
				   opt_elsestmt
				   END
				 | WHILE expr do compstmt END
				 | UNTIL expr do compstmt END
				 | CASE compstmt
				      WHEN when_args then compstmt
				      opt_whenargs
				   opt_elsestmt
				   END
				 | FOR black_var IN expr do
				 	  compstmt
				   END
				 | BEGIN
				 	  compstmt
				   END
				 | CLASS INDENTIFIER
				 	  compstmt
				   END
				 | DEF fname argdecl
				 	  compstmt
				   END'''
	p[0]=["primary"]
	for i in (1,len(p)):
		p[0].append(p[i])

def p_opt_bacll_args(p):
	'''opt_bacll_args : LPARENTHESIS call_args RPARENTHESIS
					  | none'''
	p[0]=["opt_bacll_args"]
	for i in (1,len(p)):
		p[0].append(p[i])

def p_opt_elsifstmt(p):
	'''opt_elsifstmt : ELSIF expr then
						  compstmt
					   opt_elsifstmt
					 | none'''
	p[0]=["opt_elsifstmt"]
	for i in (1,len(p)):
		p[0].append(p[i])

def p_opt_elsestmt(p):
	'''opt_elsestmt : ELSE compstmt
					| none'''
	p[0]=["opt_elsestmt"]
	for i in (1,len(p)):
		p[0].append(p[i])

def p_opt_args(p):
	'''opt_args : args
	            | none'''
	p[0]=["opt_args"]
	for i in (1,len(p)):
		p[0].append(p[i])

def p_opt_when_args(p):
	'''opt_when_args  : WHEN when_args then compstmt
						opt_when_args
					  | none'''
	p[0]=["opt_when_args"]
	for i in (1,len(p)):
		p[0].append(p[i])

def p_when_args(p):
	'''when_args : args opt_argstuff
				 | multiply arg'''
	p[0]=["when_args"]
	for i in (1,len(p)):
		p[0].append(p[i])

def p_opt_argstuff(p):
	'''opt_argstuff : COMMA
					| MULTIPLY
					| arg
	                | none'''
	p[0]=["opt_argstuff"]
	for i in (1,len(p)):
		p[0].append(p[i])

def p_then(p):
	'''then : terminals
	        | THEN
	        | terminals THEN'''
	p[0]=["then"]
	for i in (1,len(p)):
		p[0].append(p[i])

def p_do(p):
	'''do : terminals
	        | do
	        | terminals do'''
	p[0]=["do"]
	for i in (1,len(p)):
		p[0].append(p[i])

def p_block_var(p):
	'''block_var : lhs
				 | mlhs'''
	p[0]=["block_var"]
	for i in (1,len(p)):
		p[0].append(p[i])
#########################################
def p_mlhs(p):
	'''mlhs : mlhs_item opt_mlhs
			| MULTIPLY lhs'''
	p[0]=["mlhs"]
	for i in (1,len(p)):
		p[0].append(p[i])

def p_opt_mlhs(p):
	'''opt_mlhs : COMMA mlhs_item opt_mlhs
				| none'''
	p[0]=["opt_mlhs"]
	for i in (1,len(p)):
		p[0].append(p[i])
#########################################


def p_mlhs_item(p):
	'''mlhs_item : lhs
				 | LPARENTHESIS mlhs RPARENTHESIS'''
	p[0]=["mlhs_item"]
	for i in (1,len(p)):
		p[0].append(p[i])

def p_lhs(p):
	'''lhs : variable
	       | primary LBRACKET opt_args RBRACKET
	       | primary DOT idnetifier'''
	p[0]=["lhs"]
	for i in (1,len(p)):
		p[0].append(p[i])

def p_mrhs(p):
	'''mrhs : args opt_argstuff
			| MULTIPLY arg'''
	p[0]=["mrhs"]
	for i in (1,len(p)):
		p[0].append(p[i])

def p_call_args(p):
	'''call_args : args
				 | args opt_argstuff opt_argstuff2
				 | opt_argstuff2
				 | multiply arg opt_argstuff2
				 | BINARY_AND arg
				 | command'''
	p[0]=["call_args"]
	for i in (1,len(p)):
		p[0].append(p[i])

def p_opt_argstuff2(p):
	'''opt_argstuff : COMMA
					| BINARY_AND
					| arg
	                | none'''
	p[0]=["opt_argstuff2"]
	for i in (1,len(p)):
		p[0].append(p[i])

def p_args(p):
	'''args : '''
	p[0]=["args"]
	for i in (1,len(p)):
		p[0].append(p[i])

def p_argdecl(p):
	'''argdecl : LPARENTHESIS arglist RPARENTHESIS
			   | arglist terminals'''
	p[0]=["argdecl"]
	for i in (1,len(p)):
		p[0].append(p[i])

def p_variable(p):
	'''variable : varname
				| nil'''
	p[0]=["variable"]
	for i in (1,len(p)):
		p[0].append(p[i])

def p_literal(p):
	'''literal : numeric
			   | string'''
	p[0]=["literal"]
	for i in (1,len(p)):
		p[0].append(p[i])

def p_op_asgn(p):
	'''op_asgn : PLUS_EQPLUS_EQ
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
	for i in (1,len(p)):
		p[0].append(p[i])

def p_fname(p):
	'''fname : VARIABLE'''
	p[0]=["fname"]
	for i in (1,len(p)):
		p[0].append(p[i])

def p_operation(p):
	'''operation : VARIABLE'''
	p[0]=["operation"]
	for i in (1,len(p)):
		p[0].append(p[i])

def p_varname(p):
	'''varname : GLOBAL
			   | VARIABLE'''
	p[0]=["varname"]
	for i in (1,len(p)):
		p[0].append(p[i])

def p_global(p):
	'''global : DOLLAR_VARIABLE'''
	p[0]=["global"]
	for i in (1,len(p)):
		p[0].append(p[i])

def p_none(p):
	'''none : '''
	p[0]=["none"]
	for i in (1,len(p)):
		p[0].append(p[i])

yacc.yacc()

data = ""
with open(filename,'r') as myfile:
	for line in myfile.readlines():
		if line!='\n':
			data = data + line

result = yacc.parse(data)