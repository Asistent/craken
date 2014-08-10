from BruteListBuilder import ListMaker
from sys import stdout, argv
from time import time
import hashlib
import os
import random

class crack:
	'''Raw crack function without the use of dictionary'''
	def __init__(self,hash,encryption):
		self.hash = hash
		self.enc = encryption
	def step(self,word):
		hash = getattr(hashlib,self.enc)(word).hexdigest()
		stdout.write('\r'+word+" = ? "+hash) 
		if (hash==self.hash):
			print("\nFOUND: "+word)
			open("LastCracked.txt","a").write(word+" = "+self.hash)
			exit()

class build:
	def __init__(self,encryption):
		'''Dictionary builder'''
		self.enc = encryption
		self.words = []#I wanted to use arrays instead of dicts to be dependent from pickle, json...
		self.hashs = []
		self.lastSave = time()
		self.fileNumber = 1
		self.folderName = "Dict"+str(random.randint(1,1000))
		os.mkdir(self.folderName)
		
	def step(self,word):
		hash = getattr(hashlib,self.enc)(word).hexdigest()
		stdout.write('\r'+word+" = ? "+hash)
		self.words.append(word)
		self.hashs.append(hash)
		
		if (time()-self.lastSave>30):
			toWrite = ""
			#building file
			for x in range(len(self.words)):
				toWrite += self.hashs[x]+"\t"+self.words[x]+"\n"
			
			#saving
			path = self.folderName+"/"+str(self.fileNumber)+".txt"
			print("\nSaving in "+path)
			file = open(path,"w")
			file.write(toWrite)
			
			#reset timer and tmp arrays
			self.fileNumber += 1
			self.words = []
			self.hashs = []
			self.lastSave = time()
			del toWrite

def readDict(folder,hashx,n=1):
	path = folder+"/"+str(n)+".txt"
	print("Reading: "+path)
	try:
		data = open(path).read().split("\n")
	except IOError:
		print("This hash isn't in this dictionary")
		return ""
	for line in data:
		try:
			hash = line.split("\t")[0]
			word = line.split("\t")[1]
			if (hash == hashx):
				return word
		except IndexError:
			print("[*] ERROR: File corrupted?\nPassing...")
	readDict(folder,hashx,n+1)

__help__ = """
Arguements:
-nf [encryption] [hash]	use with no dictionary
-f  [filename]      	use a dictionary (make one before)
-mf [encryption]    	make dictionary
example:
> """+argv[0]+""" -nf md5 098f6bcd4621d373cade4e832627b4f6
"""

if (__name__=="__main__"):
	if (len(argv)<=1):
		print(__help__)
	elif (argv[1]=="-nf"):
		print("Cracking...")
		cracker = crack(argv[3],argv[2])
		ListMaker(cracker.step).next()
	elif (argv[1]=="-mf"):
		builder = build(argv[2])
		ListMaker(builder.step).next()
	elif (argv[1]=="-f"):
		print("Finding....")
		print(readDict(argv[2],argv[3]))
		
