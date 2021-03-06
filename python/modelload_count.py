#!/usr/bin/env python
# Model load
#
# python modelload.py  <countfile> 
# python modelload.py mc_count1
# 
# <countfile>  echo "stats items" | nc localhost 11211 | grep number


import os
import sys

def parseSizeLine( line, dic ):
	#STAT XY:chunk_size Z
	fields = line.split(':')
	slab = fields[0].split(' ')[1]
	size = fields[1].split(' ')[1]
	dic[slab] = size
	return

def loadSizes( fileName ):
	dic = {}
	ins = open(fileName, "r" )	
	for line in ins:
		parseSizeLine( line, dic )
	ins.close()
	return dic

def parseCountLine( line, dic ):
	#STAT items:XY:number Z
	fields = line.split(':')
	slab = fields[1]
	count = fields[2].split(' ')[1]
	dic[slab] = count
	return

def loadCount( fileName ):
	dic = {}
	ins = open(fileName, "r" )	
	for line in ins:
		parseCountLine( line, dic )
	ins.close()
	return dic

def debugPrint( dic1, dic2 ):
	print("Sizes:")
	for k,v in dic1.items():
	    print(k + " " + v)

	print("Count:")
	for k,v in dicCount.items():
	    print(k + " " + v)   

def fillRedis( r_server, slab, count, size ):	
	string_val = "x" * (size - 5) # -4 is to compensate key lenght (mc report full item size including key)
	for x in range(1, count):
		r_server.set(slab + "-" + str(x), string_val)
		if (x % 250 == 0):
			print('.'),

sizesFile = 'sizefile.txt'
countFile = 'countfile.txt'
server = 'localhost'

if (len(sys.argv) > 1):
	countFile = sys.argv[1]

dicCount = loadCount(countFile)
total = 0

for slab,count in dicCount.items():
	total += int(count)

print(total)