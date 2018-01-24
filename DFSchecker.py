def DFScheck(graph,current_node,visited):
    visited[current_node] = True
    for i in graph.deltaplus(current_node):
        if not visited[i[1]]:
            DFScheck(graph,i[1],visited)

def DFS(graph,node):
    visited = [False for i in range(len(graph.nodes))]
    DFScheck(graph,node,visited)
    nodesvisited = []
    for i in range(len(visited)):
        if visited[i]:
            nodesvisited.append(i)
    return nodesvisited