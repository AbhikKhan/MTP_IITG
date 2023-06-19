'''
Created on 11-Jul-2017
@author: sukanta
'''

import subprocess
import itertools        # generating permutations
from subprocess import Popen, PIPE

from functools import reduce


__Id = 1

def getNewTempVar():
    # Returns a new temporary variable
    global __Id
    newVar = "t"+str(__Id)
    __Id = __Id + 1
    return newVar

def initOPT(opFile):
#===============================================================================
# init() appends the initial conditions for the z3 solver to analyze the clauses
#===============================================================================
    opFile.write("import sys\n")
    opFile.write("import time\n")
    opFile.write("sys.path.append(\"/home/sukanta/App/z3-master/build\")\n")
    opFile.write("from z3 import *\n\n")
    opFile.write("s = Optimize()\n")
    #opFile.write("s.set(priority='pareto')\n")
    
def finishOPT(opFile,d,factorList):
    #opString = "storage = s.minimize(s1)\n"
    #opFile.write(opString)
    
    opString = "sample = s.minimize("
    for i in range(1,d+1):
        opString += f"x{i} + "
    opString = opString[:-3] + ")\n"
    opFile.write(opString)
    
    opString = "buff = s.minimize("
    for i in range(1,d+1):
        opString += f"y{i} + "
    opString = opString[:-3] + ")\n"
    opFile.write(opString)
        
    opFile.write("startTime = time.time()\n")
    opFile.write("print (s.check())\n")
    #opFile.write("while s.check() == sat:\n")
    #opFile.write("    print \"sample = \", sample.value(), \"buffer = \", buff.value()\n")
    opFile.write("print (\"sample = \", sample.value(), \"buffer = \", buff.value())\n")
    opFile.write('endTime = time.time()\n')
    opFile.write('executionTime = endTime - startTime\n')
    opFile.write("print (\"Execution Time = \",executionTime)\n")
    #For printing SAT assignments 
    opFile.write("fp = open(\'op\',\'w\')\n")
    opFile.write("lst = s.model()\n")
    opFile.write("for i in lst:\n")
    opFile.write("    fp.write(str(i) + \" = \" + str(s.model()[i]) + '\\n')\n")    
     
    opFile.close()
    
    
def init(opFile):
#===============================================================================
# init() appends the initial conditions for the z3 solver to analyze the clauses
#===============================================================================
    opFile.write("import sys\n")
    opFile.write("import time\n")
    opFile.write("sys.path.append(\"/home/sukanta/App/z3/bin\")\n")
    opFile.write("from z3 import *\n\n")
    opFile.write("s=Solver()\n")
    
def finish(opFile,d,factorList):
    opFile.write('startTime = time.time()\n')
    opFile.write('sample = 1\n')
    opFile.write('while True:\n')
    opFile.write('    s.push()\n')
    opString = "    " + "s.add("
    for i in range(1,d+1):
        opString += "x" + str(i) + " + "
    opString = opString[:-3] + " == sample)\n"
    opFile.write(opString)
    opFile.write('    if s.check() == unsat:\n') 
    opFile.write('        s.pop()\n')
    opFile.write('        sample = sample + 1\n')
    opFile.write('    else:\n')
    opFile.write('        break\n')
    opFile.write('endTime = time.time()\n')
    opFile.write('executionTime = endTime - startTime\n')
    #opFile.write("print (\"Execution Time = \",executionTime)\n")
    opString = "buff = "
    for i in range(1,d+1):
        opString += "int(s.model()[y" + str(i) + "].as_string()) +"
    opString = opString[:-1]+"\n"
    opFile.write(opString)
    opFile.write("for b in range(1,buff+1):\n")   #b = number of buffer
    opFile.write('    s.push()\n')
    opString = "    " + "s.add("
    for i in range(1,d+1):
        opString += "y" + str(i) + " + "
    opString = opString[:-3] + " == b)\n"
    opFile.write(opString)
    opFile.write('    if s.check() == unsat:\n') 
    opFile.write('        s.pop()\n')
    opFile.write('    else:\n')
    opString = "buff = "
    for i in range(1,d+1):
        opString += "int(s.model()[y" + str(i) + "].as_string()) +"
    #mix = len(factorList)
    # waste,sample,b; mix can be found from normalized factor list
    opFile.write("        print \"%d %d %d \"%(sample+b-1,sample,b)\n") 
    opFile.write('        break\n')
    
    #For printing SAT assignments 
    opFile.write('fp = open(\'op\',\'w\')\n')
    opFile.write("lst = s.model()\n")
    opFile.write("for i in lst:\n")
    opFile.write("    fp.write(str(i) + \" = \" + str(s.model()[i]) + '\\n')\n")    
     
    opFile.close()
    
def varDeclare(opFile,d):
#===============================================================================
# d: depth of skewed tree
#===============================================================================
    for i in range(1,d+1):
        opString = ""
        opString += f"X{i}, Y{i}, x{i}, y{i}, s{i} = Ints('X{i} Y{i} x{i} y{i} s{i}')\n"
        opFile.write(opString)
    # Declare variables for weights
    for i in range(2,d+1):
        if i == 2:  # Special processing
            opFile.write("w21 = Int('w21')\n")
        else:
            opString = ""
            for j in range(1,i):
                opString += f"w{i}{j}, "
            opString = opString[:-2]
            opString += " = Ints('"
            for j in range(1,i):
                opString += f"w{i}{j} "
            opString = opString[:-1]
            opString += "')\n"
            opFile.write(opString)
    opFile.write('\n\n')
    
def factorWeight(List,i,j):
#===============================================================================
# List : list of factors, (i, j) : (start_index, end_index)
# returns (List[i]*List[i+1]*...*List[j])
#===============================================================================  
    #print List, i, j
    tmp = 1
    for t in range(i,j+1):
        tmp *= List[t]
    
    return tmp  
    
def ratioConsistencyConstraintsWithLinerarization(opFile,factorList,d):
#===============================================================================
# factorList : list of factors, d: depth of skewed tree
# Nonlinear constraints are generated
#===============================================================================    
    # Create new factor list starting index from 1 and reverse of the original factorList
    newFactorList = []
    for factor in factorList:
        newFactorList.insert(0,factor)
    newFactorList.insert(0,factor)
    #print newFactorList
    
    # For reagent x_i
    for i in range(1,d+1):
        newVarDict = dict()
        opString = "s.add(" + str(factorWeight(newFactorList,i+1,d)) + f"*x{i}" 
        for k in range(i+1,d+1):
            X = f'X{k}' 
            W = f'w{k}{i}'
            t = getNewTempVar()
            newVarDict[t] = (X,W,newFactorList[k])
            opString += " + " + str(factorWeight(newFactorList,i+1,k-1)) + "*" + t
            #print newVarDict
        opString += f" == X{i})\n"
        
        # For last level no temp variable is required hence len(newVarDict) == 0
        if i == d:      
            opFile.write(opString)
            
        # Write linearization constraints
        if len(newVarDict) > 0:
            # Declare variables
            varDecStr = ""
            for t in newVarDict.keys():
                varDecStr += t + ", "
            varDecStr = varDecStr[:-2]
            if len(newVarDict) == 1:
                varDecStr += " = Int('"
            else:
                varDecStr += " = Ints('"
            for t in newVarDict.keys():
                varDecStr += t + " "
            varDecStr = varDecStr[:-1]
            varDecStr += "')\n"
            opFile.write(varDecStr) 
            # Write ratio consistency constraint
            opFile.write(opString)
            # Declare constraints
            for t in newVarDict.keys():
                (R,W,F) = newVarDict[t]
                opString = 's.add(Implies((' + W + ' == 0), (' + t + " == 0)))\n"
                opFile.write(opString)
                for loopVar in range(1,F):
                    opString = 's.add(Implies((' + W + f' == {loopVar}), (' + t  \
                                                     + f' == {loopVar}*' + R + ')))\n'
                    opFile.write(opString)  
            opFile.write('\n')            
    
    opFile.write('\n')     
    
    # For reagent y_i
    for i in range(1,d+1):
        newVarDict = dict()
        opString = "s.add(" + str(factorWeight(newFactorList,i+1,d)) + f"*y{i}" 
        for k in range(i+1,d+1):
            Y = f'Y{k}' 
            W = f'w{k}{i}'
            t = getNewTempVar()
            newVarDict[t] = (Y,W,newFactorList[k])
            opString += " + " + str(factorWeight(newFactorList,i+1,k-1)) + "*" + t
            #print newVarDict
        opString += f" == Y{i})\n"
        
        
        if i == d:      # For last level no temp variable is required hence len(newVarDict) == 0
            opFile.write(opString)
            
        # Write Linearisation constraints
        if len(newVarDict) > 0:
            # Declare variables
            varDecStr = ""
            for t in newVarDict.keys():
                varDecStr += t + ", "
            varDecStr = varDecStr[:-2]
            if len(newVarDict) == 1:
                varDecStr += " = Int('"
            else:
                varDecStr += " = Ints('"
            for t in newVarDict.keys():
                varDecStr += t + " "
            varDecStr = varDecStr[:-1]
            varDecStr += "')\n"
            opFile.write(varDecStr) 
            # Write ratio consistency constraint
            opFile.write(opString)
            # Declare constraints
            for t in newVarDict.keys():
                (R,W,F) = newVarDict[t]
                opString = 's.add(Implies((' + W + ' == 0), (' + t + " == 0)))\n"
                opFile.write(opString)
                for loopVar in range(1,F):
                    opString = 's.add(Implies((' + W + f' == {loopVar}), (' + t  \
                                                     + f' == {loopVar}*' + R + ')))\n'
                    opFile.write(opString)  
            opFile.write('\n')                
    opFile.write("\n\n")
    
            
def mixerConsistencyConstraints(opFile,factorList,d):
    # Create new factor list starting index from 1 and reverse of the original factorList
    newFactorList = []
    for factor in factorList:
        newFactorList.insert(0,factor)
    newFactorList.insert(0,factor)
    
    for i in range(1,d+1):
        opString = "s.add("
        opString += f"x{i} + y{i}" 
        for j in range(i+1,d+1):
            opString += f" + w{j}{i}"
        opString += f" == {newFactorList[i]})\n"
        opFile.write(opString) 
    opFile.write("\n\n")
    for i in range(2,d+1):
        opString = "s.add("
        for j in range(1,i):
            opString += f"w{i}{j} + "
        opString = opString[:-2]
        opString += f" <= {newFactorList[i]})\n"
        opFile.write(opString) 
    opFile.write("\n\n")  
    
def nonNegativityConstraints(opFile,factorList,d):
    # Create new factor list starting index from 1 and reverse of the original factorList
    newFactorList = []
    for factor in factorList:
        newFactorList.insert(0,factor)
    newFactorList.insert(0,factor)
    
    for i in range(1,d+1):
        opString = "s.add(And("
        opString += f"X{i} >= 0, Y{i} >= 0, "
        opString += f"x{i} >= 0, x{i} <= {newFactorList[i]-1}, "
        opString += f"y{i} >= 0, y{i} <= {newFactorList[i]-1}, "
        opString = opString[:-2]
        opString += "))\n"
        opFile.write(opString)
    for i in range(2,d+1):
        opString = "s.add(And("
        for j in range(1,i):
            opString += f"w{i}{j} >= 0, w{i}{j} <= {newFactorList[i]-1}, "
        opString = opString[:-2]
        opString += "))\n"
        opFile.write(opString) 
    # Preserver the height of the dilution tree
    '''opString = "\n\ns.add(And("
    for i in range(2,d+1):        
        opString += "w"+str(i)+str(i-1)+ " >= 1, "
    opString = opString[:-2] + "))\n"
    opFile.write(opString)
    opFile.write("\n\n")'''
        
def storageConstraint(opFile, d, k):
    opString = f"s.add(s{d} == 0)\n"
    opFile.write(opString)
    for i in range(d-1,0,-1):
        opString = f"s.add(s{i} == s{i+1} + "
        for j in range(i+2,d+1):
            opString += f"w{j}{i} + "
        opString = opString[:-2] + ")\n"
        opFile.write(opString)
    opFile.write(f"s.add(s1 <= {k})\n")

def setTarget(opFile,ratio):
    opString = "s.add(And("
    opString += f"X1 == {ratio[0]}, Y1 == {ratio[1]}"
    opString += "))\n\n\n"
    opFile.write(opString)


#----------------------main()------------------
def normalize(ratioList,factorList):
    newRatioList = ratioList[:]
    newFactorList = []
    for i in range(len(factorList)):
        if newRatioList[0]%factorList[i] == 0 and newRatioList[1]%factorList[i] == 0:
            newRatioList[0] = newRatioList[0]/factorList[i]
            newRatioList[1] = newRatioList[1]/factorList[i]
        else:
            newFactorList.append(factorList[i])        
    
    return newRatioList,newFactorList

def dilution(ratioList,factorList):
    print ('Original ratio: ',ratioList, )
    newRatioList,newFactorList = normalize(ratioList,factorList)
    if reduce(lambda x, y: x*y, newFactorList) != sum(newRatioList):
        print ("Error!!")
        return None
    
    print ('Normalized ratio: ',newRatioList, 'Factor list: ', newFactorList  )
    opDict = dict()
    d = len(newFactorList)
    if d == 1: #Don't need to call SMT
        factor = newFactorList[0]
        #(factor,) is an one element tuple 
        opDict[(factor,)] = (1,factor-1,newRatioList[0],newRatioList[1])
    else:    #Generate SMT file
        subprocess.call(["rm","clauses.py"])
        opFile = open("clauses.py","w+")
        init(opFile)
        varDeclare(opFile,d)
        ratioConsistencyConstraintsWithLinerarization(opFile,newFactorList,d)
        mixerConsistencyConstraints(opFile,newFactorList,d)
        nonNegativityConstraints(opFile,newFactorList,d)  
        setTarget(opFile,newRatioList)
        finish(opFile,d,newFactorList)
        mix = len(newFactorList)        
        # Run 'clauses.py' and get its parameters (waste,sample buffer)
        #subprocess.call(["python3","clauses.py"])
        process = Popen(["python3","clauses.py"], stdout=PIPE)
        # Get SMT output
        (output, _) = process.communicate()
        [waste,sample,buff] = [int(x) for x in output.split()]
        #print (output,error)
        opDict[tuple(newFactorList)] = (mix,waste,sample,buff)
        #print mix,waste,sample,buff
    
    return opDict      






# Using optimizing SMT
ratioList = [199,57]
factorList = [4,4,4,4]

# ratioList = [47,17]
# factorList = [4,4,4]

d = len(factorList)
subprocess.call(["rm","clauses.py"])
opFile = open("clauses.py","w+")
print (factorList, ': ',)
initOPT(opFile)
varDeclare(opFile,d)
ratioConsistencyConstraintsWithLinerarization(opFile,factorList,d)
mixerConsistencyConstraints(opFile,factorList,d)
nonNegativityConstraints(opFile,factorList,d)  
storageConstraint(opFile, d, 2)
setTarget(opFile,ratioList)
finishOPT(opFile,d,factorList)

        
# Run 'clauses.py'
subprocess.call(["python3","clauses.py"])
# sout = subprocess.check_output(["python3","clauses.py"])
# print("output: ", sout)


