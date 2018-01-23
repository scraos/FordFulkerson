class wdgraph():
    def __init__(self):
        self.nodes = []
        self.arrows = []
        self.caps = {}
        self.values = {}

    def addnode(self,n):
        self.nodes.append(n)

    def addsource(self):
        self.nodes.append(0)

    def addsink(self):
        self.nodes.append(len(self.nodes))

    def sink(self):
        return self.nodes[-1]

    def addarrow(self,arrow,cap):
        self.arrows.append(arrow)
        self.caps[arrow] = cap
        self.values[arrow] = 0

    def deltamin(self,node):
        set1 = []
        for i in self.arrows:
            if i[1] == node:
                set1.append(i)
        return set1

    def deltaplus(self,node):
        set2 = []
        for i in self.arrows:
            if i[0] == node:
                set2.append(i)
        return set2

    def flowval(self):
        totsum = 0
        dplus = self.deltaplus(0)
        dmin = self.deltamin(0)
        for i in dplus:
            totsum += self.values[i]
        for j in dmin:
            totsum -= self.values[j]
        return totsum