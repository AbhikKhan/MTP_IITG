'''
Created on 11-Jul-2017
@author: sukanta
'''
import networkx as nx

def getAssignment(filename, varIndex):    
    fp = open(filename,'r')
    for line in fp.readlines():
        (var,_,truthValue) = line.split()
        if var[0] != 't':
            varIndex[var] = int(truthValue) 

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
    varIndex = dict()
    getAssignment(filename, varIndex)
    seqGraph = nx.DiGraph()
    reagentNodeId = [5001,5002]
    # Add nodes for each reagents
    for i in range(2):
        R = [0,0]
        R[i] = factorWeight(factorList,0,d-1)
        seqGraph.add_node(reagentNodeId[i], ratio = R[:])
    # Create internal nodes
    for i in range(1,d+1):
        R = [0,0]
        varString = "X" + str(i) 
        R[0] = varIndex[varString]
        varString = "Y" + str(i) 
        R[1] = varIndex[varString]
        # Create node i
        seqGraph.add_node(i, ratio = R[:])
    # Create relevant edges
    for i in range(1,d+1):
        varString = "x" + str(i) 
        if varIndex[varString] != 0:
            seqGraph.add_edge(reagentNodeId[0],i)
            seqGraph[reagentNodeId[0]][i]['usedSegment'] = varIndex[varString]
        varString = "y" + str(i) 
        if varIndex[varString] != 0:
            seqGraph.add_edge(reagentNodeId[1],i)
            seqGraph[reagentNodeId[1]][i]['usedSegment'] = varIndex[varString]
    for i in range(2,d+1):
        for j in range(1,i):
            varString = "w" + str(i) + str(j)
            if varIndex[varString] != 0:
                seqGraph.add_edge(i,j)
                seqGraph[i][j]['usedSegment'] = varIndex[varString] 
        
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
        fp.write('%s [label = "%s",  shape = oval]\n' %(v,str(graph.node[v]['ratio'])))
        
    fp.write('}\n')          
    fp.close()    
    



factorList = [4,4,4]

#factorList = [2,5,5,2]

d = len(factorList)
seqGraph = genSeqGraph('op',factorList,d)
printGraph(seqGraph,'op.dot')