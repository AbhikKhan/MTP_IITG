'''
Created on 18-Jul-2017
@author: sukanta
'''

import subprocess
import networkx as nx
__Id = 1

runtime = 0.0

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
        opString += "x" + str(i) + " + "
    opString = opString[:-3] + ")\n"
    opFile.write(opString)
    
    opString = "buff = s.minimize("
    for i in range(1,d+1):
        opString += "y" + str(i) + " + "
    opString = opString[:-3] + ")\n"
    opFile.write(opString)
        
    opFile.write("startTime = time.time()\n")
    opFile.write("s.check()\n")
    #opFile.write("while s.check() == sat:\n")
    #opFile.write("    print \"sample = \", sample.value(), \"buffer = \", buff.value()\n")
    opFile.write('endTime = time.time()\n')
    opFile.write("print(\"sample = \", sample.value(), \"buffer = \", buff.value())\n")
    opFile.write('executionTime = endTime - startTime\n')
    opFile.write("print(\"Execution Time = \",executionTime)\n")
    #For printing SAT assignments 
    opFile.write("fp = open(\'opNew\',\'w\')\n")
    opFile.write("fp.write(\'time = %f\\n\'%executionTime)\n")
    opFile.write("lst = s.model()\n")
    opFile.write("for i in lst:\n")
    opFile.write("    fp.write(str(i) + \" = \" + str(s.model()[i]) + '\\n')\n")    
     
    opFile.close()    
    
    
def varDeclare(opFile,d):
#===============================================================================
# d: depth of skewed tree
#===============================================================================
    for i in range(1,d+1):
        opString1 = ""
        opString2 = ""
        opString1 += "X" + str(i) + ", " + "Y" + str(i) 
        opString1 += " = Reals('" + "X" + str(i) + " " + "Y" + str(i) + "')\n"
        opFile.write(opString1)
        
        opString2 += "x" + str(i) + ", " + "y" + str(i) + ", " + "s" + str(i) 
        opString2 += " = Ints('" + "x" + str(i) + " " + "y" + str(i) + " " + "s" + str(i) + "')\n"
        opFile.write(opString2)
    # Declare variables for weights
    for i in range(2,d+1):
        if i == 2:  # Special processing
            opFile.write("w21 = Int('w21')\n")
        else:
            opString = ""
            for j in range(1,i):
                opString += "w" + str(i) + str(j) + ", "
            opString = opString[:-2]
            opString += " = Ints('"
            for j in range(1,i):
                opString += "w" + str(i) + str(j) + " "
            opString = opString[:-1]
            opString += "')\n"
            opFile.write(opString)
    opFile.write('\n\n')
    
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
        #--------------------New constraint-------------------------
        # Add Xi + Yi = 1 for each mixing node
        opString = "s.add(X" + str(i) + " + Y" +str(i) + " <= 1)\n"
        opFile.write(opString)
        #------------------------------------------------------------
        newVarDict = dict()
        opString = "s.add(x" + str(i) 
        for k in range(i+1,d+1):
            X = 'X' + str(k) 
            W = 'w' + str(k) + str(i)
            t = getNewTempVar()
            newVarDict[t] = (X,W,newFactorList[k])
            opString += " + " + t
            #print newVarDict
        opString += " == " + str(newFactorList[k]) + "*X" + str(i) + ")\n"
        
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
                varDecStr += " = Real('"
            else:
                varDecStr += " = Reals('"
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
                    opString = 's.add(Implies((' + W + ' == ' + str(loopVar) + '), (' + t  \
                                                     + ' == ' + str(loopVar) + '*' + R + ')))\n'
                    opFile.write(opString)  
            opFile.write('\n')            
    
    opFile.write('\n')     
    
    # For reagent y_i
    for i in range(1,d+1):
        newVarDict = dict()
        opString = "s.add(y" + str(i) 
        for k in range(i+1,d+1):
            Y = 'Y' + str(k) 
            W = 'w' + str(k) + str(i)
            t = getNewTempVar()
            newVarDict[t] = (Y,W,newFactorList[k])
            opString += " + " + t
            #print newVarDict
        opString += " == " + str(newFactorList[k]) + "*Y" + str(i) + ")\n"
        
        
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
                varDecStr += " = Real('"
            else:
                varDecStr += " = Reals('"
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
                    opString = 's.add(Implies((' + W + ' == ' + str(loopVar) + '), (' + t  \
                                                     + ' == ' + str(loopVar) + '*' + R + ')))\n'
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
        opString += "x" + str(i) + " + " + "y" + str(i) 
        for j in range(i+1,d+1):
            opString += " + w" + str(j) + str(i)
        opString += " == " + str(newFactorList[i]) + ")\n"
        opFile.write(opString) 
    opFile.write("\n\n")
    for i in range(2,d+1):
        opString = "s.add("
        for j in range(1,i):
            opString += "w" + str(i) + str(j) + " + "
        opString = opString[:-2]
        opString += " <= " + str(newFactorList[i]) + ")\n"
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
        opString += "X" + str(i) + " >= 0, " + "Y" + str(i) + " >= 0, "
        opString += "x" + str(i) + " >= 0, " + "x" + str(i) + " <= " + str(newFactorList[i]-1) + ", "
        opString += "y" + str(i) + " >= 0, " + "y" + str(i) + " <= " + str(newFactorList[i]-1) + ", "
        opString = opString[:-2]
        opString += "))\n"
        opFile.write(opString)
    for i in range(2,d+1):
        opString = "s.add(And("
        for j in range(1,i):
            opString += "w" + str(i) + str(j) + " >= 0, " + "w" + str(i) + str(j) + " <= " + str(newFactorList[i]-1) + ", "
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
    opString = "s.add(s"+str(d)+ " == 0)\n"
    opFile.write(opString)
    for i in range(d-1,0,-1):
        opString = "s.add(s" + str(i) + " == s" + str(i+1) + " + "
        for j in range(i+2,d+1):
            opString += "w"+str(j)+str(i) + " + "
        opString = opString[:-2] + ")\n"
        opFile.write(opString)
    opFile.write("s.add(s1 <= "+str(k)+ ")\n")

def setTarget(opFile,ratio):
    opString = "s.add(And("
    opString += "X1 == (1.0*" + str(ratio[0]) + ")/" + str(sum(ratio)) + ", Y1 == (1.0*" + str(ratio[1]) + ")/" + str(sum(ratio))
    opString += "))\n\n\n"
    opFile.write(opString)
    
#---------Generate sequencing graph for printing and storage computation----

def getAssignment(filename, varIndex):    
    fp = open(filename,'r')
    for line in fp.readlines():
        (var,_,truthValue) = line.split()
        if var[0] != 't':
            varIndex[var] = truthValue 
        if var == 'time':
            varIndex[var] = truthValue

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

def genSeqGraph(filename,factorList,d):
#===============================================================================
#  d: depth of skewed tree
#===============================================================================
    global runtime
    varIndex = dict()
    getAssignment(filename, varIndex)
    runtime  = float(varIndex['time'])
    seqGraph = nx.DiGraph()
    reagentNodeId = [5001,5002]
    # Add nodes for each reagents
    for i in range(2):
        R = [0,0]
        R[i] = 1
        seqGraph.add_node(reagentNodeId[i], ratio = R[:])
    # Create internal nodes
    for i in range(1,d+1):
        R = [0,0]
        varString = "X" + str(i) 
        X_i = varIndex[varString].split("/")
        R[0] = int(X_i[0])
        varString = "Y" + str(i) 
        Y_i = varIndex[varString].split("/")
        R[1] = int(Y_i[0])
        # Create node i
        seqGraph.add_node(i, ratio = R[:])
    # Create relevant edges
    for i in range(1,d+1):
        varString = "x" + str(i) 
        if varIndex[varString] != str(0):
            seqGraph.add_edge(i,reagentNodeId[0])
            seqGraph[i][reagentNodeId[0]]['usedSegment'] = int(varIndex[varString])
        varString = "y" + str(i) 
        if varIndex[varString] != str(0):
            seqGraph.add_edge(i,reagentNodeId[1])
            seqGraph[i][reagentNodeId[1]]['usedSegment'] = int(varIndex[varString])
    for i in range(2,d+1):
        for j in range(1,i):
            varString = "w" + str(i) + str(j)
            if varIndex[varString] != str(0):
                seqGraph.add_edge(j,i)
                seqGraph[j][i]['usedSegment'] = int(varIndex[varString]) 
        
    return seqGraph            
    
def printGraph(graph,filename):
    ''' Outputs the input sequencing graph in a file'''
    fp = open(filename,'w')
    string = 'digraph "DD" { \n' 
    fp.write(string)
    string = 'graph [ ordering = "out"];\n' 
    fp.write(string)
    for e in graph.edges():
        fp.write(str(e[0])+' -> '+str(e[1])+'[label = "%s"];\n' %(str(graph[e[0]][e[1]]['usedSegment'])))
        
    for v in graph.nodes():
        fp.write('%s [label = "%s",  shape = oval]\n' %(v,str(graph.nodes[v]['ratio'])))
        
    #fp.write('{rank = sink; 5001;5002}\n')
        
    fp.write('}\n')          
    fp.close()  
    
#----------- Calculate parameters -- mix, waste, sample, buffer--------------------
def calculateParameters(seqGraph,N):
    G = seqGraph.copy()
    
    sample = 0
    for (u,v) in G.in_edges(5001):
        sample = sample + G[u][v]['usedSegment']
    buff = 0
    for (u,v) in G.in_edges(5002):
        buff = buff + G[u][v]['usedSegment']
    
    # Removing reagent nodes
    G.remove_node(5001)
    G.remove_node(5002)
    
    mix = nx.number_of_nodes(G)
    
    waste = sample + buff - N
    
    # Calculate storage
    longestPath =  nx.dag_longest_path(G)
    #print longestPath, nx.number_of_nodes(G)
    longestPath.reverse()   # Process bottom-up
    storage = 0
    for i in range(1,len(longestPath)):
        for (u,v) in G.out_edges(longestPath[i]):
            if v != longestPath[i-1]:
                storage = storage + G.edges[u, v]['usedSegment']
        
        
    return (mix,waste,sample,buff,storage)
    
      


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


def dilution(ratioList,factorList,N,k):   #Number of storage = k
    newRatioList, newFactorList = normalize(ratioList,factorList)
    print(newRatioList, newFactorList)
    d = len(newFactorList)
    if d == 1:  # No need to call SMT
        (sample,buff) = newRatioList
        mix = 1
        waste = 0
        storage = 0
        print("sample = %d buffer = %d"%(sample,buff))
        return (mix,waste,sample,buff,storage)
            
    subprocess.call(["rm","clausesNewModeling.py"])
    opFile = open("clausesNewModeling.py","w+")
    print (newFactorList, ': ')
    initOPT(opFile)
    varDeclare(opFile,d)
    ratioConsistencyConstraintsWithLinerarization(opFile,newFactorList,d)
    mixerConsistencyConstraints(opFile,newFactorList,d)
    nonNegativityConstraints(opFile,newFactorList,d)  
    storageConstraint(opFile, d, k)
    setTarget(opFile,newRatioList)
    finishOPT(opFile,d,newFactorList)
      
    # Run 'clauses.py'
    subprocess.call(["python3","clausesNewModeling.py"])

    # Generate sequencing graph
    seqGraph = genSeqGraph('opNew',factorList,d)
    printGraph(seqGraph,'opNew.dot')
    (m,w,s,b,storage) =  calculateParameters(seqGraph,N)
    print ("mix = %d, waste = %d, sample = %d, buffer = %d, storage = %d"%(m,w,s,b,storage))
     
    return (m,w,s,b,storage)

def FloSPAD_allTarget(N,d,k,opFileName):
    opFile = open(opFileName, 'w')
    global runtime
    
    for i in range(1,2):
        # ratioList = [i, N**d-i]
        ratioList = [199, 57]
        factorList = [4 for j in range(d)]
        (m,w,s,b,storage) = dilution(ratioList,factorList,N,k)
        opFile.write("%d %d %d %d %d %d %f\n"%(i,m,w,s,b,storage,runtime))
    opFile.close()

# (N,d,k)= (4,4,100)
# FloSPAD_allTarget(N,d,k,'FLoSPAD_N4_D4')

'''
(N,d,k)= (4,4,1)
FloSPAD_allTarget(N,d,k,'FLoSPAD_N4_D5_k1')

(N,d,k)= (4,4,2)
FloSPAD_allTarget(N,d,k,'FLoSPAD_N4_D5_k2')

(N,d,k)= (4,4,3)
FloSPAD_allTarget(N,d,k,'FLoSPAD_N4_D5_k3')

(N,d,k)= (4,4,4)
FloSPAD_allTarget(N,d,k,'FLoSPAD_N4_D5_k4')

(N,d,k)= (4,4,5)
FloSPAD_allTarget(N,d,k,'FLoSPAD_N4_D5_k5')

(N,d,k)= (4,4,6)
FloSPAD_allTarget(N,d,k,'FLoSPAD_N4_D5_k6')
'''
    
(N,d,k)= (4,4,8)
FloSPAD_allTarget(N,d,k,'FLoSPAD_N4_D5_k8')




'''
N = 4
targetNumerator = 207
ratioList = [targetNumerator,256-targetNumerator]
factorList = [4,4,4,4]
dilution(ratioList,factorList,N,100)
'''

'''
# Using optimizing SMT
ratioList = [125,131]
factorList = [4,4,4,4]

d = len(factorList)
subprocess.call(["rm","clausesNewModeling.py"])
opFile = open("clausesNewModeling.py","w+")
print factorList, ': ',
initOPT(opFile)
varDeclare(opFile,d)
ratioConsistencyConstraintsWithLinerarization(opFile,factorList,d)
mixerConsistencyConstraints(opFile,factorList,d)
nonNegativityConstraints(opFile,factorList,d)  
storageConstraint(opFile, d, 6)
setTarget(opFile,ratioList)
finishOPT(opFile,d,factorList)

        
# Run 'clauses.py'
subprocess.call(["python3","clausesNewModeling.py"])
'''

