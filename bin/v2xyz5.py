#!/usr/bin/python
import sys

shift=(0,0,0)
if len(sys.argv) > 3:
	shift=( float(sys.argv[1]), float(sys.argv[2]) ,float(sys.argv[3]) )
#print shift

xdat = open("CONTCAR")
xyzf = open("CONTCAR.xyz",'w')
xdat.readline()
latscale = float( xdat.readline())
a = [float(x) for x in xdat.readline().split()]
b = [float(x) for x in xdat.readline().split()]
c = [float(x) for x in xdat.readline().split()]
#print a[0], a[0], a[0]
#print b[0], b[0], b[0]
#print c[0], c[0], c[0]
enames = [x for x in xdat.readline().split()]
ecount = [int(x) for x in xdat.readline().split()]

#print enames
#print ecount
ntot = sum(ecount)
line   = xdat.readline(); #print "readlin >> ",line
line   = xdat.readline(); #print "readlin >> ",line
line   = xdat.readline(); #print "readlin >> ",line
iatom = 0
itype = 0
xyzf.write( "%i\n" %ntot )
xyzf.write( "from VAPS CONTCAR\n" )
while line:
	#print iimage,itype,iatom,ecount[itype],line
	ds_ = [float(x) for x in line.split()[:3] ]
	ds = [ (ds_[0] + shift[0])%1.0,   (ds_[1] + shift[1])%1.0,   (ds_[2] + shift[2])%1.0   ]
	x = ds[0]*a[0] + ds[1]*b[0] + ds[2]*c[0]
	y = ds[0]*a[1] + ds[1]*b[1] + ds[2]*c[1]
	z = ds[0]*a[2] + ds[1]*b[2] + ds[2]*c[2]
	xyzf.write( enames[itype]+("  %f %f %f \n" %(x,y,z)) )
	line = xdat.readline()
	iatom+=1;
	if(iatom>=ecount[itype]):
		iatom=0
		itype+=1
		if(itype>=len(ecount)):
			break
			

xyzf.write( "\n" )
xyzf.close()
xdat.close()

		
