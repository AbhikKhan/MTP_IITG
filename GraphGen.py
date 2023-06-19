import subprocess

graph = []

for i in range(0, 5):
    graph.append({})
for line in open('/home/sparrow/Desktop/MTP/Codes/MTP_IITG/output/op57'):
    listWords = line.split(' ')
    # getting the first letter
    firstLetter = listWords[0][0]
    match firstLetter:
        case 'R' | 'x' | 'w':
            i, j = int(listWords[0][1]), int(listWords[0][2])
            graph[i][listWords[0]] = int(listWords[2])


subprocess.call(["rm","graph.dot"])
opfile = open("graph.dot","w+")
i = 0
r1 = 0
r2 = 0
opfile.write('digraph Tree{\n')
opfile.write('\trankdir="BT"\n')
for node in graph[1:]:
    i = i+1
    keys = node.keys()
    for key in keys:
        if (key[0] == 'w') & (node[key] != 0):
            if int(key[1]) - int(key[2]) > 1:
                opfile.write(f"\t{key[1]} -> {key[2]} [label = \"{node[key]}\", color = \"red\"];\n")
            elif int(key[1]) - int(key[2]) == 1:
                opfile.write(f"\t{key[1]} -> {key[2]} [label = \"{node[key]}\", color = \"black\"];\n")
        elif (key[0] == 'x') & (node[key] != 0):
            if(key[2] == '1'):
                opfile.write(f"\t{key} -> {key[1]} [label = \"{node[key]}\", color = \"blue\"];\n")
                opfile.write(f"\t{key} [label = \"sample\", shape = \"box\"];\n")
            else:
                opfile.write(f"\t{key} -> {key[1]} [label = \"{node[key]}\", color = \"green\"];\n")
                opfile.write(f"\t{key} [label = \"buffer\", shape = \"box\"];\n")
        elif key == f'R{i}1':
            r1 = node[key]
        elif key == f'R{i}2':
            r2 = node[key]
    opfile.write(f'\t{i} [label = \"{r1}:{r2}\"];\n')

opfile.write('}\n\n')
opfile.close()
