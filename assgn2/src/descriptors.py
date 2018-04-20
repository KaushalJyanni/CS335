infinity=10000000
from utils import *
def initialise():
	for symbol in symbollist:
		addrdesc[symbol]=[]
		addrdesc[symbol].append('')
		addrdesc[symbol].append(True)
	for reg in registers:
		regdesc[reg]=''

def lookreg(var):
	if(addrdesc[var][0]):
		return 1
	else:
		return 0

def findempty():
	for reg in registers:
		if(not regdesc[reg]):
			return reg
	return 

def spill(reg,var):
	if(not addrdesc[var][1]):
		print "movl\t%"+reg+",\t"+var
		addrdesc[var][1]=True
	regdesc[reg]=''
	addrdesc[var][0]=''
	addrdesc[var][1]=True

def remove(var):
	for reg in registers:
		if(regdesc[reg]==var):
			regdesc[reg]=''
	# addrdesc[reg][]

def farthest(instruction,insnumber,nextinfotable):
	farthestuse=0
	farthestvar=''
	farthestreg=''
	for reg,vari in regdesc.iteritems():
		if(nextinfotable[insnumber][vari][1]==infinity):
			spill(reg,vari)
			return reg
		else:
			if(nextinfotable[insnumber][vari]>farthestuse):
				farthestuse=nextinfotable[insnumber][vari]
				farthestvar=vari
				farthestreg=reg
	spill(farthestreg,farthestvar)
	return farthestreg

def getreg(instruction,insnumber,nextinfotable,var):
	#x=y op z
	if(instruction.operation=="/" or instruction.operation=="/=" or instruction.operation=="%" or instruction.operation=="%="):
		if(not regdesc["ebx"]):
			return "ebx"
		elif(not regdesc["ecx"]):
			return "ecx"

		vebx=regdesc["ebx"]
		vecx=regdesc["ecx"]
		if(nextinfotable[insnumber][vebx][1]>nextinfotable[insnumber][vecx][1]):
			spill("ebx",vebx)
			return "ebx" 
		else:
			spill("ecx",vecx)
			return "ecx"
	elif(instruction.instype=="dstore"):
		x=instruction.target
		y=instruction.src1
		z=instruction.src2
		if(not check_int(y)):
			ydash=addrdesc[y][0]
		else:
			ydash=''
		# #y is in register and no next use
		# if(ydash and nextinfotable[insnumber][y][1]==infinity):
		# 	spill(ydash,y)
		# 	return ydash
		#return empty register
		if(findempty()):
			return findempty()
		else:
			return farthest(instruction,insnumber,nextinfotable)
	elif(instruction.instype=="assignment"or instruction.instype=="arithmetic"or instruction.instype=="logical"):
			x=instruction.target
			y=instruction.src1
			z=instruction.src2
			if(not check_int(y)):
				ydash=addrdesc[y][0]
			else:
				ydash=''
			#y is in register and no next use
			if(ydash and nextinfotable[insnumber][y][1]==infinity):
				spill(ydash,y)
				return ydash
			#return empty register
			elif(findempty()):
				return findempty()
			else:
				return farthest(instruction,insnumber,nextinfotable)
	
	elif(instruction.instype=="ifgoto"):
		if(not check_int(var)):
			y=var
			if(addrdesc[y][0]):
				return addrdesc[y][0]
			elif(findempty()):
				reg=findempty()
				print "movl\t("+y+"),\t%"+reg
				addrdesc[y][0]=reg
				addrdesc[y][1]=False
				regdesc[reg]=y
				return reg
			else:
				reg=farthest(instruction,insnumber,nextinfotable)
				print "movl\t("+y+"),\t%"+reg
				addrdesc[y][0]=reg
				addrdesc[y][1]=False
				regdesc[reg]=y
				return reg
		else:
			if(findempty()):
				reg=findempty()
				print "movl\t$"+var+",\t%"+reg
				# dont update descriptors coz jjust for temporary use
				# addrdesc[y][0]=reg
				# addrdesc[y][1]=False
				# regdesc[reg]=y
				return reg
			else:
				reg=farthest(instruction,insnumber,nextinfotable)
				print "movl\t$"+var+",\t%"+reg
				# dont update descriptors coz jjust for temporary use
				# addrdesc[y][0]=reg
				# addrdesc[y][1]=False
				# regdesc[reg]=y
				return reg

	elif(instruction.instype=="retint"):
		y=var
		if(addrdesc[y][0]):
			return addrdesc[y][0]
		elif(findempty()):
			reg=findempty()
			print "movl\t("+y+"),\t%"+reg
			addrdesc[y][0]=reg
			addrdesc[y][1]=False
			regdesc[reg]=y
			return reg
		else:
			reg=farthest(instruction,insnumber,nextinfotable)
			print "movl\t("+y+"),\t%"+reg
			addrdesc[y][0]=reg
			addrdesc[y][1]=False
			regdesc[reg]=y
			return reg
	elif(instruction.instype=="callint"):
		y=var
		if(addrdesc[y][0]):
			return addrdesc[y][0]
		elif(findempty()):
			reg=findempty()
			print "movl\t("+y+"),\t%"+reg
			addrdesc[y][0]=reg
			addrdesc[y][1]=False
			regdesc[reg]=y
			return reg
		else:
			# print "father"
			farthestuse=0
			farthestvar=''
			farthestreg=''
			for reg,vari in regdesc.iteritems():
				if(reg=="eax"):
					continue
				if(nextinfotable[insnumber][vari][1]==infinity):
					spill(reg,vari)
					return reg
				#calcuate
				else:
					if(nextinfotable[insnumber][vari]>farthestuse):
						farthestuse=nextinfotable[insnumber][vari]
						farthestvar=vari
						farthestreg=reg
			spill(farthestreg,farthestvar)
			return farthestreg
	elif(instruction.instype=="load"):
		if(findempty()):
			reg=findempty()
			y=instruction.target
			addrdesc[y][0]=reg
			addrdesc[y][1]=False
			regdesc[reg]=y
			return reg
		else:
			reg=farthest(instruction,insnumber,nextinfotable)
			y=instruction.target
			addrdesc[y][0]=reg
			addrdesc[y][1]=False
			regdesc[reg]=y
			return reg

