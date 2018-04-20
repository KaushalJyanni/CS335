#!/usr/bin/python2
import ply.yacc as yacc
import sys
from lexer import tokens
import types
import sym_table
body =""
filename = sys.argv[1]

def type(a):
	try:
		float(a)
		try:
			int(a)
			if(int(a)==float(a)):
				return 'int'
			else:
				return 'float'
		except:
			return 'float'
	except:
		return 'string'

relop={
	"<=":'leq',
	"<":'lt',
	">=":'geq',
	">":'gt',
	"==":'eq',
	"!=":'neq'
}
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
temps=0
labels=0
elabels=0
alabels=0
argno = 0
switchtemp="stemp"
slabel=0
class_m=0
class_n=None
classlist={}
classinstances={}
def newtemp(st,typeof):
    global temps
    temps = temps + 1
    name = "temp"+str(temps)+"_"+str(curr_scope)
    st.insert(name, typeof)
    return name

def newlabel():
    global labels
    labels = labels + 1
    name = "label"+str(labels)
    return name

def elselabel():
    global elabels
    name = "elselabel"+str(elabels)
    elabels = elabels + 1
    return name

def afterlabel():
    global alabels
    name = "afterlabel"+str(alabels)
    alabels = alabels + 1
    return name

def getelabel():
	global elabels
	name = "elselabel"+str(elabels)
	return name

def getalabel():
	global alabels
	name = "afterlabel"+str(alabels)
	return name

allscopes={}
total_scopes=0
curr_scope=0
scope_stack=[]
scope_stack_copy=[]
scope_stack.append(curr_scope)
allscopes[curr_scope]=sym_table.Symtable()

def newscope(name=None):
	global allscopes
	global curr_scope
	global total_scopes
	total_scopes=total_scopes+1
	parent=curr_scope
	curr_scope = total_scopes
	scope_stack.append(curr_scope)	
	allscopes[curr_scope]=sym_table.Symtable(name)
	allscopes[curr_scope].parent=parent
	allscopes[parent].children.append(curr_scope)
	#print "incremented curr_scope to ", curr_scope

def delscope():
	#print "deleting scope"
	global curr_scope
	scope_stack.pop()
	curr_scope=scope_stack[-1]

def global_lookup(var):
	# print "type yo",type(var)
	for sc in reversed(scope_stack):
		for key in allscopes[sc].table.keys():
			if ((key.startswith(str(var)+"_") and not key.endswith("class")) or key==var):
				return key
		# if var in allscopes[sc].table.keys():
	return None

def global_gettype(var):
	for sc in reversed(scope_stack):
		for key in allscopes[sc].table.keys():
			if key.startswith(str(var)+"_") or key==var:
				return allscopes[sc].table[key]["type"]
	return None

def printfinal(node):
	# print
	# print
	# print ''.join(node.code+["return"])
	print ''.join(node.code)
	# print "return"
	# print
	# global total_scopes
	# print "total",total_scopes+1
	for curr_scope in range(0,total_scopes+1):
		print curr_scope
		print allscopes[curr_scope].table
		print
	# print classlist
	# print classinstances

class Node:
	def __init__(self):
		self.type=""
		self.code=[]
		self.place=""
		self.place2=""
		self.label=""
		# self.next=None



def p_program(p):
	'''program : compstmt'''
	p[0] = p[1]
	#print "final code"
	printfinal(p[0])

def p_compstmt(p):
	'''compstmt : stmts opt_terminals'''
	p[0] = p[1]
	#print "check:comp ", p[0]
	if(p[2]!=None):
		p[0].code += p[2].code

def p_stmts(p):
	'''stmts : stmts terminals expr
			 | stmt'''
	
	if(len(p)==4):
		p[0]=p[1]
		# #print "checks of error",p[0].code, p[2].code, p[3].code 
		# #print "yo check this shit out"
		# #print p[1].code
		# #print p[2].code
		# #print p[3].code
		# p[0].code=[p[0].code]
		p[0].code += p[2].code + p[3].code
	else:
		p[0]=p[1]
	# #print "check: stmts", p[0]

def p_stmt(p):
	'''stmt : expr
			| call DO compstmt END
			| stmt IF expr
			| stmt WHILE expr
			| stmt UNLESS expr
			| stmt UNTIL expr
			| BEGIN LCBRACKET compstmt RBRACKET
			| END LCBRACKET compstmt RBRACKET
			| lhs EQUAL command
			| lhs EQUAL command do compstmt END
			| nfunction
			| main'''
	if(len(p)==2):
		p[0]=p[1]

def p_main(p):
	'''main : MAIN'''
	p[0]=Node()
	p[0].code=["MAIN\n"]	

def p_expr(p):
	'''expr : mlhs EQUAL mrhs
			| RETURN call_args
			| expr AND expr
			| expr OR expr
			| NOT expr
			| command
			| LOGICAL_NOT command
			| nfunction
			| args
			| main'''
	if(len(p)==2):
		p[0]=p[1]
	elif(p[1]=="return"):
		#print "did return"
		p[0]=Node()
		if(p[2].code):
			p[0].code += "retint"
			p[0].code+=[", "]
			p[0].code += p[2].code+["\n"]
		else:
			p[0].code += "retvoid \n"

def p_call(p):
	'''call : function
			| command'''
	p[0]=p[1]

def p_command(p):
	'''command : primary DOT variable call_args'''
	p[0]=["command"]
	for i in range(1,len(p)):
		p[0].append(p[i])
 	
def p_nfunction(p):
	'''nfunction : variable LPARENTHESIS fcall_args RPARENTHESIS
				| primary DOT variable LPARENTHESIS fcall_args RPARENTHESIS
				| primary DOT variable
				| primary DOUBLECOLON variable'''
	if(len(p)==5):
		p[0]=Node()
		if(not p[1].place.endswith("class")):
			p[1].place=p[1].place.split("_")[0]
		p[0].code += p[3].code
		p[0].place = p[1].place
		if(p[1].place.startswith("print")):
			# print "yes found print"
			p[0].code += ["print\n"]
		else:
			p[0].code += ["callvoid, ",p[1].place+"\n"]
		p[0].type = "function"
	elif(len(p)==4):
		p[0]=Node()
		if(not p[3].place.endswith("class")):
			p[3].place=p[3].place.split("_")[0]+"_class"
		p[0].place=p[1].place+"_"+p[3].place
	elif(len(p)==7):
		p[0]=Node()
		if(not p[3].place.endswith("class")):
			p[3].place=p[3].place.split("_")[0]+"_class"
		p[0].code += p[5].code
		p[0].code += ["callvoid, ",p[1].place+"\n"]
		p[0].place = p[1].place+"_"+p[3].place
		p[0].type = "function"

def p_function(p):
	'''function : variable LPARENTHESIS fcall_args RPARENTHESIS
				| primary DOT variable LPARENTHESIS fcall_args RPARENTHESIS
				| primary DOT variable
				| primary DOUBLECOLON variable'''
	if(len(p)==5):
		p[0]=Node()
		if(not p[1].place.endswith("class")):
			p[1].place=p[1].place.split("_")[0]
		p[0].code += p[3].code
		p[0].place = p[1].place
		if(p[1].place.startswith("print")):
			# print "yes found print"
			p[0].code += ["print\n"]
		p[0].type = "function"
	elif(len(p)==4):
		p[0]=Node()
		if(not p[3].place.endswith("class")):
			p[3].place=p[3].place.split("_")[0]+"_class"
		p[0].place=p[1].place+"_"+p[3].place
	elif(len(p)==7):
		p[0]=Node()
		if(not p[3].place.endswith("class")):
			p[3].place=p[3].place.split("_")[0]+"_class"
		p[0].code += p[5].code
		# p[0].place = p[1].place+"_"+p[3].place
		p[0].place = p[3].place
		p[0].type = "function"

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
		   | arg BINARY_OR arg
		   | arg BINARY_XOR arg
		   | arg BINARY_AND arg
		   | arg COMPARISON arg
		   | arg GREATER_THAN arg
		   | arg GREATER_THAN_EQ arg
		   | arg LESS_THAN arg
		   | NOT arg
		   | arg LESS_THAN_EQ arg
		   | arg EQUALS arg
		   | arg NOT_EQUALS arg
		   | arg LOGICAL_NOT arg
		   | arg BINARY_LSHIFT arg
		   | arg BINARY_RSHIFT arg
		   | arg LOGICAL_AND arg
		   | arg LOGICAL_OR arg
		   | NEWCLASS variable 
		   | ARRAY DOT NEW LPARENTHESIS variable RPARENTHESIS
		   | ARRAY DOT NEW LPARENTHESIS INTNUMBER RPARENTHESIS
		   | variable LBRACKET variable RBRACKET
	       | variable LBRACKET INTNUMBER RBRACKET
		   | primary'''
	checkcount=1
	# #print checkcount
	checkcount += 1
	global curr_scope
	if(len(p)==4):
		if(p[2]==".."):
			#print "doule dot niggers *******************8"
			p[0]=Node()
			p[0].place=p[1].place
			p[0].place2=p[3].place
			p[0].type=p[1].type
			#print "from double dot",p[0]
		elif(p[2] in ['+','-','/','*','%','^','|','<<','>>','&','&&','||',"<=","<",">=",">","==","!="]):
			#print "latest check,",p[1],p[1].code,p[1].type,p[1].place
			if(p[1].type):
				if(global_gettype(p[1].place)):
					# print p[1].place,"check"
					temp = newtemp(allscopes[curr_scope], global_gettype(p[1].place))
				else:
					# print p[1].place,"check"
					temp = newtemp(allscopes[curr_scope], p[1].type)
				# print "my type is",temp,p[1].type
			else:
				# print p[1].place,"check"
				temp = newtemp(allscopes[curr_scope], global_gettype(p[1].place))	
			# #print "check arg p1 ",p[1].code
			# #print "check arg p3 ",p[3].code	
			p[0]=Node()
			p[0].code = p[1].code + p[3].code
			p[0].place = temp
			p[0].type=p[1].type
			#print "checking ", p[3].place
			if(p[3].type=="variable" and (not global_lookup(p[3].place))):
				print "error. variable, "+ p[3].place +" value not assigned before"
				sys.exit()
			#print "checking ", p[1].place
			if(p[1].type=="variable" and (not global_lookup(p[1].place))):
				print allscopes[curr_scope].table
				print "error. variable, "+ p[1].place +" value not assigned before"
				sys.exit()
			if(global_gettype(p[1].place)):
				# print global_gettype(p[1].place),global_gettype(p[3].place)
				if(global_gettype(p[1].place)=="class" or global_gettype(p[3].place)=="class"):
					print "type mismatch for ",p[1].place,p[3].place#,global_gettype(p[1].place),"and1",global_gettype(p[3].place)
					sys.exit()
			else:
				# print p[1].type,p[3].type 
				if(p[1].type=="class" or p[3].type=="class"):
					print "type mismatch for ",p[1].place,p[3].place#,p[1].type,"and2",p[3].type
					sys.exit()
			if(p[2] in ["<=","<",">=",">","==","!="]):
				# #print "did the big stuff"
				lab1 = newlabel()
				lab2 = newlabel()
				p[0].code += ["ifgoto, ",relop[p[2]]+", "+p[1].place+", "+p[3].place+", "+lab1+" \n"]
				p[0].code += ["=, "+p[0].place+", 0 \n"]
				p[0].code += ["goto, "+lab2+" \n"]
				p[0].code += ["label, "+lab1+"\n"]
				p[0].code += ["=, "+p[0].place+", 1 \n"]
				p[0].code += ["label, "+lab2+"\n"]
			else:
				p[0].code += [p[2]+", "+p[0].place+", "+p[1].place+", "+p[3].place+" \n"]
		elif(p[2]=='='):
			p[0]=Node()				
			if(p[3].type=="class"):
				if(not p[3].place.endswith("class")):
					p[3].place=p[3].place.split("_")[0]
				p[0].code=["newclass,",p[1].place,","+p[3].place+"\n"]
				classinstances[p[1].place]=p[3].place
				p[0].type="class"
			elif(p[3].type=="array"):
				p[1].type="array"
				p[0].code = p[1].code
				p[0].code = ["array, "+p[1].place+"\n"]
				p[0].type = p[3].type
				if(not allscopes[curr_scope].lookup(p[1])):
					#print "type insertion is", p[3].type, "for ",p[1].place
					allscopes[curr_scope].insert(p[1].place,p[3].type)
			else:
				#print "updating type of",p[1].place,p[3].type
				# if(p[3].type):
				p[1].type = p[3].type

				try:
					float(p[3].place)
					if(not p[1].place.endswith("class")):
						if("_" in p[0]):
							p[1].place=p[1].place.split("_")[0]+"_"+str(curr_scope)
					# print "success nigger"
				except:
					#print "checking",p[3].place
					if(p[3].type == "variable" and (not global_lookup(p[3].place))):
						print "error. variable, "+ p[3].place +" value not assigned before"
						sys.exit()
				# #print "check arg p1 ",p[1].code
				# #print "check arg p3 ",p[3].code
				# #print "concatenating", ''.join([p[2]]+[", "]+[p[1].place]+[", "]+[p[3].place])
				p[0].code = p[1].code + p[3].code
				if(p[3].type=="function"):
					p[0].code += ["callint, "+p[1].place+", "+p[3].place+" \n"]	
					p[0].type = "int"
				else:
					p[0].code += ["=, "+p[1].place+", "+p[3].place+" \n"]
					p[0].type = p[3].type
				if(not allscopes[curr_scope].lookup(p[1])):
					# print "type insertion is", p[3].type, "for ",p[1].place
					allscopes[curr_scope].insert(p[1].place,"int")
	elif(len(p)==2):
		#print "---------------------",p[1]
		p[0] = p[1]
		#print "type of arg", p[0].place, p[0].type
	elif(p[1]=="newclass"):
		p[0]=Node()
		p[0].place=p[2].place
		p[0].type="class"
	elif(len(p)==3):
		temp = newtemp(allscopes[curr_scope],"bool")
		p[0]=Node()
		p[0].place=temp
		if(not global_lookup(p[2].place)):
				print "error. variable, "+ p[2].place +" value not assigned before"
				sys.exit()
		p[0].code += ["not, "+p[0].place+", "+p[2].place+" \n"]
		p[0].type = "bool"
	elif(p[1]=="array"):
		p[0]=Node()
		p[0].type="array"
		try:
			float(p[5])
			p[0].code = [str(p[5])]
		except:
			p[0].code = [p[5].place]
	elif(len(p)==5):
		p[0]=Node()
		p[0].type="pointer"
		try:
			int(p[3])
			t=newtemp(allscopes[curr_scope],"pointer")
			p[0].code += ["+, "+t+", "+p[1].place+", "+p[3]+" \n"]
			p[0].code += ["*, "+t+" \n"]
			p[0].place=t
		except:
			t=newtemp(allscopes[curr_scope],"pointer")
			p[0].code += ["+, "+t+", "+p[1].place+", "+p[3].place+"\n"]
			p[0].code += ["*, "+t+"\n"]
			p[0].place=t

	# #print "check: arg", ''.join(p[0].code)

def p_opt_elsifstmt(p):
	'''opt_elsifstmt : ELSIF expr then nscope compstmt escope opt_elsifstmt
					 | none'''
	if(len(p)==8):
		lab1=newlabel()
		p[0]=Node()
		p[0].label=lab1
		p[0].code += ["label, "+p[0].label,"\n"]
		p[0].code += p[2].code
		p[0].type="elifcode"
		if(p[7]):
			p[0].code += ["ifgoto, eq, "+ p[2].place+ ", 0, "+p[7].label+" \n"]
		else:
			p[0].code += ["ifgoto, eq, "+ p[2].place+ ", 0, "+getelabel()+" \n"]
		p[0].code += p[5].code
		p[0].code += ["goto, "+getalabel()+"\n"]
		if(p[7]):
			p[0].code += p[7].code
		#print "check from elsif:",p[0].code
	else:
		p[0]=None



def p_opt_elsestmt(p):
	'''opt_elsestmt : ELSE nscope compstmt escope
					| none'''
	if(len(p)==5):	
		p[0]=p[3]
		#print "check from else: ",p[0].code


def p_nscope(p):
	'''nscope : '''
	newscope()
	#print "started new scope"

def p_escope(p):
	'''escope : '''
	#print "end new scope"
	delscope()

def p_nfscope(p):
	'''nfscope : none'''
	global scope_stack_copy
	global scope_stack
	#print "started new function scope"
	#print scope_stack
	scope_stack_copy = scope_stack
	scope_stack=[]
	p[0]=p[1]
	newscope(p[-1])

def p_efscope(p):
	'''efscope : none'''
	global scope_stack_copy
	global scope_stack
	global curr_scope
	scope_stack=scope_stack_copy
	scope_stack_copy=[]
	#print "end new fu*nction scope"
	#print scope_stack
	p[0]=p[1]
	curr_scope=scope_stack[-1]
	# delscope()

def p_cstart(p):
	'''cstart : '''
	global class_m
	global class_n
	class_m=1
	class_n=p[-1].place.split("_")[0]
	classlist[class_n]=[]
	# print "set class_m to 1"

def p_endclass(p):
	'''endclass : ENDCLASS'''
	global class_m
	global class_n
	class_n=None
	class_m=0
	# print "set class_m to 0"

def p_primary(p):
	'''primary : LPARENTHESIS compstmt RPARENTHESIS
				 | variable
				 | literal
				 | primary LBRACKET opt_args RBRACKET
				 | LBRACKET opt_args RBRACKET
				 | LCBRACKET opt_args RCBRACKET
				 | RETURN 
				 | RETURN LPARENTHESIS call_args RPARENTHESIS
				 | function
				 | IF expr then nscope compstmt escope opt_elsifstmt opt_elsestmt  END
				 | UNLESS expr then compstmt opt_elsestmt END
				 | WHILE expr do compstmt END
				 | UNTIL expr do compstmt END
				 | CASE compstmt WHEN when_args then compstmt opt_when_args opt_elsestmt END
				 | nscope FOR block_var IN expr do compstmt escope END
				 | BEGIN compstmt END
				 | CLASS variable cstart terminals compstmt endclass
				 | DEF fname nfscope argdecl compstmt efscope END'''
	global curr_scope
	if(p[1]=="class"):
		p[0]=Node()
		p[0].type="class"
		p[2].place=p[2].place.split("_")[0]
		allscopes[curr_scope].insert(p[2].place,'class')
		p[0].code=["class, "+p[2].place+"\n"]
		p[0].code+=p[5].code
		p[0].code+=["endclass\n"]
	elif(len(p)==2):
		if(p[1]!='return'):
			#print p[1]
			p[0]=p[1]
			p[0].place = p[1].place
			p[0].type = p[1].type
			#print "typye in primary of ",p[0].place, p[0].type
		else:
			p[0]=Node()
			p[0].code=["retvoid\n"]
	elif(p[1]=="while"):
		lab1 = newlabel()
		lab2 = newlabel()
		p[0]=Node()
		p[0].code += ["label, "+lab1+" \n"]
		p[0].code += p[2].code
		p[0].code += ["ifgoto, eq, "+ p[2].place+ ", 0, "+lab2+" \n"]
		p[0].code += p[4].code
		p[0].code += ["goto, "+lab1+"\n"]
		p[0].code += ["label, "+lab2+" \n"]
		p[0].type="while"
	elif(p[1]=="if"):
		alabel=afterlabel()
		elabel=elselabel()
		p[0]=Node()
		p[0].code += p[2].code
		if(p[7]):
			p[0].code += ["ifgoto, eq, "+ p[2].place+ ", 0, "+p[7].label+" \n"]
		else:
			p[0].code += ["ifgoto, eq, "+ p[2].place+ ", 0, "+elabel+" \n"]
		p[0].code += p[5].code
		p[0].code += ["goto, "+alabel+"\n"]
		if(p[7]):
			p[0].code += p[7].code
		p[0].code += ["label, "+elabel+" \n"]
		if(p[8]):
			p[0].code += p[8].code
		p[0].code += ["label, "+alabel+" \n"]
	elif(p[2]=="for"):
		lab1 = newlabel()
		p[0]=Node()
		# #print "inserted ",p[3].place
		# #print "&&&&& currscope is", curr_scope
		# x=global_lookup(p[3].place)
		# x["type"]=p[5].type
		try:
			float(p[5].place)
		except:
			if(not global_lookup(p[5].place)):
				print "error. variable, "+ p[5].place +" value not assigned before"
				sys.exit()
		p[0].code += ["=, "+p[3].place+", "+p[5].place+" \n"]
		p[0].code += ["label, "+lab1+"\n"]
		p[0].code += p[7].code
		p[0].code += ["+, ",p[3].place+", "+p[3].place+", 1\n"]
		p[0].code += ["ifgoto, leq, "+ p[3].place+ ", "+p[5].place2+", "+lab1+" \n"]
		p[0].type="for"
	elif(p[1]=="("):
		p[0]=p[2]
	elif(p[1]=="def"):
		p[0]=Node()
		p[0].code += ["label, "+p[2].place+"\n"]
		if(p[4]):
			p[0].code += p[4].code
		p[0].code += p[5].code
	elif(p[1]=="case"):
		p[0]=Node()
		# temp=newtemp(allscopes[curr_scope],"case")
		# global switchtemp
		global slabel
		slabel = slabel + 1
		# switchtemp=temp
		p[0].code=p[2].code
		p[0].code+=["=, "+switchtemp+","+p[2].place+"\n"]
		# p[0].code+=p[4].code
		#print "fuckkk"
		#print p[2].place
		p[0].code+=["ifgoto, neq, "+switchtemp+", "+p[4].place+", s"+str(slabel)+"\n"]
		p[0].code+=p[6].code
		p[0].code+="goto, safter \n"
		p[0].code+=["label, s"+str(slabel)+"\n"]
		p[0].code+=p[7].code
		p[0].code+=["label, safter\n"]


def p_opt_when_args(p):
	'''opt_when_args  : WHEN when_args then compstmt opt_when_args
					  | none'''
	p[0]=Node()
	global slabel
	#print "slabel is",slabel
	global switchtemp
	# p[0].code = ["label, s"+str(slabel)+"\n"]
	slabel = slabel + 1
	if(len(p)==6):
		# p[0].code+=p[2].code
		# if(p[5].code!=[]):
		p[0].code+=["ifgoto, neq, "+switchtemp+", "+p[2].place+", s"+str(slabel)+"\n"]
		# else:
		# 	p[0].code+=["ifgoto, neq, "+switchtemp+", "+p[2].place+", s0"+"\n"]
		p[0].code+=p[4].code
		p[0].code+=["label, s"+str(slabel)+"\n"]
		p[0].code+="goto, safter\n"
		p[0].code+=p[5].code
	# else:
	# 	slabel=0

def p_opt_argstuff(p):
	'''opt_argstuff : COMMA args opt_argstuff
					| none'''
	p[0]=["opt_argstuff"]
	for i in range(1,len(p)):
		p[0].append(p[i])

def p_when_args(p):
	'''when_args : arg
				 | arg COMMA when_args'''
	if(len(p)==2):
		p[0]=p[1]
		#print "yoloyo",p[0].place
		p[0].code = p[1].place
	else:
		p[0]=Node()
		# print p[3].code
		p[0].code = [p[1].place+", "]+list(p[3].code)

def p_then(p):
	'''then : terminals
	        | THEN
	        | THEN terminals'''
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
	#print "yuio",p[-1]
	allscopes[curr_scope].insert(p[1].place,'int')
	p[0]=p[1]
#########################################
def p_opt_mlhs(p):
	'''opt_mlhs : COMMA mlhs_item opt_mlhs
				| none'''
	if(len(p)==4):
		p[0]=Node()
		p[0].code = [", "+p[2].code+p[3].code]
	else:
		p[0]=p[1]

def p_mlhs(p):
	'''mlhs : mlhs_item opt_mlhs'''
	p[0]=p[1]
	if(p[2]):
		p[0].code += p[2].code

#########################################


def p_mlhs_item(p):
	'''mlhs_item : lhs'''
	p[0]=p[1]

def p_lhs(p):
	'''lhs : variable
	       | primary DOT variable
	       | variable LBRACKET variable RBRACKET
	       | variable LBRACKET INTNUMBER RBRACKET
	       | NIL'''
	if(len(p)==2):
		p[0]=p[1]
		p[0].place = p[1].place
	elif(len(p)==5):
		p[0]=Node()
		try:
			int(p[3])
			t=newtemp(allscopes[curr_scope],"pointer")
			p[0].code += ["+, "+t+", "+p[1].place+", "+p[3]+" \n"]
			p[0].code += ["*, "+t+" \n"]
			p[0].place=t+"_"+str(curr_scope)
		except:
			t=newtemp(allscopes[curr_scope],"pointer")
			p[0].code += ["+, "+t+", "+p[1].place+", "+p[3].place+"\n"]
			p[0].code += ["*, "+t+"\n"]
			p[0].place=t+"_"+str(curr_scope)
	elif(len(p)==4):
		p[0]=Node()
		try:
			classinstances[p[1].place]
			pass
		except KeyError:
			print "no such class exists.", p[1].place,"\naborting"
			sys.exit()
		
		if(not p[3].place.endswith("class")):
			p[3].place=p[3].place.split("_")[0]+"_class"
		if p[3].place in classlist[classinstances[p[1].place]]:
			pass
		else:
			print "no such class member exists.", p[3].place,"\naborting"
			sys.exit()
		p[0].place=p[1].place+"_"+p[3].place
	# #print "check: lhs", p[0].code

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

# def p_opt_argstuff2(p):
# 	'''opt_argstuff2 : opt_argstuff2 COMMA BINARY_AND arg
# 	                | none'''
# 	p[0]=["opt_argstuff2"]
# 	for i in range(1,len(p)):
# 		p[0].append(p[i])

def p_call_args(p):
	'''call_args : call_args COMMA call_args
				 | MULTIPLY arg
				 | BINARY_AND arg
				 | arg
				 | command
				 | none'''
	p[0]=Node()
	if(p[1]!="*" and p[1]!="&"):
		if(len(p)==2):
			p[0].code += [p[1].place]
		else:
			p[0].code += p[1].code+[", "]+p[3].code

def p_fcall_args(p):
	'''fcall_args : fcall_args COMMA fcall_args
				 | MULTIPLY arg
				 | BINARY_AND arg
				 | arg
				 | command
				 | none'''
	p[0]=Node()
	if(p[1]!="*" and p[1]!="&"):
		if(len(p)==2 and p[1].place):
			p[0].code += ["push, "+p[1].place+"\n"]
		elif(len(p)==4):
			p[0].code += p[1].code+p[3].code	

def p_opt_args(p):
	'''opt_args : args
	            | none'''
	p[0]=p[1]


def p_args(p):
	'''args : arg
			| args COMMA arg'''
	if(len(p)==2):
		p[0]=p[1]

def p_argdecl(p):
	'''argdecl : LPARENTHESIS arglist RPARENTHESIS opt_terminals
			   | arglist terminals'''
	if(p[1]=='('):
		p[0]=p[2]

def p_opt_variables(p):
	'''opt_variables : COMMA variable opt_variables
			   | COMMA MULTIPLY variable opt_variables
			   | COMMA BINARY_AND variable opt_variables
			   | none'''
	global argno
	if(len(p)==4):
		argno += 1
		p[0]=p[2]
		p[0].code += ["load, arg"+str(argno)+", "+p[2].place+"\n"]
		if(p[3]):
			p[0].code += p[3].code
		allscopes[curr_scope].insert(p[2].place,"int")
	elif(len(p)==2):
		argno = 0

def p_arglist(p):
	'''arglist : variable opt_variables
			   | MULTIPLY variable opt_variables
			   | BINARY_AND variable opt_variables
			   | none'''
	if(len(p)==3):
		global argno
		argno += 1
		p[0]=p[1]
		p[0].code += ["load, arg"+str(argno)+", "+p[1].place+"\n"]
		if(p[2]):
			p[0].code += p[2].code
		allscopes[curr_scope].insert(p[1].place,"int")

def p_literal(p):
	'''literal : INTNUMBER
			   | FLOATNUMBER
			   | STRING'''
	p[0]=Node()
	p[0].place=p[1]
	#print "literal, ",p[1],"type ",type(p[1])
	p[0].type=type(p[1])
	if(p[0].type=="string"):
		#print "yess"
		p[0].place=str('\''+p[1]+'\'')

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
	'''fname : variable'''
	if(not p[1].place.endswith("class")):
		p[1].place=p[1].place.split("_")[0]
	# else:
	# 	p[1].place=class_n+"_"+p[1].place
	p[0] = p[1]
# def p_operation(p):
# 	'''operation : variable'''
# 	p[0]=["operation"]
# 	for i in range(1,len(p)):
# 		p[0].append(p[i])

# def p_varname(p):
# 	'''varname : global
# 			   | variable'''
# 	p[0]=["varname"]
# 	for i in range(1,len(p)):
# 		p[0].append(p[i])

def p_variable(p):
	'''variable : VARIABLE
			    | DOLLAR VARIABLE'''
	if(len(p)==2):
		p[0]=Node()
		# print 'found var'
		global class_m
		global class_n
		# print "class name",class_n
		# print class_m
		# if(p[-1]=="class"):
			# classlist[class_n]=[]
			# print "class started"
		if(not class_m):
			if(global_lookup(p[1])):
				if(global_gettype(p[1])=="class" and p[-1]!="newclass"):
					print "variable name, "+p[1]+" cant be same as class name. aborting"
					sys.exit()
				p[0].place=str(global_lookup(p[1]))
				# print "rturn ",p[0].place
			else:
				if(global_gettype(p[1])=="class" and p[-1]!="newclass"):
					print "variable name, "+p[1]+" cant be same as class name. aborting"
					sys.exit()
				p[0].place=p[1]+"_"+str(curr_scope)
				# print "rturn ",p[0].place
		else:
			p[0].place=p[1]+"_class"
			if(class_n):
				classlist[class_n].append(p[0].place)
			# print "yuio",p[0].place
		p[0].type="variable"
		if(global_lookup(p[1])):
			#print "found type of", p[1]
			p[0].type=global_gettype(p[1])
	else:
		p[0]=Node()
		p[0].place=str(p[1])+str(p[2])
		p[0].type="variable"
		if(global_lookup(p[2])):
			p[0].type=global_gettype(p[2])
	# #print "type of from variabl",p[0].place,p[0].type
	

def p_none(p):
	'''none :'''
	p[0]=Node()

def p_terminals(p):
	'''terminals : SEMICOLON
				 | NEWLINE'''
	p[0]=Node()
	p[0].place="newline"

def p_opt_terminals(p):
	'''opt_terminals : terminals
					 | none'''
	p[0] = p[1]
		 
# def p_error(p):
# 	#print "Syntax error"

yacc.yacc()

data = ""
with open(filename,'r') as myfile:
	for line in myfile.readlines():
		if line!='\n':
			data = data + line

result = yacc.parse(data)
# #print
# #printRightDeriv(result)
