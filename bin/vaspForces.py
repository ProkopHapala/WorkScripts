#!/usr/bin/python

import vaspUtils as vu
import sys 

#nstart = 1
#nend   = 15

nstart = int(sys.argv[1])
nend   = int(sys.argv[2])
filename = 'OUTCAR'
if len(sys.argv) > 3:
   filename = sys.argv[3]

'''
infile = open( filename, 'r' )
ftot, forces = vu.getLastForce( infile, nstart, nend )
'''

ftot, forces = vu.getLastForceGrep( filename, nstart, nend )
print ftot[0],ftot[1],ftot[2]
