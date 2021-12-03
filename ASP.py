
import os
import time
import networkx as nx

def converter(fileName, graph):
    # Graph is produced from a file
    if fileName != None:
        #--------------------------------------------------------------------
        # Create list of nodes
        nodeList = []
        # Create list of neighbors for each node
        neighborList = []
        # Create variable for number of lines

        #--------------------------------------------------------------------
        # Open the file
        file = open("cfgs/text/" + fileName.split(".")[0] + ".txt")
        lines = file.readlines()

        #--------------------------------------------------------------------
        # Get the length (number of lines) of the original program
        faultyProgram = open("testFiles/" + fileName)
        length = 0
        for line in faultyProgram.readlines():
            if len(line.strip()) != 0:
                length += 1

        #--------------------------------------------------------------------
        # Address each line appropriately for the matching case:
        # 1) The line instantiates a node
        index = 1
        if lines[0].rstrip() == "strict digraph \"\" {":
            index = 3
        for line in lines[index:]:
            if line.find("[") != -1:
                line_split = line.split("[")
                line_split[0] = line_split[0].strip()
                line_split[1] = line_split[1][:-3]
                nodeList.append(line_split)

        # Create dictionary from nodeList
        dict = {}
        for node in nodeList:
            dict[node[0]] = node[1].split(":")[0][-1]
        all_values = dict.values()
        for i in range(length + 1): #+1 to account for the 0 start/stop lines
            neighborList.append([])

        #--------------------------------------------------------------------
        #  2) The line instantiates an edge
        for line in lines[1:]:
            line_split = line.split()
            if ("->" in line_split and len(line_split) == 3):
                # Edges start at 0...
                node1 = int(dict[line_split[0]])
                node2 = int(dict[line_split[2][:-1]])  # the -1 removes the semicolon at the end...
                neighborList[node1].append(node2)

        #--------------------------------------------------------------------
        file = open('rules.lp', 'a')
        file.write("\n")
        for i in range(1, length + 1):
            for j in range(len(neighborList[i])):
                file.write("edge(" + str(i) + ", " + str(neighborList[i][j]) + ").\n")

    #--------------------------------------------------------------------
    #--------------------------------------------------------------------
    #--------------------------------------------------------------------
    # Graph is already available in nx format
    elif(graph != None):
        length = graph.number_of_nodes()
        file = open('rules.lp', 'a')
        file.write("\n")
        for e in graph.edges():
            file.write("edge" + str(e) + ".\n")
        file.close()

    #--------------------------------------------------------------------
    # Run the answer set program
    command = "conda activate potassco && clingo rules.lp > ASPOutput.txt"
    stream = os.popen(command)

    inFile = open("ASPOutput.txt")
    functionCall = inFile.readlines()[4]
    reachabilityList = functionCall.split()

    transitiveClosure=[]
    for i in range(length):
        transitiveClosure.append([])

    for statement in reachabilityList:
        function = statement.split("(")[0]
        args = statement.split("(")[1]
        args = args.split(",")

        if function=="reachable":
            arg1 = args[0]
            arg2 = args[1][:-1]
            (transitiveClosure[int(arg2)-1]).append(int(arg1))

    print(transitiveClosure)

#--------------------------------------------------------------------
# Main function
# -- timing experiments. I altered the times to get my results. Clear the edges from rules.lp between tests...
for size in [101]:
    G = nx.DiGraph()
    for i in range(1, size):
        G.add_node(i)
    for i in range(1, size):
        G.add_edge(i, i+1)
    start = time.time_ns()
    converter(None, G)
    end = time.time_ns()
    print("size: {0}, # nodes: {1}, # edges: {2}, time: {3}".format(str(size), str(G.number_of_nodes()), str(G.number_of_edges()), str(end-start)))
    G.clear()
    #with open('rules.lp', 'r+') as file: 
        #file.truncate(0)
    #file.close()
    #file = open('rules.lp', 'a')
    #file.write("reachable(Z, X) :- edge(X, Y), edge(Y, Z).\n")
    #file.write("edge(X, Y) :- reachable(Y, X).\n")
    #file.close
    
# Testing from a file
'''
start = time.time_ns()
converter("wrong_1_001.py", None)
end = time.time_ns()
print(end-start)
'''