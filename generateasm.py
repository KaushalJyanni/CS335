from utils import *
from descriptors import *

name={
	'+':"addl",
	'-':"subl",
	'*':"multl",
	'/':"divl",
	'+=':"addl",
	'-=':"subl",
	'*=':"multl",
	'/=':"divl",
	'<<':"shl",
	'>>':"shr",
	'&':"and",
	'|':"orl",
	'^':"xorl",
	'<<=':"shl",
	'>>=':"shr",
	'&=':"andl",
	'|=':"orl",
	'^=':"xor",
	'leq':"jle",
	'lt':"jl",
	'geq':"jge",
	'gt':"jg",
	'eq':"jeq",
	'neq':"jne"
}

def gencode(i,instruction,nextinfotable):
	if(instruction.instype=='assignment'):
		if(check_int(instruction.src1)):
			if(addrdesc[instruction.target][0]):
				print str("movl\t$")+instruction.src1+str(",\t%")+addrdesc[instruction.target][0]
			else:
				print str("movl\t$")+instruction.src1+str(",\t")+instruction.target
		else:
			ydash=addrdesc[instruction.src1][0]
			if(ydash):
				if(addrdesc[instruction.target][0]):
					print str("movl\t%")+ydash+str(",\t%")+addrdesc[instruction.target][0]
				else:
					print str("movl\t%")+ydash+str(",\t(")+instruction.target+")"
			else:
				regt=getreg(instruction,i,nextinfotable,instruction.target)
				print str("movl\t(")+instruction.src1+str("),\t%")+regt
				addrdesc[instruction.target][0]=regt
				addrdesc[instruction.target][1]=False
				regdesc[regt]=instruction.target
	
	elif(instruction.instype=='arithmetic' or instruction.instype== 'logical'):
		#x=y op z
		if(not addrdesc[instruction.target][0]):	#if x not already in reg
			regt=getreg(instruction,i,nextinfotable,instruction.target)
		else:
			regt=addrdesc[instruction.target][0]
		#check y addrdesc
		if(not check_int(instruction.src1)):
			ydash=addrdesc[instruction.src1][0]
		else:
			ydash=''
		if(ydash and ydash != regt): ##if y already in reg
			print str("movl\t%")+ydash+str(",\t%")+regt
		elif(not ydash and ydash!=regt):
			if(check_int(instruction.src1)):		##from a constant
				print str("movl\t$")+instruction.src1+str(",\t%")+regt
			else:
				print str("movl\t(")+instruction.src1+str("),\t%")+regt
		if(not check_int(instruction.src2)):
			zdash=addrdesc[instruction.src2][0]
		else:
			zdash=''
		##if reg
		if(zdash):
			print name[instruction.operation]+str("\t%")+zdash+str(",\t%")+regt
		##from mem
		else:
			if(not check_int(instruction.src2)):
				print name[instruction.operation]+str(" \t(")+instruction.src2+str("),\t%")+regt
			else:
				print name[instruction.operation]+str(" \t$")+instruction.src2+str(",\t%")+regt
		addrdesc[instruction.target][0]=regt
		addrdesc[instruction.target][1]=False
		regdesc[regt]=instruction.target
	
	elif(instruction.instype=='label'):
		print instruction.label+":"
		if(instruction.label in functions):
			print "pushl\t%ebp"
			print "movl\t%esp,%ebp"
	
	elif(instruction.instype=='goto'):
		writeback()
		print "jmp\t",instruction.target
	
	elif(instruction.instype=="ifgoto"):
		writeback()
		if(instruction.operation not in ['eq','neq','gt','geq','lt','leq']):
			print "unknown comparison in ifgoto"
			exit()
		else:
			#check y addrdesc
			if(not check_int(instruction.src2)):
				regsrc2=getreg(instruction,i,nextinfotable,instruction.src2)
				regsrc1=addrdesc[instruction.src1][0]
				if(regsrc1):
					print str("cmp \t%")+regsrc2+str(",\t%")+regsrc1
				else:
					print str("cmp \t%")+regsrc2+str(",\t")+instruction.src1
			else:
				if(not check_int(instruction.src1)):
					if(addrdesc[instruction.src1][0]):
						print str("cmp \t$")+instruction.src2+str(",\t%")+adddrdesc[isntruction.src1][0]
					else:
						print str("cmp \t$")+instruction.src2+str(",\t")+instruction.src1
				else:
					regsrc1=getreg(instruction,i,nextinfotable,instruction.src1)
					print str("cmp \t$")+instruction.src2+str(",\t%")+regsrc1
			print name[instruction.operation],"\t",instruction.target
	
	elif(instruction.instype=='callvoid'):
		writeback()
		print "call\t",instruction.target
	
	elif(instruction.instype=='retvoid'):
		writeback()
		print "leave"
		print "ret"
		print
	
	elif(instruction.instype=='callint'):
		writeback()
		print "call\t",instruction.target
		if(addrdesc[instruction.src1][0]):
			print "movl\t%eax"+",\t%"+addresdesc[instruction.src1][0]
		else:
			print "movl\t%eax"+",\t("+instruction.src1+")"

	elif(instruction.instype == 'retint'):
		writeback()
		if(not check_int(instruction.target)):
			if(addrdesc[instruction.target][0]):
				reg=addrdesc[instruction.target][0]
				if(reg!="eax"):
					if(regdesc["eax"]):
						spill("eax",regdesc["eax"])
					print "movl\t%"+reg+"\,t%eax"
					remove(instruction.target)
			else:
				print "movl\t("+instruction.target+"),\t%eax"
		else:
			if(regdesc["eax"]):
				spill("eax",regdesc["eax"])
				print "movl\t$"+instruction.target+",\t%eax"
				valueof=''
				regdesc["eax"]=valueof ##not any variable just an int
		print "leave"
		print "ret"
		print
	elif(instruction.instype == 'print'):
		writeback()
		print "movl\t("+instruction.src1+"),\t%eax"
		print "call print"
	else:
		print "unknown instruction"
		exit()
