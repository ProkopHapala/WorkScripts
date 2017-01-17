#!/usr/bin/python

#from xyzutils import *

import sys

is_test = False
if(len(sys.argv)>1):
	job_type=sys.argv[1]
	if( job_type=='t' ):
		is_test=True
 

poscar = open('POSCAR','w') 

poscar.write( "Some structure\n" )
poscar.write( "1.00000000\n" )

celfile = open('cel.lvs')
for line in celfile:
	poscar.write( line )
celfile.close()

names = []
potcar = open('POTCAR')
for line in potcar:
	if 'TITEL' in line:
		#print line
		names.append(line.split()[3])
potcar.close()
#names = [x for x in xdat.readline().split()]

#print names

poscar.write( " ".join(names) + "\n" )




mask = []
try:
	maskfile = open('fixmask')
	for line in maskfile:
		words=line.split()
		mask.append( [int(words[0]),int(words[1])] )
except Exception, e:
	print "no mask" 

mask.append( [1000000,1000001] )

print mask


xyzfile = open('answer.xyz')
nnames = len(names)
rewrite = [[0,[]] for i in range(nnames)]
imask = 0
iline = 0
for line in xyzfile:
	while ((iline-1)>mask[imask][1]):
		print imask, iline, mask[imask][1]
		imask+=1
	fix=' T T T\n'
	if( (iline-1) >= mask[imask][0] ):
		fix=' F F F\n'
	for iname in range(nnames):
		words = line.split()
		if len(words)>2:
			if words[0] == names[iname]:
				#print names[iname]," ",line
				rewrite[ iname ][0]+=1
				rewrite[ iname ][1].append( words[1]+"      "+words[2]+"      "+words[3]+fix )
				break
	iline+=1

for iname in range(nnames):
	poscar.write( "%i " %rewrite[ iname ][0] )
poscar.write( "\n" )

poscar.write( "Selective dynamics\n" )
poscar.write( "Cartesian\n" )

if(is_test):
	for iname in range(nnames):
		for line in rewrite[ iname ][1]:
			poscar.write( names[iname]+"    "+line )
else:
	for iname in range(nnames):
		for line in rewrite[ iname ][1]:
			poscar.write( line )

poscar.close()
