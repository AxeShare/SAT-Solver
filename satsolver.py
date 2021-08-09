from copy import copy, deepcopy
import sys
import operator
import time		
start_time = time.time()
 
sys.setrecursionlimit(10000)
 
decomp=0
tst = 0
file = open("output.txt", mode='w')

globalLiterals=[]
def keyForSorted(a):
	global globalLiterals
	return -globalLiterals[a]

def chainRxn(dynamicOri, chosenOri, lengthOri, stack):
	global lite
	a=time.time()
	dynamic = [row[:] for row in dynamicOri]
	chosen = chosenOri[:]
	length = [row[:] for row in lengthOri]

	while len(stack)>0:
		templit = stack.pop()
		chosen.append(templit)
		check = 0
		removal_log = []
		for i in range(len(length)):
 
			if templit in dynamic[length[i][0]]:
				removal_log.append(length[i])
 
			elif -1*templit in dynamic[length[i][0]]:
				dynamic[length[i][0]].remove(-1*templit)	#always false literal in that branch of tableaux
				length[i][1]=length[i][1]-1
				if length[i][1]==1:
					stack.append(dynamic[length[i][0]][0])
				if length[i][1]==0:
						return 0,0,0
 
		stack = list(set(stack))
		for l in range(len(removal_log)):
			length.remove(removal_log[l])
 
	if len(length) == 0:
		chosen=sorted(chosen, key=abs)
		#print(chosen)
		print(decomp)
		print("--- %s seconds ---" % (time.time() - start_time))
		file.write("SAT\n")
		for ctr in range(lite):
			if -(ctr+1) in chosen:
				file.write("%d "%-(ctr+1))
			else:
				file.write("%d "%(ctr+1))

		file.write("0\n")
		file.close()
		exit()
 
	return dynamic, chosen, length
 
def solve(dynamicOri, chosenOri, lengthOri, literalsOri):

	global clau, data, decomp, globalLiterals,tst
	
 
	if len(lengthOri)<1:
		chosenOri=sorted(chosenOri, key=abs)
		#print(chosenOri)
		print(decomp)
		file.write("SAT\n")
		for ctr in range(lite):
			if -(ctr+1) in chosenOri:
				file.write("%d "%-(ctr+1))
			else:
				file.write("%d "%(ctr+1))

		file.write("0\n")
		file.close()
		print("--- %s seconds ---" % (time.time() - start_time))
		exit()
 
	mistake = []
 	
	for j in range(lengthOri[0][1]):
		decomp+=1
		aa=time.time()
		dynamic = [row[:] for row in dynamicOri]
		chosen = chosenOri[:]
		literals = dict(literalsOri)	
		length = [row[:] for row in lengthOri]
		lendyn = len(dynamic)
		for l in range(len(mistake)):
			dynamic.append([-mistake[l]])
			length.append([lendyn+l,1])
 
		templit = dynamic[length[0][0]][j]
		chosen.append(templit)
		check=0
 
		removal_log=[]
		stack = []
		for i in range(len(length)):

			if templit in dynamic[length[i][0]]:
				removal_log.append(length[i])
			elif -1*templit in dynamic[length[i][0]]:
				dynamic[length[i][0]].remove(-1*templit)	#always false literal in that branch of tableaux
				literals[-templit]-=1
				length[i][1]=length[i][1]-1
				if length[i][1]==1:
					stack.append(dynamic[length[i][0]][0])
				if length[i][1]==0:
						check=1
						break

		if check==1:
			mistake.append(templit)
			continue

		for l in range(len(removal_log)):
			for k in dynamic[removal_log[l][0]]:
				literals[k]-=1
			length.remove(removal_log[l])

		stack = list(set(stack))
		dynamic, chosen, length = chainRxn(dynamic, chosen, length, stack)

		globalLiterals = literals
 
		if dynamic == 0:
			mistake.append(templit)
			continue
		t111 = time.time()
		for i in range(len(length)):
			dynamic[length[i][0]]=sorted(dynamic[length[i][0]], key=keyForSorted)
		tst= time.time()-t111+ tst
		if check==0:
			length = sorted(length, key=operator.itemgetter(1))
			solve(dynamic, chosen, length, literals)
 
with open("input.txt") as f:
 
	lite=-1	#number of literals
	clau=-1	#number of clauses
	data=[]
	literalsp = []
	literalsn = []
	check = 0
 
	for line in f:
		if line[0]=='c' or (line[0]=='p' and check == 1):
			pass
		elif line[0]=='p' and check == 0:
			check =1 
			arr=line.split()
			if arr[1]!='cnf':
				print ("Not in cnf form.")
				exit()
 
			lite =	 int(arr[2])
			literalsp = [0 for i in range(lite+1)]
			literalsn = [0 for i in range(lite+1)]
			clau = int(arr[3])
		else:
			clause=list(map(int,line.split()))
			clause.remove(0)
 
			clause=list(set(clause))
			modclause=[]
 
			for lit in clause:
				modclause.append(abs(lit))
 
			if len(modclause) != len(set(modclause)):
				clau-=1
				continue
 
			data.append(clause)
 
			for lit in clause:
				if lit<0:
					literalsn[abs(lit)]+=1
				else:
					literalsp[lit]+=1
 
	chosen=[]	#the chosen ones
 
	literals = {}
 
	for i in range(1,len(literalsp)):
		literals[i]=literalsp[i]
	for i in range(1, len(literalsn)):
		literals[-i]=literalsn[i]
  
	length = []
 
	for i in range(clau):
		length.append([i,len(data[i])])
 
	length = sorted(length, key=operator.itemgetter(1))

	globalLiterals = literals
	for i in range(len(data)):
		data[i]=sorted(data[i], key=keyForSorted)
 
	dynamic = [row[:] for row in data]

	solve(dynamic, chosen, length, literals)
 
	print("NO SOLUTION")
	print(decomp)
	file.write("UNSAT")

	file.close()