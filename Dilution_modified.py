"""
Created on 04-Sep-2015
@author: sukanta
"""
import subprocess

subprocess.call(["rm", "z3Optimizer.py"])
opfile = open("z3Optimizer.py", "w+")

__Id = 1


def init():
    # ===============================================================================
    # init() appends the initial conditions for the z3 solver to analyze the clauses
    # ===============================================================================
    opfile.write("import sys\n")
    opfile.write("import time\n")
    opfile.write('sys.path.append("/home/sukanta/App/z3/bin")\n')
    opfile.write("from z3 import *\n\n")
    opfile.write("def getOptimizer(r11, r12):\n")
    opfile.write("\ts=Optimize()\n")


def finish():
    opfile.write("for r in range(1, 128):\n")
    opfile.write("\tgetOptimizer(256-r, r)")
    opfile.close()


def varDeclare(N, d, n):
    # ===============================================================================
    # N: Mixer-N, d: depth of skewed tree, n: no_of_reagents i.e., R1, R2, . . ., Rn
    # ===============================================================================
    for i in range(1, d + 1):
        opString = "\t"
        for j in range(1, n + 1):
            opString += f"R{i}{j}, "
        for j in range(1, n + 1):
            opString += f"x{i}{j}, "
        # adding loading variable
        for j in range(1, n + 1):
            opString += f"L{i}{j}, "
        opString = opString[:-2]
        opString += " = Ints('"
        for j in range(1, n + 1):
            opString += f"R{i}{j} "
        for j in range(1, n + 1):
            opString += f"x{i}{j} "
        # adiing loading variable
        for j in range(1, n + 1):
            opString += f"L{i}{j} "
        opString = opString[:-1]
        opString += "')\n"
        opfile.write(opString)
    # Declare variables for weights
    for i in range(2, d + 1):
        if i == 2:  # Special processing
            opfile.write("\tw21 = Int('w21')\n")
        else:
            opString = "\t"
            for j in range(1, i):
                opString += f"w{i}{j}, "
            opString = opString[:-2]
            opString += " = Ints('"
            for j in range(1, i):
                opString += f"w{i}{j} "
            opString = opString[:-1]
            opString += "')\n"
            opfile.write(opString)
    opfile.write("\n\n")


def getNewTempVar():
    # Returns a new temporary variable
    global __Id
    newVar = "t" + str(__Id)
    __Id = __Id + 1
    return newVar


def ratioConsistencyConstraintsWithLinerarization(N, d, n):
    # ===============================================================================
    # N: Mixer-N, d: depth of skewed tree, n: no_of_reagents i.e., R1, R2, . . ., Rn
    # Nonlinear constraints are generated
    # ===============================================================================
    for i in range(1, d + 1):
        for j in range(1, n + 1):
            newVarDict = dict()
            opString = f"\ts.add({N**(d-i)}*x{i}{j}"
            for k in range(i + 1, d + 1):
                R = f"R{k}{j}"
                W = f"w{k}{i}"
                t = getNewTempVar()
                newVarDict[t] = (R, W)
                opString += f" + {N**(k-i-1)}*" + t
            # print newVarDict
            opString += f" == R{i}{j})\n"
            if (
                i == d
            ):  # For last level no temp variable is required hence len(newVarDict) == 0
                opfile.write(opString)
            # Write Linearisation constraints
            if len(newVarDict) > 0:
                # Declare variables
                varDecStr = "\t"
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
                opfile.write(varDecStr)
                # Write ratio consistency constraint
                opfile.write(opString)
                # Declare constraints
                for t in newVarDict.keys():
                    (R, W) = newVarDict[t]
                    opString = "\ts.add(Implies((" + W + " == 0), (" + t + " == 0)))\n"
                    opfile.write(opString)
                    for loopVar in range(1, N + 1):
                        opString = (
                            "\ts.add(Implies(("
                            + W
                            + f" == {loopVar}), ("
                            + t
                            + f" == {loopVar}*"
                            + R
                            + ")))\n"
                        )
                        opfile.write(opString)
                opfile.write("\n")

    opfile.write("\n\n")


def ratioConsistencyConstraints(N, d, n):
    # ===============================================================================
    # N: Mixer-N, d: depth of skewed tree, n: no_of_reagents i.e., R1, R2, . . ., Rn
    # Nonlinear constraints are generated
    # ===============================================================================
    for i in range(1, d + 1):
        for j in range(1, n + 1):
            opString = f"\ts.add({N**(d-i)}*x{i}{j}"
            for k in range(i + 1, d + 1):
                opString += f" + {N**(k-i-1)}*R{k}{j}*w{k}{i}"
            opString += f" == R{i}{j})\n"
            opfile.write(opString)
    opfile.write("\n\n")


def mixerConsistencyConstraints(N, d, n):
    for i in range(1, d + 1):
        opString = "\ts.add("
        for j in range(1, n + 1):
            opString += f"x{i}{j} + "
        opString = opString[:-2]
        for j in range(i + 1, d + 1):
            opString += f" + w{j}{i}"
        opString += f" == {N})\n"
        opfile.write(opString)
    opfile.write("\n\n")
    for i in range(2, d + 1):
        opString = "\ts.add("
        for j in range(1, i):
            opString += f"w{i}{j} + "
        opString = opString[:-2]
        opString += f" <= {N})\n"
        opfile.write(opString)
    opfile.write("\n\n")


# Need to be modified: Add x??, w?? <= N
def nonNegativityConstraints(N, d, n):
    for i in range(1, d + 1):
        opString = "\ts.add(And("
        for j in range(1, n + 1):
            opString += f"R{i}{j} >= 0, "
        for j in range(1, n + 1):
            opString += f"x{i}{j} >= 0, " + f"x{i}{j} <= {N-1}, "

        opString = opString[:-2]
        opString += "))\n"
        opfile.write(opString)
    for i in range(2, d + 1):
        if i == 2:
            opfile.write("\ts.add(w21 >= 0)\n")
        else:
            opString = "\ts.add(And("
            for j in range(1, i):
                if i - j <= 2:
                    opString += f"w{i}{j} >= 0, w{i}{j} <= {N-1}, "
                else:
                    opString += f"w{i}{j} == 0, "
            opString = opString[:-2]
            opString += "))\n"
            opfile.write(opString)
    opfile.write("\n\n")

    # new constraints for current node and grand-parent sharing
    for i in range(2, d + 1):
        # as only node-grand-parent sharing is considered
        opString = ""
        if i == 2:
            opString += f"\ts.add(If(w{i}{i-1} == {N-1}, w{i+1}{i-1} == 0, And(w{i+1}{i-1} >= 0, w{i+1}{i-1} <= 3)))\n"
        elif i == d:
            opString += f"\ts.add(If(w{i}{i-1} == {N-1}, w{i}{i-2} == 0, And(w{i}{i-2} >= 0, w{i}{i-2} <= 3)))\n"
        else:
            opString += f"\ts.add(If(w{i}{i-1} == {N-1}, And(w{i+1}{i-1} == 0, w{i}{i-2} == 0), And(w{i+1}{i-1} >= 0, w{i+1}{i-1} <= 3, w{i}{i-2} >= 0, w{i}{i-2} <= 3)))\n"
        opfile.write(opString)
    opfile.write("\n\n")


# to add loading constraints
def loadingConstraints(N, d, n):
    opString = ""
    for i in range(1, d + 1):
        # if xij == 1 Lij = 1 else Lij = 0
        opString += f"\ts.add(If(x{i}1 >= 1, L{i}1 == 1, L{i}1 == 0))\n"
        opString += f"\ts.add(If(x{i}2 >= 1, L{i}2 == 1, L{i}2 == 0))\n"
    opfile.write(opString)
    opfile.write("\n")


def setTarget(ratio):
    opString = "\ts.add(And(R11 == r11, R12 == r12))\n"
    opString += "\n"
    opfile.write(opString)


def optimizationCriteria(N, d, n):
    # adding optimization criteria
    opString = f"\tsampleLoading = s.minimize("
    for i in range(1, d + 1):
        opString += f"L{i}1+"
    opString = opString[0:-1]
    opString += ")\n"
    opfile.write(opString)
    opString = f"\tbufferLoading = s.minimize("
    for i in range(1, d + 1):
        opString += f"L{i}2+"
    opString = opString[0:-1]
    opString += ")\n"
    opfile.write(opString)
    opfile.write("\n")


def checkForSat():
    opfile.write(
        "\tfp = open(f'/home/sparrow/Desktop/MTP/Codes/MTP_IITG/output/op{r12}','w')\n"
    )
    # opfile.write('\tfp = open(f\'/home/sparrow/Desktop/IITG/MTP/Codes/MTP_IITG/output/op{r}\',\'w\')\n')
    opfile.write("\tif s.check() == unsat:\n")
    opfile.write("\t\tprint ('unsat')\n")
    opfile.write("\telse:\n")
    opfile.write("\t\tprint ('sat')\n")
    opfile.write("\t\ts.lower(sampleLoading)\n")
    opfile.write("\t\tlst = s.model()\n")
    opfile.write("\t\tfor i in lst:\n")
    opfile.write("\t\t\tfp.write(str(i) + \" = \" + str(s.model()[i]) + '\\n')\n\n\n")


def OSP(ratio, N, d):
    n = len(ratio)
    if sum(ratio) != N**d:
        print("Error !!")
    init()
    varDeclare(N, d, n)
    # ratioConsistencyConstraints(N,d,n)
    ratioConsistencyConstraintsWithLinerarization(N, d, n)
    mixerConsistencyConstraints(N, d, n)
    nonNegativityConstraints(N, d, n)
    loadingConstraints(N, d, n)
    setTarget(ratio)
    optimizationCriteria(N, d, n)
    checkForSat()
    finish()


# (N,d,n)=(4,4,7)
# OSP((4,6,10,14,22,26,174),N,d)
# (N,d,n)=(4,3,4)
# OSP((19,15,15,15),N,d)

(N, d, n) = (4, 4, 2)
# OSP((47,17),N,d)
OSP((199, 57), N, d)


"""
#-----------------------------------------------------------
#            Testing for all ratios
#-----------------------------------------------------------
def genPartitions(n,m):
    partitions = []
    #H1
    a = [1 for i in range(m+2)]
    a[1] = n-m+1
    for j in range(2,m+1):
        a[j] = 1
    a[m+1] = -1
    # H2 - H3
    while True:    
        partitions.append(a[1:-1])
        #print a[1:-1]    
        if not(a[2] >= a[1] - 1):
            a[1] = a[1] - 1
            a[2] = a[2] + 1
            continue
        
        # H4
        j = 3
        s = a[1] + a[2] - 1
        while(a[j] >= a[1] - 1):
            s = s + a[j]
            j = j + 1
        # H5
        if j > m:
            return partitions
        else:
            x = a[j] + 1
            a[j] = x
            j = j - 1
        # H6
        while j > 1:
            a[j] = x
            s = s - x
            j = j - 1
        a[1] = s

#-------------------------main()----------------------     
allPartitions = genPartitions(64,4)   
for partition in allPartitions:
    (N,d,n) = (4,3,4)
    OSP(partition, N, d)
    print partition,
    subprocess.call(["python","OSP_clauses.py"])
    subprocess.call(["rm","OSP_clauses.py"])
    opfile = open("OSP_clauses.py","w+")
"""
