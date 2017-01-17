import vaspUtils as vu
import numpy as np

M = ( (16,1,9),(7,6,-4),(-4,9,1) )

v = ( 1.0, 1.545, -0.66 )

print "vu.deter2x2( M )", vu.deter3x3( M )
print "np.det( M )", np.linalg.det( M )


print "vu.invert( M )", vu.invert3x3( M )
print "np.inv( M )", np.linalg.inv( M )


print "vu.Mvec3 (M, v )", vu.Mvec3 ( M, v )
print "np.dot  ( M, v )", np.dot   ( M, v )
