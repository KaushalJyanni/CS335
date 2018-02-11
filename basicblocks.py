def leaders(ir):
	arr=[]
	arr.append(0)
	for i, instruction in enumerate(ir):
		# print i
		if(i==0):
			continue
		if(instruction.instype in ["ifgoto","jmp","callint","callvoid"]):
			if(i<len(ir)-1):
				arr.append(i+1)
		elif(instruction.instype in ['label']):
			arr.append(i)
		# elif(instruction.instype=="label"):
		# 	arr.append(i)
	# print arr
	return arr


def createblocks(ir):
	blocks=[]
	leaders_arr=leaders(ir)
	for i in range (0,len(leaders_arr)):
		if(i!=len(leaders_arr)-1):
			blocks.append(list(ir[x] for x in range(leaders_arr[i],leaders_arr[i+1])))
			# print list(ir[x] for x in range(leaders_arr[i],leaders_arr[i+1]))
		else:
			blocks.append(list(ir[x] for x in range(leaders_arr[i],len(ir))))
			# print list(ir[x] for x in range(leaders_arr[i],len(ir)))
		print
	return blocks

