from utils import *
infinity=10000000
dead=0
live=1
def useinfo(block):
	table=[{} for i in range(len(block)-1,-1,-1)]
	for i in range(len(block)-1,-1,-1):
		for symbol in symbollist:
			table[i][symbol]=list([dead,infinity])
	
	for i in range(len(block)-1,-1,-1):
		# print "i=",i,block[i].target, block[i].src1, block[i].src2
		if(i != len(block)-1):
			table[i]=table[i+1].copy()
		if(block[i].target and not check_int(block[i].target)):
			table[i][block[i].target]=list([dead,infinity])
		if(block[i].src1 and not check_int(block[i].src1)):
			table[i][block[i].src1]=list([live,i])
		if(block[i].src2 and not check_int(block[i].src2)):
			table[i][block[i].src2]=list([live,i])
		# print "for i=",i,table[i]
	
	for i in range(0,len(block)-1):
		table[i]=table[i+1].copy()
	# for i in range(0,len(block)):
	# 	print table[i]

	i=len(block)-1
	for symbol in symbollist:
		table[i][symbol]=list([dead,infinity])

	# print "now i'll fuck up"
	# for i in range(0,len(block)):
	# 	print table[i]

	return table
			# print table[i]
		# print '\n'


