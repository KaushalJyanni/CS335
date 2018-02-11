from utils import *
# import utils
from descriptors import *

name={
	'+':"add",
	'-':"sub",
	'*':"mult",
	'/':"div",	#check
	'%':"mod",	#check
	'+=':"add",
	'-=':"sub",
	'*=':"mult",
	'/=':"div",
	'%=':"mod",
	'<<':"shl",
	'>>':"shr",
	'&':"and",
	'|':"or",
	'^':"xor",
	'<<=':"shl",	#check
	'>>=':"shr",
	'&=':"and",
	'|=':"or",
	'^=':"xor",
	'leq':"je",
	'lt':"jl",
	'geq':"jge",
	'gt':"jg",
	'eq':"jeq",
	'neq':"jne"
}

def gencode(i,instruction,nextinfotable):
	# print "# line number ",i+1
	if(instruction.instype=='assignment'):
		if(check_int(instruction.src1)):
			if(addrdesc[instruction.target][0]):
				print str("movl\t$")+instruction.src1+str(",\t%")+addrdesc[instruction.target][0]
			else:
				print str("movl\t$")+instruction.src1+str(",\t(")+instruction.target+")"
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
				###############################################################dont delete it################################3
		# if(not addrdesc[instruction.target][0]):	#if x not already in reg
		# 	regt=getreg(instruction,i,nextinfotable,instruction.target)
		# else:
		# 	regt=addrdesc[instruction.target][0]
		# if(check_int(instruction.src1)):
		# 	print str("movl\t$")+instruction.src1+str(",\t%")+regt
		# else:
		# 	ydash=addrdesc[instruction.src1][0]
		# 	if(ydash):
		# 		print str("movl\t%")+ydash+str(",\t%"),regt
		# 	else:
		# 		print str("movl\t(")+instruction.src1+str("),\t%")+regt
		# addrdesc[instruction.target][0]=regt
		# addrdesc[instruction.target][1]=False
		# regdesc[regt]=instruction.target
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
		### do what, if same???
		if(not check_int(instruction.src2)):
			zdash=addrdesc[instruction.src2][0]
			# print "src2 is", instruction.src2
		else:
			zdash=''
		##if reg
		if(zdash):
			print name[instruction.operation]+str("\t%")+zdash+str(",\t%")+regt
		##from mem
		else:
			print name[instruction.operation]+str("\t(")+instruction.src2+str("),\t%")+regt
		addrdesc[instruction.target][0]=regt
		addrdesc[instruction.target][1]=False
		regdesc[regt]=instruction.target
	
	elif(instruction.instype=='label'):
		print instruction.label,":"
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
			if(not check_int(instruction.src1)):
				# regsrc1=getreg(instruction,i,nextinfotable,instruction.src1)
				# if(not check_int(instruction.src2)):
				# 	if(addrdesc[instruction.src2][0]):
				# 		print str("cmp\t%")+regsrc1+str("\t,%")+addrdesc[instruction.src2][0]
				# 	else:
				# 		print str("cmp\t%")+regsrc1+str("\t,(")+instruction.src2+")"
				# else:
				# 	reg=getreg(instruction,i,nextinfotable,instruction.src2)
				# 	print str("cmp\t%")+regsrc1+str(",\t$")+instruction.src2
				regsrc2=getreg(instruction,i,nextinfotable,instruction.src2)
				regsrc1=addrdesc[instruction.src1][0]
				if(regsrc1):
					print str("cmp\t%")+regsrc1+str(",\t%")+regsrc2
				else:
					print str("cmp\t(")+instruction.src1+str("),\t%")+regsrc2
			else:
				regsrc2=getreg(instruction,i,nextinfotable,instruction.src2)
				print str("cmp\t$")+isntruction.src1+str("\t,%")+regsrc2
			print name[instruction.operation],"\t",instruction.target
	elif(instruction.instype=='callvoid'):
		writeback()
		print "call\t",instruction.target
	elif(instruction.instype=='retvoid'):
		# print "writeback of retvoid"
		writeback()
		print "leave"
		print "ret"
		print
	elif(instruction.instype=='callint'):
		writeback()
		#writeback of eax
		# if(regdesc["eax"]):
		# 	var=regdesc["eax"]
		# 	print "movl\t%"+"eax"+",\t"+var
		# 	regdesc["eax"]=''
		# 	addrdesc[var][0]=''
		# 	addrdesc[var][1]=True
		print "call\t",instruction.target
		# reg=getreg(instruction,i,nextinfotable,instruction.src1)
		# if(addrdesc[instruction.src1][0]):
			# reg=addrdesc[instruction.src1][0]
			# print "movl\t%"+eax+",\t%"+reg
		# else:
		if(addrdesc[instruction.src1][0]):
			print "movl\t%eax"+",\t%"+addresdesc[instruction.src1][0]
		else:
			print "movl\t%eax"+",\t("+instruction.src1+")"

	elif(instruction.instype == 'retint'):
		# print "writeback of retint"
		writeback()
		if(not check_int(instruction.target)):
			# reg=getreg(instruction,i,nextinfotable,instruction.target)
			# if(reg!="eax"):
			# 	if(regdesc["eax"]):
			# 		spill("eax",regdesc["eax"])
			# 	remove(instruction.target)	
			# 	print "movl\t%"+reg+"\,t%eax"
			# 	regdesc["eax"]=instruction.target
			# 	addrdesc[instruction.target][0]="eax"
			# 	addrdesc[instruction.target][1]=False
			if(addrdesc[instruction.target][0]):
				reg=addrdesc[instruction.target][0]
				if(reg!="eax"):
					if(regdesc["eax"]):
						spill("eax",regdesc["eax"])
					print "movl\t%"+reg+"\,t%eax"
					remove(instruction.target)
			else:
				print "movl\t("+instruction.target+"),\t%eax"
			# regdesc["eax"]=instruction.target
			# addrdesc[instruction.target][0]="eax"
			# addrdesc[instruction.target][1]=False

		else:
			if(regdesc["eax"]):
				spill("eax",regdesc["eax"])
				print "movl\t$"+instruction.target+",\t%eax"
				valueof=''
				regdesc["eax"]=valueof ##not any variable just an int
		print "leave"
		print "ret"
		print 
	else:
		print "unknown instruction"
		exit()
