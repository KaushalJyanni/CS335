from utils import *
class threeAddCode:
	instype=''
	operation=''
	src1=''
	src2=''
	target=''
	label=''

	def __init__(self,instruction):
		if(instruction[1] == '='):
			self.instype = 'assignment'
			self.operation = '='
			self.target = instruction[2]
			self.src1 = instruction[3]
		
		elif(instruction[1] in ['+','-','/','*','%']):
			self.instype = "arithmetic"
			self.operation = instruction[1]
			self.src1 = instruction[3]
			self.src2 = instruction[4]
			self.target = instruction[2]

		elif(instruction[1] in ['+=','-=','/=','*=','%=']):
			self.instype = "arithmetic"
			self.operation = instruction[1]
			self.src1 = instruction[2]
			self.src2 = instruction[3]
			self.target = instruction[2]

		elif(instruction[1] in ['^','|','<<','>>','&']):
			self.instype = "logical"
			self.operation = instruction[1]
			self.src1 = instruction[3]
			self.src2 = instruction[4]
			self.target = instruction[2]

		elif(instruction[1] in ['^=','|=','<<=','>>=','&=']):
			self.instype = "logical"
			self.operation = instruction[1]
			self.src1 = instruction[2]
			self.src2 = instruction[3]
			self.target = instruction[2]

		elif(instruction[1]== "ifgoto"):
			self.instype = "ifgoto"
			self.operation = instruction[2]
			self.src1 = instruction[3]
			self.src2 = instruction[4]
			self.target = instruction[5]

		elif(instruction[1] == "goto"):
			self.instype = "goto"
			self.target = instruction[2]

		elif(instruction[1] == "callvoid"):
			self.instype = "callvoid"
			self.target = instruction[2]
			functions.append(self.target)

		elif(instruction[1] == "retvoid"):
			self.instype = "retvoid"

		elif(instruction[1] == "callint"):
			self.instype = "callint"
			self.src1 = instruction[2] #return in this variable
			self.target = instruction[3]
			functions.append(self.target)

		elif(instruction[1] == "retint"):
			self.instype = "retint"
			self.target = instruction[2]

		elif(instruction[1] == "label"):
			self.instype = "label"
			self.label = instruction[2]
			labels.append(self.label)

		elif(instruction[1] == "print"):
			self.instype = "print"
			self.src1 = instruction[2]
		
		elif(instruction[1] == "scan"):		#todo
			self.instype = "scan"
			self.target = instruction[2]

		else:
			print "unknown instruction type,",instruction[1], "aborting"
			exit()
		
		if(self.target and self.target not in symbollist and not check_int(self.target)):
			symbollist.append(self.target)
		if(self.src1 and self.src1 not in symbollist and not check_int(self.src1)):
			symbollist.append(self.src1)
		if(self.src2 and self.src2 not in symbollist and not check_int(self.src2)):
			symbollist.append(self.src2)
	
	def __repr__(self):
		return ('%s %s %s %s %s %s' % (repr(self.instype), repr(self.operation), repr(self.src1), repr(self.src2), repr(self.target), self.label))
		

