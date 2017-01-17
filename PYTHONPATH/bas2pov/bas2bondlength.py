#! /usr/bin/python

import Element
import math
import sys

widthscale=  float(sys.argv[1])		# bond width in visualization
#bclr=   float(sys.argv[2])      # bond color 


minlen=2.31
maxlen=2.42

el1=14
el2=14


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
		#print e[i],e[j]
		if(((e[i]==el1)&(e[j]==el2))|((e[i]==el2)&(e[j]==el1))):
			dx=x[j]-x[i]
			dy=y[j]-y[i]
			dz=z[j]-z[i]
			r=math.sqrt(dx*dx+dy*dy+dz*dz)
			#bondlength=Element.rad[e[i]-1]+ Element.rad[e[j]-1]
			if ((r<maxlen)&(r>minlen)) :
				#bondw=widthscale*(1-(r-minlen)/(maxlen-minlen))
				bondw = 0.25;
				#print bondw
				#clr1= Element.clr[e[i]-1]
				#clr2= Element.clr[e[j]-1]
				clr =[0.0,0.0,0.0]
				t=(1-(r-minlen)/(maxlen-minlen))
				clr[0] = 255*(1+math.cos( 5.0000*(t + 0.00000 + 0.4) ))
				clr[1] = 255*(1+math.cos( 5.0000*(t + 0.33333 + 0.4) ))
				clr[2] = 255*(1+math.cos( 5.0000*(t + 0.66666 + 0.4) ))

				#clr[0] = (clr1[0] + clr2[0]) * 0.5
				#clr[1] = (clr1[1] + clr2[1]) * 0.5
				#clr[2] = (clr1[2] + clr2[2]) * 0.5
				#clr[0] = clr[1] = clr[2] = 255* (1-(r-minlen)/(maxlen-minlen))

				s= 'b( %10.5f, %10.5f, %10.5f, %10.5f, %10.5f, %10.5f, %10.5f, %10.5f, %10.5f, %10.5f, %10.5f,0.0 ) \n' %( x[i],y[i],z[i], bondw , x[j],y[j],z[j], bondw, clr[0]/255,clr[1]/255,clr[2]/255 )
				pov.write(s); 

for i in range(100):
	clr =[0.0,0.0,0.0]
	t=i*0.01
	clr[0] = 255*(1+math.cos( 5.0000*(t + 0.00000 + 0.4) ))
	clr[1] = 255*(1+math.cos( 5.0000*(t + 0.33333 + 0.4) ))
	clr[2] = 255*(1+math.cos( 5.0000*(t + 0.66666 + 0.4) ))
	s = 'a( %10.5f, %10.5f, %10.5f, %10.5f, %10.5f, %10.5f, %10.5f, %10.5f ) \n' %( -10-t*10,-10+t*10,-10-t*10, 0.75, clr[0]/255.0,clr[1]/255.0,clr[2]/255.0,0.0 )
	pov.write(s); 

pov.close()
