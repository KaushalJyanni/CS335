#!/bin/python2
from utils import *
import sys
import asmcode as asm
import useinfo as ui
import basicblocks as bb
import generateasm as ga
import descriptors as desc

ir=[]
instructions=[]
file=sys.argv[1]
with open(file,'r') as f:
	ir=f.readlines()
	ir = [x.strip('\n') for x in ir] 

for i in ir:
	i=i.split(',')
	i=[x.strip(' ') for x in i]
	instructions.append(asm.threeAddCode(i))

desc.initialise()
blocks=bb.createblocks(instructions)
createsymboltable()
print ".data"
for symbol in symbollist:
	if(symbol in functions or symbol in labels):
		continue
	print "\t"+symbol+":\t.int\t0" 
print "\toutFormat:\t.asciz\t\"%d\\n\""
print "\tinFormat:\t.ascii\t\"%d\""
print
print ".text"
print ".global\tmain"
print
print "main:"
print "\tcall realmain"
print "\tjmp exit"
print
# print "realmain:"
# print "pushl\t%ebp"
# print "movl\t%esp,%ebp"
j=0
for block in blocks:
	nextinfotable=ui.useinfo(block)
	for i,ins in enumerate(block):
		print "#"+ir[j]
		ga.gencode(i,ins,nextinfotable)
		j+=1
	writeback()

writeexit()
# writeprint()


