#!/usr/bin/python

import vaspUtils as vu

fname    = 'answer.bas'

fin   = open( fname, 'r' )
fout  = open( fname+'_shifted.bas' )

def readCell( cellname = 'cel.lvs' ):
	fcell = open( cellname, 'r' )
	cell = [ 
		[ float(word) in fcell.readline().split() ]
		[ float(word) in fcell.readline().split() ]
		[ float(word) in fcell.readline().split() ]
	]
	fcell.close()
	return cell

def moveInCell( xyz ):
	abc  = vu.Mvec3( icell, xyz )
	abc_ = ( (abc[0] + shift[0])%1.0,  (abc[1] + shift[1])%1.0, (abc[2] + shift[2])%1.0 )
	return vu.Mvec3( abc_ )

cell  = readCell()
icell = vu.invert3x3( cell )

n = int( fin.readline() )
fout.write('%i \n' %n )
for i in range( n ):
	words = fin.readline().split()
	xyz  = ( float(words[1]), float(words[2]), float(words[3]) )
	xyz_ = moveInCell( xyz )
	fout.write( '%s %f %f %f \n' %(words[0], xyz_[0], xyz_[1], xyz_[2] ) )
