class Graph :
    def __init__(self):
        self.numNodes = 0;
        self.numEdges = 0;
        # per node i a list of node-ids j for which (i,j) \in E
        self.edges = [frozenset()];

    def hasEdge(self, i, j):
        return max(i,j)-1 in self.edges[min(i,j)-1];
    
    def load(self, fullpath):
        fg = open(fullpath);
        self.edges = [];
        edgeList = [];
        for line in fg :
            tmp = line.strip().split(',');
            if len(tmp) < 2 :
                continue;
            
            i = int(tmp[0]);
            j = int(tmp[1]);
            if i > self.numNodes :
                self.numNodes = i;
            if j > self.numNodes :
                self.numNodes = j;
            edgeList.append((min(i,j),max(i,j)));

        tmpAdj = [set() for i in range(self.numNodes)];
        
        for edge in edgeList :
            (i,j) = edge;
            # option 1
            if(j-1 not in tmpAdj[i-1]) :
                tmpAdj[i-1].add(j-1);            
                self.numEdges += 1;

        # finalize edges into frozensets
        self.edges = [frozenset(x) for x in tmpAdj];
        
        #print self.edges, self.numEdges;
        return;
  
    def plot(self):
        for idx in range(len(self.edges)) :
            mystr = "".join(["." for x in range(0,idx+1)]);
            for idy in range(idx+1,len(self.edges)) :
                if idy in self.edges[idx] :
                    mystr += "1";
                else :
                    mystr += "0";
            print mystr;
