from wgraphclass import *

def alpha_arrows(path):
    set1 = []
    for i in range(len(path)-1):
        set1.append((path[i],path[i+1]))
    return set1

def newhelpflowgraph(graph):
    helpgraph = wdgraph()
    for j in graph.nodes:
        helpgraph.addnode(j)
    for i in graph.arrows:
        if graph.values[i] < graph.caps[i]:
            helpgraph.addarrow(i,0)
        if graph.values[i] > 0:
            helpgraph.addarrow((i[1],i[0]),0)
    return helpgraph

def getPpathBSF(graph):
    open_set = []
    closed_set = []
    meta = {}
    start = 0
    goal = graph.sink()
    meta[start] = None
    open_set.append(start)
    while open_set:
        parent_state = open_set.pop(0)
        if parent_state == goal:
            return construct_path(parent_state, meta)
        for child in graph.deltaplus(parent_state):
            if child[1] in closed_set:
                continue
            if child[1] not in open_set:
                meta[child[1]] = parent_state
                open_set.append(child[1])
        closed_set.append(parent_state)

def construct_path(state, meta):
    path = (state,)
    while True:
        if meta[state]:
            path += (meta[state],)
            state = meta[state]
        else:
            break
    return (0,) + path[::-1]


def FordFulkerson(graph):
    d_f = newhelpflowgraph(graph)
    p_path = getPpathBSF(d_f)
    while p_path:
        alphaset = []
        alphapath = p_path
        alphaarrows = alpha_arrows(alphapath)
        for i in alphaarrows:
            if i in graph.arrows:
                alphaset.append(graph.caps[i]-graph.values[i])
            elif i[::-1] in graph.arrows:
                alphaset.append(graph.values[i[::-1]])
        alpha = min(alphaset)
        for j in graph.arrows:
            if j in alphaarrows:
                graph.values[j] += alpha
            elif j[::-1] in alphaarrows:
                graph.values[j] -= alpha
        d_f = newhelpflowgraph(graph)
        p_path = getPpathBSF(d_f)
    for item in graph.arrows:
        print('arrow {}, with flow {} and cap {}'.format(item,graph.values[item],graph.caps[item]))

g1 = wdgraph()
g1.addsource()
g1.addnode(1)
g1.addnode(2)
g1.addnode(3)
g1.addnode(4)
g1.addnode(5)
g1.addnode(6)
g1.addsink()
g1.addarrow((0,1),1)
g1.addarrow((0,2),2)
g1.addarrow((0,3),10)
g1.addarrow((1,2),4)
g1.addarrow((3,2),2)
g1.addarrow((3,6),5)
g1.addarrow((3,5),4)
g1.addarrow((2,5),1)
g1.addarrow((2,4),7)
g1.addarrow((2,6),2)
g1.addarrow((1,4),2)
g1.addarrow((4,7),11)
g1.addarrow((5,4),2)
g1.addarrow((5,1),2)
g1.addarrow((6,5),5)
g1.addarrow((5,7),2)
g1.addarrow((6,7),1)

FordFulkerson(g1)
print(g1.flowval())