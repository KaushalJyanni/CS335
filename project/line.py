import sys
file = sys.argv[1]
with open(file,'r') as f:
	data=f.readlines()

for i in range(0,len(data)):
	data[i]=str(i+1)+", "+data[i]

with open(file,'w') as f:
	for i in range(0,len(data)):
		f.write(data[i])
