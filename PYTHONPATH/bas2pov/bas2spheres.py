#! /usr/bin/python

import Element
import sys

spherescale=float(sys.argv[1])	

e=[]	# Proton number array
x=[]	# x coordinate array
y=[]
z=[]

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


pov = open("bas.pov","a")
print n
for i in range(n):
    clr = Element.clr[e[i]-1]
    a = (z[i] + 1.8)*2.0
    s = 'a( %10.5f, %10.5f, %10.5f, %10.5f, %10.5f, %10.5f, %10.5f, %10.5f ) \n' %( x[i],y[i],z[i], spherescale*Element.rad[e[i]-1], clr[0]/255.0-a,clr[1]/255.0,clr[2]/255.0+a,0.0 )
    # s = 'a( %10.5f, %10.5f, %10.5f, %10.5f, %10.5f, %10.5f, %10.5f, %10.5f ) \n' %( x[i],y[i],z[i], spherescale*Element.rad[e[i]-1], a*clr[0]/255.0,a*clr[1]/255.0,a*clr[2]/255.0,0.0 )
    pov.write(s); 
    #print i,s


i=0
for zz in [-1.6,-1.7,-1.8,-1.9, -2.0]:
	a = (zz + 1.8)*2.0 
	clr= Element.clr[14-1]
	s = 'a( %10.5f, %10.5f, %10.5f, %10.5f, %10.5f, %10.5f, %10.5f, %10.5f ) \n' %( 0, 2+i*1.5, 0, 0.6, clr[0]/255.0-a,clr[1]/255.0,clr[2]/255.0+a,0.0 )
	pov.write(s)
	i=i+1
pov.close()
