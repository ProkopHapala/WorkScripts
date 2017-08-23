#!/usr/bin/python
import sys
import numpy as np
import matplotlib.pyplot as plt
import os
import __main__ as main

sys.path.append("/home/lada/Progs/PPM") 

import pyProbeParticle                as PPU     
from   pyProbeParticle            import basUtils
import pyProbeParticle.GridUtils      as GU
#import pyProbeParticle.fieldFFT       as fFFT
#import pyProbeParticle.PPPlot         as PPP

center = np.array([10.0, 10.0, 10.0]);


data1='ddensity-Si232-H.xsf'
data2='ddensity-Si232-CH3.xsf'
data3='ddensity-Si232-C6.xsf'
data4='ddensity-Si232-OH.xsf'
data5='ddensity-Si232-CHO.xsf'
data6='ddensity-Si232-CH3.xsf'



data, lvec, nDim, head = GU.loadXSF(str(data5))


ntot = nDim[0]*nDim[1]*nDim[2]
dV = lvec[1][0]*lvec[2][1]*lvec[3][2]/ntot

GU.setGridN   ( np.array( data.shape ).astype(np.int32)    )
GU.setGridCell( np.array((lvec[1],lvec[2],lvec[3])).copy() )
center, Hsum = GU.cog( data ); #print center, Hsum
rs,Hs,Ws = GU.sphericalHist( data, center, 0.1, 400 )
plt.subplot(2,1,1); plt.plot(rs, Hs*(len(Hs)/float(ntot)),  label="raw"  ); plt.plot(rs, Hs/Ws, label="weighted" ); 


sumHs= np.cumsum(Hs*dV) 
plt.subplot(2,1,2); plt.plot(rs, np.cumsum(Hs*(len(Hs)/float(ntot))),  label="raw" )

np.savetxt('Si232-CHO.dat', np.transpose(np.array([rs,Hs, Ws, Hs/Ws,sumHs])) )

#int_ch=integral(rs)

'''
data, lvec, nDim, head = GU.loadXSF(str(data2))
ntot = nDim[0]*nDim[1]*nDim[2]
GU.setGridN   ( np.array( data.shape ).astype(np.int32)    )
GU.setGridCell( np.array((lvec[1],lvec[2],lvec[3])).copy() )
center, Hsum = GU.cog( data ); #print center, Hsum
rs,Hs,Ws = GU.sphericalHist( data, center, 0.1, 400 )
plt.subplot(6,1,2); plt.plot(rs, Hs*(len(Hs)/float(ntot)),  label="raw"  ); plt.plot(rs, Hs/Ws, label="weighted" );

data, lvec, nDim, head = GU.loadXSF(str(str(data3))
ntot = nDim[0]*nDim[1]*nDim[2]
GU.setGridN   ( np.array( data.shape ).astype(np.int32)    )
GU.setGridCell( np.array((lvec[1],lvec[2],lvec[3])).copy() )
center, Hsum = GU.cog( data ); #print center, Hsum
rs,Hs,Ws = GU.sphericalHist( data, center, 0.1, 400 )
plt.subplot(6,1,3); plt.plot(rs, Hs*(len(Hs)/float(ntot)),  label="raw"  ); plt.plot(rs, Hs/Ws, label="weighted" );

data, lvec, nDim, head = GU.loadXSF(str(data4))
ntot = nDim[0]*nDim[1]*nDim[2]
GU.setGridN   ( np.array( data.shape ).astype(np.int32)    )
GU.setGridCell( np.array((lvec[1],lvec[2],lvec[3])).copy() )
center, Hsum = GU.cog( data ); #print center, Hsum
rs,Hs,Ws = GU.sphericalHist( data, center, 0.1, 400 )
plt.subplot(6,1,4); plt.plot(rs, Hs*(len(Hs)/float(ntot)),  label="raw"  ); plt.plot(rs, Hs/Ws, label="weighted" );

data, lvec, nDim, head = GU.loadXSF(str(data5))
ntot = nDim[0]*nDim[1]*nDim[2]
GU.setGridN   ( np.array( data.shape ).astype(np.int32)    )
GU.setGridCell( np.array((lvec[1],lvec[2],lvec[3])).copy() )
center, Hsum = GU.cog( data ); #print center, Hsum
rs,Hs,Ws = GU.sphericalHist( data, center, 0.1, 400 )
plt.subplot(6,1,5); plt.plot(rs, Hs*(len(Hs)/float(ntot)),  label="raw"  ); plt.plot(rs, Hs/Ws, label="weighted" );

'''

#print rs

#np.savetxt("mem.dat",mem_usage)
#plt.subplot(2,1,1); plt.plot(rs, Hs*(len(Hs)/float(ntot)),  label="raw"  ); plt.plot(rs, Hs/Ws, label="weighted" );
#plt.subplot(2,1,2); plt.plot(rs, Hs    );
#plt.savefig('mem.png',bbox_inches='tight')
plt.grid()
plt.show()
