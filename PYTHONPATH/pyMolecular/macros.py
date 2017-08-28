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

def pbcTileMovie( shots=None, lvec=None, xyz_out=None, xyz_in='answer.xyz', cel_in='cel.lvs',  n=(2,2,2) ):
    if xyz_out is None:
        xyz_out = xyz_in[:xyz_in.index('.')]+( "_%ix%ix%i.xyz" %n );  print xyz_out
    if lvec is None:
        lvec  = np.genfromtxt(cel_in)
    if shots is None:
        shots = mol.loadXYZmovie( xyz_in )
    with open(xyz_out,'w') as f:
        for shot in shots:
            xyzs,_,enames = mol.pbc_tile( shot[0], lvec, enames=shot[2], n=n )
            mol.toXYZ( f, enames, xyzs )

def pbcRollMovie( shots=None, lvec=None, xyz_out=None, xyz_in='answer.xyz', cel_in='cel.lvs',  d=(0.5,0.5,0.5) ):
    if xyz_out is None:
        xyz_out = xyz_in[:xyz_in.index('.')]+"_shifted.xyz"
        print xyz_out
    if lvec is None:
        lvec  = np.genfromtxt(cel_in)
    if shots is None:
        shots = mol.loadXYZmovie( xyz_in )
    with open(xyz_out,'w') as f:
        for shot in shots:
            xyzs = mol.pbc_roll( shot[0], lvec, d=d )
            mol.toXYZ( f, shot[2], xyzs )
