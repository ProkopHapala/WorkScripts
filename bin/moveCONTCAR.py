#!/usr/bin/python
import sys
#import numpy as np
import vaspUtils as vu

i0atom      = 8
istart      = int(sys.argv[1])
iend        = int(sys.argv[2])
shift_xyz   = ( float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5] ) )
imin=i0atom+istart
imax=i0atom+iend

print "imin,imax ", imin,imax

infile  = open( "CONTCAR", 'r' )
outfile = open( "POSCAR",  'w' )
inlines = infile.readlines()

lvec   = vu.getLvec  ( inlines )
enames = vu.getENames( inlines  )
ecount = vu.getEcount( inlines  )

ilvec     = vu.invert3x3( lvec )
shift_abc = vu.Mvec3(ilvec, shift_xyz)

#print "lvec      ", lvec
#print "enames    ", enames
#print "ecount    ", ecount
#print "shift_abc ", shift_abc

for iline,line in enumerate( inlines ):
	if( iline >= imin ) and ( iline <= imax ):
		outfile.write( vu.shiftAtom( line, shift_abc )+"\n" )
	else:
		outfile.write( line )

infile.close()
outfile.close()
