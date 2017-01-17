#! /usr/bin/python

import Element
import math
import sys


bondl=  float(sys.argv[1])      # bond length relative to sum of atomic radii
bondw=  float(sys.argv[2])		# bond width in visualization
#bclr=   float(sys.argv[2])      # bond color 

e=[]	# Proton number array
x=[]	# x coordinate array
y=[]
z=[]

bond = []

    # read atoms in memory
bas = open("answer.bas","r")
n=int(bas.readline())
for i in range(n):
    l=bas.readline().split()
    e.append(int(l[0]))
    x.append(float(l[1]))
    y.append(float(l[2]))
    z.append(float(l[3]))
bas.close()


# Find bonds
pov = open("bas.pov","a")
for i in range(n):
	for j in range(i):
		dx=x[j]-x[i]
		dy=y[j]-y[i]
		dz=z[j]-z[i]
		r=math.sqrt(dx*dx+dy*dy+dz*dz)
		bondlength=Element.rad[e[i]-1]+ Element.rad[e[j]-1]
		if (r<( bondl * bondlength)) :
			clr1= Element.clr[e[i]-1]
			clr2= Element.clr[e[j]-1]
			clr =[0.0,0.0,0.0]
			clr[0] = (clr1[0] + clr2[0]) * 0.5
			clr[1] = (clr1[1] + clr2[1]) * 0.5
			clr[2] = (clr1[2] + clr2[2]) * 0.5
			s= 'b( %10.5f, %10.5f, %10.5f, %10.5f, %10.5f, %10.5f, %10.5f, %10.5f, %10.5f, %10.5f, %10.5f,0.0 ) \n' %( x[i],y[i],z[i], bondw , x[j],y[j],z[j], bondw, clr[0]/255,clr[1]/255,clr[2]/255 )
			pov.write(s); 
pov.close()
