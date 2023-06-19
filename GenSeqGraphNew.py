import os
import GraphGen

inputPath = '/home/sparrow/Desktop/MTP/Codes/MTP_IITG/output/'
outputPath = '/home/sparrow/Desktop/MTP/Codes/MTP_IITG/outputTrees/'
os.chdir(inputPath)
d = 4

for file in os.listdir():
    GraphGen.generateGraph(4, inputPath+file, outputPath+file+'.dot')