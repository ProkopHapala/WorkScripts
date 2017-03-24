#!/usr/bin/python

import sys
import numpy as np
import pyMolecular.atomicUtils as au

# === read input

fname       = sys.argv[1]
celname     = sys.argv[2]
nabc        = np.array( ( int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]) ) ) 

# === main

lvec             = np.genfromtxt(celname)
xyzs, Zs, enames = au.loadAtoms(fname)

enames_=[];Zs_=[];xyzs_=[]
for ia in range(nabc[0]):
    for ib in range(nabc[1]):
        for ic in range(nabc[2]):
            xyzs_  .append( xyzs + (lvec[0]*ia + lvec[1]*ib + lvec[0]*ic)[np.newaxis,:] )
            enames_ += enames
            Zs_     .append(Zs)
Zs_ = np.concatenate( Zs_ )
xyzs_ = np.concatenate( xyzs_ )


au.saveXyz(fname+'_%ix%ix%i.xyz' %(nabc[0],nabc[1],nabc[2]),enames_,xyzs_)
au.saveBas(fname+'_%ix%ix%i.bas' %(nabc[0],nabc[1],nabc[2]),Zs_,xyzs_)
