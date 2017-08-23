#!/usr/bin/python

import numpy as np
import elements
import atomicUtils as mol

def orient( xyzs, ifw=(0,1), iUp=(0,2), i0=None ):
    if i0 is not None:
        xyzs = xyzs - xyzs[0][None,:]
    fw   = xyzs[ifw[1]] - xyzs[ifw[0]]
    up   = xyzs[iUp[1]] - xyzs[iUp[0]]
    mat  = mol.makeRotMat( fw, up )
    return np.dot( xyzs, np.transpose(mat) )

def orientXyzFile( fnin, fnout, ifw=(0,1), iUp=(0,2), i0=None ):
    xyzs,Zs,enames = mol.loadAtoms(  fnin )
    xyzs_ = orient( xyzs, ifw=ifw, iUp=iUp, i0=i0 )
    mol.saveXyz( fnout+".xyz", enames, xyzs_ )

