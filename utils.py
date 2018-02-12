registers = ['eax','ebx','ecx','edx']
addrdesc={}
regdesc={}
symbollist=[]
symboltable={}
functions=[]
labels=[]
flag=0
def check_int(a):
	try:
		int(a)
		return 1
	except:
		return 0

def createsymboltable():
	for symbol in symbollist:
		if(symbol in functions):
			symboltable[symbol]={"type":"function","argslist":None}
		elif(symbol in labels):
			symboltable[symbol]={"type":"label","argslist":None}
		else:
			symboltable[symbol]={"type":"int","argslist":None}

def writeback():
	for reg in registers:
		if(regdesc[reg]):
			var=regdesc[reg]
			print "movl\t%"+reg+",\t"+var
			regdesc[reg]=''
			addrdesc[var][0]=''
			addrdesc[var][1]=True
	flag=1
	return

def writeexit():
	print "exit:"
	print "movl\t$0,\t%ebx"
	print "movl\t$1,\t%eax"
	print "int\t$0x80"
	print

def writeprint():
	print "print:"
	print "pushl\t%ebp"
	print "movl\t%esp,%ebp"
	with open ("printInteger.S") as f:
		d=f.readlines()
	for d1 in d:
		print d1.strip("\n")
