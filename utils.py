# registers = ['rax','rbx','rcx','rdx','rsi','rdi','rbp','rsp']
registers = ['eax','ebx','ecx','edx']
addrdesc={}
regdesc={}
symbollist=[]
functions=[]
labels=[]
flag=0
def check_int(a):
	try:
		int(a)
		return 1
	except:
		return 0

def writeback():
	# print "writng back"
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
		# d1.strip("\n")
		print d1.strip("\n")
#doubts
#writing label in x86
#writing jmp instruction. more or less ame as above
#shl operator
#SRC DST OR DST SRC

