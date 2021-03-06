from utils import *
from descriptors import *

name={
	'+':"addl",
	'-':"subl",
	'*':"imul",
	'/':"divl",
	'%':"mod",#thorough div
	'+=':"addl",
	'-=':"subl",
	'*=':"imul",
	'/=':"divl",
	'%=':"mod",#thorugh div
	'<<':"shl",
	'>>':"shr",
	'&&':"andl",
	'||':"orl",
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
	'eq':"je",
	'neq':"jne"
}

def gencode(i,instruction,nextinfotable):
	if(instruction.instype=='main'):
		print "realmain:"
		print "pushl\t%ebp"
		print "movl\t%esp,%ebp"
	elif(instruction.instype=="classd"):
		pass
	elif(instruction.instype=="classi"):
		pass
	elif(instruction.instype=="endclass"):
		pass
	elif(instruction.instype=="store"):
		if(check_int(instruction.src1)):
			if(addrdesc[instruction.target][0]):
				print "movl\t$",instruction.src1+",\t(%"+addrdesc[instruction.target][0]+")"
			else:
				print "movl\t$",instruction.src1+",\t("+instruction.target+")"
		else:
			if(addrdesc[instruction.src1][0]):
				print "movl\t%",addrdesc[instruction.src1][0]+",\t(%"+addrdesc[instruction.target][0]+")"
			else:
				print "movl\t(",instruction.src1+"),\t("+instruction.target+")"
	elif(instruction.instype=="dstore"):
		ydash=addrdesc[instruction.src1][0]
		if(ydash):
			if(addrdesc[instruction.target][0]):
				print "#from 1"
				print str("movl\t(%")+ydash+str("),\t%")+addrdesc[instruction.target][0]
			else:
				print "#from 2"
				regt=getreg(instruction,i,nextinfotable,instruction.src1)
				print str("movl\t(%")+ydash+str("),\t%")+regt
				addrdesc[instruction.target][0]=regt
				addrdesc[instruction.target][1]=False
				regdesc[regt]=instruction.target
		else:
			regsrc=getreg(instruction,i,nextinfotable,instruction.src1)
			addrdesc[instruction.src1][0]=regsrc
			addrdesc[instruction.src1][1]=False
			regdesc[regsrc]=instruction.src1
			if(addrdesc[instruction.target][0]):
				print "#from3"
				print str("movl\t(%")+regsrc+str("),\t%")+addrdesc[instruction.target][0]
			else:
				print "#from4"
				regt=getreg(instruction,i,nextinfotable,instruction.src1)
				print str("movl\t(%")+regsrc+str("),\t%")+regt
				addrdesc[instruction.target][0]=regt
				addrdesc[instruction.target][1]=False
				regdesc[regt]=instruction.target	
	elif(instruction.instype=="array"):
		if(check_int(instruction.src1)):
			print "subl\t$"+instruction.src1+",\t%esp"
		else:
			if(addrdesc[isntruction.src1][0]):
				print "subl\t%"+instruction.src1+",\t%esp"
			else:
				print "subl\t("+instruction.src1+"),\t%esp"
		if(addrdesc[instruction.target][0]):
			print "movl\t%esp,\t",addrdesc[instruction.target][0]
		else:
			print "movl\t%esp,\t",instruction.target
	elif(instruction.instype=='assignment'):
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
					print str("movl\t%")+ydash+str(",\t")+instruction.target+""
			else:
				regt=getreg(instruction,i,nextinfotable,instruction.target)
				print str("movl\t(")+instruction.src1+str("),\t%")+regt
				addrdesc[instruction.target][0]=regt
				addrdesc[instruction.target][1]=False
				regdesc[regt]=instruction.target
	
	elif(instruction.instype=='arithmetic' or instruction.instype== 'logical'):
		#for divide
		if(instruction.operation=="/" or instruction.operation=="/=" or instruction.operation=="%" or instruction.operation=="%="):
			#store values temporarily so do not update registers
			tempeax=''
			tempedx=''
			if(regdesc["eax"]):
				tempeax=regdesc["eax"]
				print "movl\t%eax,\t"+tempeax
			if(regdesc["edx"]):
				tempedx=regdesc["edx"]
				print "movl\t%edx,\t"+tempedx
			print "movl\t$0,\t%edx"
			#dividend=src1 #divisor =src2
			if(not check_int(instruction.src1)):
				#dividend
				if(addrdesc[instruction.src1][0]):
					print "movl\t%"+addrdesc[instruction.src1][0]+",\t%eax"
				else:
					print "movl\t("+instruction.src1+"),\t%eax"
					# regdesc["eax"]=instruction.src1
					# addrdesc[instruction.src1][0]="eax"
					# addrdesc[instruction.src1][1]=False
				#divisor
				if(not check_int(instruction.src2)):
					if(addrdesc[instruction.src2][0]):
						print "idivl\t%",addrdesc[instruction.src2][0]
					else:
						print "idivl\t"+instruction.src2
				else:
					regsrc2=getreg(instruction,i,nextinfotable,instruction.src2)
					# print "#myreg is ",regsrc2
					print "movl\t$",instruction.src2,",\t%"+regsrc2
					print "idivl\t%"+regsrc2
			else:
				print "movl\t$",isntruction.src1,",\t%eax"
				if(not check_int(instruction.src2)):
					if(addrdesc[instruction.src2][0]):
						print "idivl\t%",addrdesc[instruction.src2][0]
					else:
						print "idivl\t"+instruction.src2
				else:
					regsrc2=getreg(isntruction,i,nextinfotable,instruction.src2)
					print "idivl\t%"+instruction.src2

			if(instruction.operation=="/" or instruction.operation=="/="):
				reg="eax"
			else:
				reg="edx"
			if(addrdesc[instruction.target][0]):
				print "movl\t%"+reg+",\t%",addrdesc[instruction.target][0]
			else:
				print "movl\t%"+reg+",\t",instruction.target

			if(tempeax):
				print "movl\t("+tempeax+"),\t%eax"
			if(tempedx):
				print "movl\t("+tempedx+"),\t%edx"
		
		else:
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
			print "movl\t%eax"+",\t"+instruction.src1

	elif(instruction.instype=="load"):
		regt = getreg(instruction,i,nextinfotable,instruction.target)
		print "movl\t"+str(4+4*int(instruction.src1))+"(%ebp),\t%"+regt

	elif(instruction.instype == "push"):
		# writeback()
		if(not check_int(instruction.src1)):
			if(addrdesc[instruction.src1][0]):
				print "pushl\t%"+addrdesc[instruction.src1][0]
			else:
				print "pushl\t"+instruction.src1
		else:
				print "pushl\t$"+instruction.src1
	
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
	elif(instruction.instype == "print"):
		# writeback()
		# if(addrdesc[instruction.src1][0]):
		# 	print "pushl\t%"+addrdesc[instruction.src1][0]
		# else:
		# 	print "pushl\t"+instruction.src1
		print "pushl $outFormat"
		print "call printf" 
	
	elif(instruction.instype == "scan"):
		if(addrdesc[instruction.target][0]):
			regdesc[addresdesc[instruction.target][0]]=''
			addresdesc[instruction.target][0]=''
			addresdesc[instruction.target][1]=True
		print "pushl $",instruction.target
		print "pushl $inFormat"
		print "call scanf"

	else:
		print "unknown instruction"
		exit()
