from wgraphclass import *
from tkinter import *
root = Tk()

w = Canvas(root, width=800, height=600)
w.pack()

widgetlist = []

g1 = wdgraph()

coords = []
vertices_save = {}
alphab = [i for i in range(50)]

def createcoor(event):
    coords.append((event.x, event.y))

    if len(coords) == 1:
        btn = Button(root, text=alphab[0], bg='white', command = lambda j=alphab[0]: clickbutton(j))
        btn.place(x=coords[0][0], y=coords[0][1])
        widgetlist.append(btn)
        vertices_save[alphab[0]] = (coords[0][0], coords[0][1])
        g1.addnode(alphab[0])
        del alphab[0]

    if len(coords) == 1:
        del coords[0]

w.bind("<Button-1>", createcoor)

entry3 = Entry(root)
entry3.pack(side = RIGHT)
label3 = Label(root, text='Capacity entry')
label3.pack(side = RIGHT)

connecter = []
capacitiesT = {}
flowsT = {}

def clickbutton(a):
    connecter.append(a)
    if len(connecter) == 2:
        g1.addarrow((connecter[0], connecter[1]), int(entry3.get()))
        x1 = vertices_save[connecter[0]][0]
        y1 = vertices_save[connecter[0]][1]
        x2 = vertices_save[connecter[1]][0]
        y2 = vertices_save[connecter[1]][1]
        w.create_line(x1, y1, x2, y2,arrow='last')
        capacitiesT[(connecter[0], connecter[1])] = Label(root, text='c{}'.format(g1.caps[(connecter[0], connecter[1])]))
        capacitiesT[(connecter[0], connecter[1])].place(x=(x1 + x2)/2,y=(y1 + y2)/2)
        flowsT[(connecter[0], connecter[1])] = Label(root, text='f{}'.format(g1.values[(connecter[0], connecter[1])]))
        flowsT[(connecter[0], connecter[1])].place(x=(x1 + x2) / 2 + 25, y=(y1 + y2) / 2)
        del connecter[0]
        del connecter[0]

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

def FFexec():
    FordFulkerson(g1)
    for i in flowsT.keys():
        flowsT[i].config(text='f{}'.format(g1.values[i]))

def printarrowflow():
    for i in g1.arrows:
        print('arrow {}, with flow {} and with capacity {}'.format(i, g1.values[i], g1.caps[i]))

printarrows = Button(root, text='Print arrows', command=printarrowflow)
printarrows.pack(side=LEFT)

ffbutton = Button(root, text="Ford Fulkerson", command=FFexec)
ffbutton.pack(side=LEFT)

root.mainloop()