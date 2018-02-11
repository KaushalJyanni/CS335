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
		print "movl\t%"+reg+",\t"+var #"\t\t from spill"
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
		if(nextinfotable[insnumber][vari][1]==infinity):    ####will all variables value be present?
			spill(reg,vari)
			return reg
		#calcuate
		else:												####shud u check if this reg is in src or target
			if(nextinfotable[insnumber][vari]>farthestuse):
				farthestuse=nextinfotable[insnumber][vari]
				farthestvar=vari
				farthestreg=reg
	spill(farthestreg,farthestvar)
	return farthestreg

def getreg(instruction,insnumber,nextinfotable,var):
	#x=y op z
	if(instruction.instype=="assignment"or instruction.instype=="arithmetic"or instruction.instype=="logical"):
		x=instruction.target
		y=instruction.src1
		z=instruction.src2
		if(not check_int(y)):
			ydash=addrdesc[y][0]
		else:
			ydash=''
		# print "ydash",ydash
		#y is in register and no next use
		if(ydash and nextinfotable[insnumber][y][1]==infinity):
			# print "giving ",y,"'s register"
			# print nextinfotable[insnumber][y]
			spill(ydash,y)						######during spilling shud u removle regdesc[ydash]
			# print "return ing y's register"
			return ydash
		#return empty register
		elif(findempty()):
			return findempty()
			# print "returning empty register"
		else:
			# print "father"
			return farthest(instruction,insnumber,nextinfotable)
	
	elif(instruction.instype=="ifgoto"):
		if(not check_int(var)):
			y=var
			if(addrdesc[y][0]):
				return addrdesc[y][0]
			elif(findempty()):
				reg=findempty()
				print "movl\t("+y+"),\t%"+reg #### changed y from instruction.src1
				addrdesc[y][0]=reg
				addrdesc[y][1]=False
				regdesc[reg]=y
				return reg
				# print "returning empty register"
			else:
				reg=farthest(instruction,insnumber,nextinfotable)
				print "movl\t("+y+"),\t%"+reg #### changed y from instruction.src1
				addrdesc[y][0]=reg
				addrdesc[y][1]=False
				regdesc[reg]=y
				return reg
		else:
			if(findempty()):
				reg=findempty()
				print "movl\t$"+var+",\t%"+reg #### changed y from instruction.src1
				# dont update descriptors coz jjust for temporary use
				# addrdesc[y][0]=reg
				# addrdesc[y][1]=False
				# regdesc[reg]=y
				return reg
				# print "returning empty register"
			else:
				reg=farthest(instruction,insnumber,nextinfotable)
				print "movl\t$"+var+",\t%"+reg #### changed y from instruction.src1
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
			print "movl\t("+y+"),\t%"+reg#### changed y from instruction.src1
			addrdesc[y][0]=reg
			addrdesc[y][1]=False
			regdesc[reg]=y
			return reg
			# print "returning empty register"
		else:
			reg=farthest(instruction,insnumber,nextinfotable)
			print "movl\t("+y+"),\t%"+reg######
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
			print "movl\t("+y+"),\t%"+reg #### changed y from instruction.src1
			addrdesc[y][0]=reg
			addrdesc[y][1]=False
			regdesc[reg]=y
			return reg
			# print "returning empty register"
		else:
			print "father"
			farthestuse=0
			farthestvar=''
			farthestreg=''
			for reg,vari in regdesc.iteritems():
				if(reg=="eax"):
					continue
				if(nextinfotable[insnumber][vari][1]==infinity):    ####will all variables value be present?
					spill(reg,vari)
					return reg
				#calcuate
				else:												####shud u check if this reg is in src or target
					if(nextinfotable[insnumber][vari]>farthestuse):
						farthestuse=nextinfotable[insnumber][vari]
						farthestvar=vari
						farthestreg=reg
			spill(farthestreg,farthestvar)
			return farthestreg

