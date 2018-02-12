#!/bin/python2
# import utils
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
	# print i
	instructions.append(asm.threeAddCode(i))

desc.initialise()

blocks=bb.createblocks(instructions)

print ".data"
for symbol in symbollist:
	if(symbol in functions or symbol in labels):
		continue
	print "\t"+symbol+":\t.int\t0" 
print "\t"+"message"+":\t.ascii\t\"\\n\"" 
print
print ".text"
print ".global\t_start"
print
print "_start:"
print "\tcall main"
print "\tjmp exit"
print
print "main:"
print "pushl\t%ebp"
print "movl\t%esp,%ebp"
for block in blocks:
	nextinfotable=ui.useinfo(block)
	for i,ins in enumerate(block):
		ga.gencode(i,ins,nextinfotable)
	# if(not flag):
	# print "writeback of main"
	writeback()
	# utils.flag=0

writeexit()
writeprint()


