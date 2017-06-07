#!/usr/bin/python

import sys
import numpy as np
import pyMolecular.atomicUtils as au

# === read input

def CM(xyz):
    c=np.zeros(3)
    for i in np.arange(len(xyz[:,0])):	
	c[:]=c[:]+xyz[i,:]
    c[:]=c[:]/(len(xyz[:,0]))
    return c



fname       = sys.argv[1] 


xyzs, Zs, enames = au.loadAtoms( fname )

print CM(xyzs)
cm=CM(xyzs)

#Rs = np.dot( xyzs[:,0],xyzs[:,0] ) + np.dot( xyzs[:,1],xyzs[:,1] ) + np.dot( xyzs[:,2],xyzs[:,2] )

x=[]
for i in np.arange(0,20,0.01):          # loop over atoms
	for j in np.arange(len(xyzs[:,0])):
		diff=cm[:]-xyzs[j,:],cm-xyzs[j,:])
		if np.dot(diff,diff) < i && np.dot(diff,diff) >=i:
			if (enames) == Si:
			if (enames) == C:
			if (enames) == H:
			if (enames) == O:

print x
print np.shape(x)



'''
narg = len(sys.argv)
if narg < 5:
    print "use like this:"
    print "4    inputs [ input_file  center up fw ] (center, fw, up is atom index)" 
    print "or 6 inputs [ input_file  center up[0] up[1] fw[0] fw[1] ]"
    print "orient_mol.py  input.xyz   10      20       25       equals" 
    print "orient_mol.py  input.xyz   10   10 20    10 25             " 
    exit()
  
fname       = sys.argv[1] 
center_atom = int(sys.argv [2]);
fw_atoms    = [int(sys.argv[3]),center_atom]
up_atoms    = [int(sys.argv[4]),center_atom]

if(len(sys.argv)>6):
    fw_atoms    = [int(sys.argv[3]),int(sys.argv[4])]
    up_atoms    = [int(sys.argv[5]),int(sys.argv[6])]

margin = None
if(len(sys.argv)>7):
    margin = float(sys.argv[7])

print "fname=%s center %i fw %s up %s " %(fname,center_atom,fw_atoms,up_atoms)

# === main

xyzs, Zs, enames = au.loadAtoms( fname )

# center = np.array([10.0,20.0,15.0])
# xyzs_ = (xyzs - center[np.newaxis,:])
# Rs = np.dot( xyzs[:,0],xyzs[:,0] ) + np.dot( xyzs[:,1],xyzs[:,1] ) + np.dot( xyzs[:,2],xyzs[:,2] )

fw = xyzs[fw_atoms[1]-1]-xyzs[fw_atoms[0]-1]
up = xyzs[up_atoms[1]-1]-xyzs[up_atoms[0]-1]
rotmat = au.makeRotMat( fw , up );                    print rotmat
rotmat = np.transpose( rotmat[(2,1,0),:] );           print rotmat

#xyzs_ = xyzs - (xyzs[center_atom-1])[np.newaxis,:] 
xyzs_ = np.dot( xyzs - (xyzs[center_atom-1])[np.newaxis,:], rotmat  )

if margin is not None:
    xyzs_[:,0] += margin - xyzs_[:,0].min()
    xyzs_[:,1] += margin - xyzs_[:,1].min() 
    xyzs_[:,2] += margin - xyzs_[:,2].min() 

au.saveXyz(fname+'_.xyz',enames,xyzs_)
au.saveBas(fname+'_.bas',Zs,xyzs_)
'''