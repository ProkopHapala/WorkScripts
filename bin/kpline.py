#! /usr/bin/python

import sys

fin =open('kline.in')
fout=open('kline.kpts')


lines = []
n = 0
for line in fin:
	words = text.split()
	dn =  int(words[6]);
	lines.append( ( (float(words[0]), float(words[1]), float(words[2]) ), (float(words[3]), float(words[4]), float(words[5]), dn) ) )
	n+=dn

w = 1.0/n

fout.write("%i\n" %n )
for line in lines:
	m  = line[2]
	dx = ( line[1][0] - line[0][0] )/m
	dy = ( line[1][1] - line[0][1] )/m
	dz = ( line[1][2] - line[0][2] )/m
	for i in range( m ):
		fout.write( " %f %f %f \n" %(line[1][0]+dx*i,line[1][0]+dx*i,line[1][0]+dx*i,w)


