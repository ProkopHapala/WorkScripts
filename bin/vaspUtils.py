
iline_cel    = 2
iline_enames = 5 
iline_ecount = 6

def deter3x3( M ):
	return ( M[0][0]*( M[2][2]*M[1][1]-M[2][1]*M[1][2] ) - 
		     M[1][0]*( M[2][2]*M[0][1]-M[2][1]*M[0][2] ) + 
		     M[2][0]*( M[1][2]*M[0][1]-M[1][1]*M[0][2] ) )

def invert3x3( A ):
	idet = 1.0/deter3x3( A )
	return (
	(  (A[2][2]*A[1][1]-A[2][1]*A[1][2]) *idet,
	  -(A[2][2]*A[0][1]-A[2][1]*A[0][2]) *idet,
	   (A[1][2]*A[0][1]-A[1][1]*A[0][2]) *idet),
	( -(A[2][2]*A[1][0]-A[2][0]*A[1][2]) *idet,
	   (A[2][2]*A[0][0]-A[2][0]*A[0][2]) *idet,
	  -(A[1][2]*A[0][0]-A[1][0]*A[0][2]) *idet),
	(  (A[2][1]*A[1][0]-A[2][0]*A[1][1]) *idet,
	  -(A[2][1]*A[0][0]-A[2][0]*A[0][1]) *idet,
	   (A[1][1]*A[0][0]-A[1][0]*A[0][1]) *idet) )

def Mvec3(M,v):
	return (
		v[0]*M[0][0]+v[1]*M[0][1]+v[2]*M[0][2],
		v[0]*M[1][0]+v[1]*M[1][1]+v[2]*M[1][2],
		v[0]*M[2][0]+v[1]*M[2][1]+v[2]*M[2][2] )

def Mvec3_T(M,v):
	return ( 
		v[0]*M[0][0]+v[1]*M[1][0]+v[2]*M[2][0],
		v[0]*M[0][1]+v[1]*M[1][1]+v[2]*M[2][1],
		v[0]*M[0][2]+v[1]*M[1][2]+v[2]*M[2][2] )

def getLvec( inlines, i0=iline_cel  ):
	#print "getLvec: ", inlines[ i0   ]
	return [ [float(x) for x in inlines[ i0   ].split()],
	         [float(x) for x in inlines[ i0+1 ].split()],
	         [float(x) for x in inlines[ i0+2 ].split()] ]

def getENames( inlines, i0=iline_enames ):
	#print "getENames: ", inlines[ i0   ]
	return [x for x in inlines[i0].split()]

def getEcount( inlines, i0=iline_ecount ):
	#print "getEcount: ", inlines[ i0   ]
	return	[int(x) for x in inlines[i0].split()]

def shiftAtom( line, shift_abc ):
	words = line.split()
	ds = [ float(x) for x in words[:3] ]
	return ( " %10.10f %10.10f %10.10f " %(  (ds[0] + shift_abc[0])%1.0,   (ds[1] + shift_abc[1])%1.0,   (ds[2] + shift_abc[2])%1.0   ) )+ " ".join( words[3:] )

def shiftAtomXYZ( line, shift_abc, lvec ):
	words = line.split()
	ds = [ float(x) for x in words[:3] ]
	abc = ( (ds[0] + shift_abc[0])%1.0,   (ds[1] + shift_abc[1])%1.0,   (ds[2] + shift_abc[2])%1.0   )
	xyz = Mvec3_T( lvec, abc )
	return " %10.10f %10.10f %10.10f " %( xyz )


def genEnameList( enames, ecount ):
	ntot = sum( ecount )
	elist = [ ]
	for i in xrange( len(enames) ):
		elist = elist + [ enames[i] for j in xrange( ecount[i] ) ] 
	return elist

def readNLines( infile, n = 100 ):
	lines = []
	for i in xrange( n ):
		line  = infile.readline()
		lines.append( line )
	return lines

def readLinesUntil( infile, keyword, nmax = 1000000 ):
	lines = []
	for i in xrange( nmax ):
		line  = infile.readline()
		lines.append( line )
		if( keyword in line ):
			break
	return lines
		
def readUpTo( infile, keyword, nmax = 1000000 ):
	for i in xrange( nmax ):
		line = infile.readline()
		if ( keyword in line ):
			return True
	return False

def getNextForces( infile, nstart, nend ):
	if not readUpTo( infile, "TOTAL-FORCE (eV/Angst)" ):
		return None, None
	fx=0;fy=0;fz=0;
	iline = 0
	forces=[]
	while True:
		line = infile.readline()
		if iline >= nstart:
			#print iline, line,
			words = line.split()
			fs = (float(words[3]),float(words[4]),float(words[5]))
			forces.append( fs )
			fx+=fs[0]; fy+=fs[1]; fz+=fs[2]
			if( iline >= nend ):
				break
		iline+=1
	return (fx,fy,fz), forces

def getLastForce( infile, nstart, nend ):
	ftot=None; forces=None
	while infile.readline(): 
		ftot_, forces_ = getNextForces( infile, nstart, nend )
		if ftot_ is not None:
			ftot = ftot_; forces = forces_;
	return ftot, forces

def getLastForceGrep( fname, nstart, nend ):
	import os
	command = "grep -A %i TOTAL-FORCE %s | tail -%i > tmp" %( nend+1, fname, nend-nstart+1)
	#print command
	os.system( command )
	ftmp = open( 'tmp', 'r' )
	fx=0;fy=0;fz=0; forces=[]
	for line in ftmp:
		#print "-", line
		words = line.split()
		fs = (float(words[3]),float(words[4]),float(words[5]))
		forces.append( fs )
		fx+=fs[0]; fy+=fs[1]; fz+=fs[2]
	ftmp.close() 
	return (fx,fy,fz), forces





