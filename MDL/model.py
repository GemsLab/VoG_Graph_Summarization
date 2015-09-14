#from math import log;

class Model :
    strucTypes = [];
    numStrucTypes = 0;
    structs = [];
    numStructs = 0;
    
    numFullCliques = 0;
    numNearCliques = 0;
    numFullOffDiagonals = 0;
    numNearOffDiagonals = 0;
    numChains = 0;
    numStars = 0;
    numBiPartiteCores = 0;
    numNearBiPartiteCores = 0;
    numCorePeripheries = 0;
    numJellyFishes = 0;
    
    def __init__(self):
        self.strucTypes = ["fc","nc","ch","st","bc","nb"]; #,"cp","jf","fod","nod"];
        self.numStrucTypes = len(self.strucTypes);
        self.structs = [];        
        self.numStructs = 0;

    def setStrucTypes(self, st) :
        self.strucTypes = st;
        self.numStrucTypes = len(self.strucTypes);
        
    # struct of type Struct
    def addStructure(self, struct) :
        self.structs.append(struct);
        self.numStructs += 1;
        
        if struct.getType() not in self.strucTypes :
            print "structure type not declared";
            
        if struct.isFullClique() :
            self.numFullCliques += 1;
        elif struct.isNearClique() :
            self.numNearCliques += 1;            
        if struct.isFullOffDiagonal() :
            self.numFullOffDiagonals+= 1;
        elif struct.isNearOffDiagonal() :
            self.numNearOffDiagonals += 1;            
        elif struct.isChain() :
            self.numChains += 1;
        elif struct.isStar() :
            self.numStars += 1;
        elif struct.isBiPartiteCore() :
            self.numBiPartiteCores += 1;        
        elif struct.isNearBiPartiteCore() :
            self.numNearBiPartiteCores += 1;
        elif struct.isCorePeriphery() :
            self.numCorePeripheries += 1;        
        elif struct.isJellyFish() :
            self.numJellyFishes += 1;        

    # remove structure struct
    def rmStructure(self, struct) :
        self.structs.remove(struct);
        self.numStructs -= 1;
        
        if struct.getType() not in self.strucTypes :
            print "structure type not declared";
            
        if struct.isFullClique() :
            self.numFullCliques -= 1;
        elif struct.isNearClique() :
            self.numNearCliques -= 1;            
        if struct.isFullOffDiagonal() :
            self.numFullOffDiagonals-= 1;
        elif struct.isNearOffDiagonal() :
            self.numNearOffDiagonals -= 1;            
        elif struct.isChain() :
            self.numChains -= 1;
        elif struct.isStar() :
            self.numStars -= 1;
        elif struct.isBiPartiteCore() :
            self.numBiPartiteCores -= 1;        
        elif struct.isNearBiPartiteCore() :
            self.numNearBiPartiteCores -= 1;
        elif struct.isCorePeriphery() :
            self.numCorePeripheries -= 1;        
        elif struct.isJellyFish() :
            self.numJellyFishes -= 1;        

    def load(self, fullpath):
        fg = open(fullpath);
        for line in fg :
            if len(line) < 4 or line[0] == "#" :
                continue;
            struct = Structure.load(line);
            if struct != 0 :
                self.addStructure(struct);
        return;
     
    def loadLine(self, content, lineNo):
        line = content[lineNo]; # line of the model to be added
        if len(line) < 4 or line[0] == "#":
            return -1;
        struct = Structure.load(line);
        if struct != 0 :
            self.addStructure(struct);
	return struct;

    def loadLines(self, fullpath, lineList):
        fg = open(fullpath);
        lineNo = 0;
        for line in fg :
            lineNo = lineNo + 1;
            if lineNo > lineList[len(lineList) - 1] :
                break;
            if lineNo in lineList :
            	if len(line) < 4 or line[0] == "#":
                	continue;
            	struct = Structure.load(line);
            	if struct != 0 :
                	self.addStructure(struct);
        return;

class Structure :
    def getType(self):
        return "?";
    getType = staticmethod(getType);
        
    def isFullClique(self):
        return False;
    def isNearClique(self):
        return False;

    def isFullOffDiagonal(self):
        return False;
    def isNearOffDiagonal(self):
        return False;

    def isChain(self):
        return False;
    def isStar(self):
        return False;

    def isBiPartiteCore(self):
        return False;

    def isNearBiPartiteCore(self):
        return False;

    def isCorePeriphery(self):
        return False;

    def isJellyFish(self):
        return False;

    def load(line) :
        if line[:2] == FullClique.getType() :
            return FullClique.load(line);
        elif line[:2] == NearClique.getType() :
            return NearClique.load(line);
        if line[:3] == FullOffDiagonal.getType() :
            return FullOffDiagonal.load(line);
        elif line[:3] == NearOffDiagonal.getType() :
            return NearOffDiagonal.load(line);
        elif line[:2] == Chain.getType() :
            return Chain.load(line);
        elif line[:2] == Star.getType() :
            return Star.load(line);
        elif line[:2] == BiPartiteCore.getType() :
            return BiPartiteCore.load(line);
        elif line[:2] == NearBiPartiteCore.getType() :
            return NearBiPartiteCore.load(line);
        elif line[:2] == CorePeriphery.getType() :
            return CorePeriphery.load(line);
        elif line[:2] == JellyFish.getType() :
            return JellyFish.load(line);
    load = staticmethod(load)

class Clique(Structure) :
    nodes = [];
    numNodes = 0;


class FullClique(Clique) :
    def __init__(self, nodes):
        self.nodes = nodes;
        self.numNodes = len(nodes);
        
    def getType():
        return "fc";
    getType = staticmethod(getType);

    def isFullClique(self):
        return True;
    
    def load(line) :
        # "fc 1 2 3 4 ..
        if line[:2] != FullClique.getType() :
            return 0;
        parts = line[3:].strip().split(' ');
        nodes = [];
        for x in parts :
            if x.find('-') > 0 :
                y = x.strip().split('-');
                nodes.extend([z for z in range(int(y[0]),int(y[1])+1)]);
            else :
                nodes.append(int(x));
        return FullClique(sorted(nodes));        
    load = staticmethod(load);


class NearClique(Clique) :
    numEdges = 0;
    
    def __init__(self, nodes, numEdges):
        self.nodes = nodes;
        self.numNodes = len(nodes);
        self.numEdges = numEdges;

    def getType():
        return "nc";
    getType = staticmethod(getType);

    def isNearClique(self):
        return True;

    def load(line) :
        # "nc <edge count>, 1 2 3 4 ..
        if line[:2] != NearClique.getType() :
            return 0;
        cParts = line[3:].strip().split(',');
        numEdges = int(float(cParts[0].strip()));
        
        sParts = cParts[1].strip().split(' ');
        
        nodes = [];
        for x in sParts :
            if x.find('-') > 0 :
                y = x.strip().split('-');
                nodes.extend([x for x in range(int(y[0]),int(y[1])+1)]);
            else :
                nodes.append(int(x));
        return NearClique(sorted(nodes), numEdges);        
    load = staticmethod(load);

class Rectangle(Structure) :
	lNodeList = [];
	rNodeList = [];
	numNodesLeft = 0;
	numNodesRight = 0;

	def __init__(self, left, right):
		self.lNodeList = left;
		self.rNodeList = right;
		self.numNodesLeft = len(left);
		self.numNodesRight = len(right);

class FullOffDiagonal(Rectangle) :
    def __init__(self, left, right):
        Rectangle.__init__(self, left, right)

    def getType():
        return "fod";
    getType = staticmethod(getType);

    def isFullOffDiagonal(self):
        return True;

    def load(line) :
        # "fod [left ids], [right ids]
        if line[:3] != FullOffDiagonal.getType() :
            return 0;
        parts = line[4:].strip().split(',');
        lParts = parts[0].strip().split(' ');
        lNodeList = [];
        for x in lParts :
            if x.find('-') > 0 :
                y = x.strip().split('-');
                lNodeList.extend([z for z in range(int(y[0]),int(y[1])+1)]);
            else :
                lNodeList.append(int(x));
        rParts = parts[1].strip().split(' ');
        rNodeList = [];
        for x in rParts :
            if x.find('-') > 0 :
                y = x.strip().split('-');
                rNodeList.extend([z for z in range(int(y[0]),int(y[1])+1)]);
            else :
                rNodeList.append(int(x));
        return FullOffDiagonal(sorted(lNodeList),sorted(rNodeList));
    load = staticmethod(load);


class NearOffDiagonal(Rectangle) :
    def __init__(self, left, right):
        Rectangle.__init__(self, left, right)

    def getType():
        return "nod";
    getType = staticmethod(getType);

    def isNearOffDiagonal(self):
        return True;

    def load(line) :
        # "fod [left ids], [right ids]
        if line[:3] != NearOffDiagonal.getType() :
            return 0;
        parts = line[4:].strip().split(',');
        lParts = parts[0].strip().split(' ');
        lNodeList = [];
        for x in lParts :
            if x.find('-') > 0 :
                y = x.strip().split('-');
                lNodeList.extend([z for z in range(int(y[0]),int(y[1])+1)]);
            else :
                lNodeList.append(int(x));
        rParts = parts[1].strip().split(' ');
        rNodeList = [];
        for x in rParts :
            if x.find('-') > 0 :
                y = x.strip().split('-');
                rNodeList.extend([z for z in range(int(y[0]),int(y[1])+1)]);
            else :
                rNodeList.append(int(x));
        return NearOffDiagonal(sorted(lNodeList),sorted(rNodeList));
    load = staticmethod(load);



class Chain(Structure) :
    nodes = [];
    numNodes = 0;
    
    def __init__(self, nodes):
        self.nodes = nodes;
        self.numNodes = len(nodes);

    def getType():
        return "ch";
    getType = staticmethod(getType);

    def isChain(self):
        return True;

    def load(line) :
        # "ch 1 2 3 4 ..
        if line[:2] != Chain.getType() :
            return 0;
        parts = line[3:].strip().split(' ');
        nodes = [];
        for x in parts :
            if x.find('-') > 0 :
                y = x.strip().split('-');
                nodes.extend([x for x in range(int(y[0]),int(y[1])+1)]);
            else :
                nodes.append(int(x));
        return Chain(nodes);
    load = staticmethod(load);


class Star(Structure) :
    cNode = -1;
    sNodes = [];
    numSpokes = 0;
    
    def __init__(self, hub, spokes):
        self.cNode = hub;
        self.sNodes = spokes;
        self.numSpokes = len(spokes);

    def getType():
        return "st";
    getType = staticmethod(getType);
        
    def isStar(self):
        return True;

    def load(line) :
        # "st <hubid> [spoke ids ...]
        if line[:2] != Star.getType() :
            return 0;
        parts = line[3:].strip().split(',');
        cParts = parts[0].strip().split(' ');
        cNodes = [];
        for x in cParts :
            if x.find('-') > 0 :
                y = x.split('-');
                cNodes.extend([x for x in range(int(y[0]),int(y[1])+1)]);
            else :
                cNodes.append(int(x));
        sParts = parts[1].strip().split(' ');
        sNodes = [];
        for x in sParts :
            
            if x.find('-') > 0 :
                y = x.split('-');
                sNodes.extend([x for x in range(int(y[0]),int(y[1])+1)]);
            else :
                sNodes.append(int(x));
        return Star(cNodes[0],sorted(sNodes));
    load = staticmethod(load);


class BiPartiteCore(Structure) :
    lNodes = [];
    numNodesLeft = 0;
    rNodes = [];
    numNodesRight = 0;
    
    def __init__(self, left, right):
        self.lNodes = left;
        self.numNodesLeft = len(left);
        self.rNodes = right;
        self.numNodesRight = len(right);

    def getType():
        return "bc";
    getType = staticmethod(getType);

    def isBiPartiteCore(self):
        return True;

    def load(line) :
        # "bc [left ids], [right ids]
        if line[:2] != BiPartiteCore.getType() :
            return 0;
        parts = line[3:].strip().split(',');
        lParts = parts[0].strip().split(' ');
        lNodes = [];
        for x in lParts :
            if x.find('-') > 0 :
                y = x.strip().split('-');
                lNodes.extend([z for z in range(int(y[0]),int(y[1])+1)]);
            else :
                lNodes.append(int(x));
        rParts = parts[1].strip().split(' ');
        rNodes = [];
        for x in rParts :
            if x.find('-') > 0 :
                y = x.strip().split('-');
                rNodes.extend([z for z in range(int(y[0]),int(y[1])+1)]);
            else :
                rNodes.append(int(x));
        return BiPartiteCore(sorted(lNodes),sorted(rNodes));
    load = staticmethod(load);
   

class NearBiPartiteCore(Structure) :
    lNodes = [];
    numNodesLeft = 0;
    rNodes = [];
    numNodesRight = 0;
    
    def __init__(self, left, right):
        self.lNodes = left;
        self.numNodesLeft = len(left);
        self.rNodes = right;
        self.numRightNodes = len(right);

    def getType():
        return "nb";
    getType = staticmethod(getType);

    def isNearBiPartiteCore(self):
        return True;

    def load(line) :
        # "nb [left ids], [right ids]
        if line[:2] != NearBiPartiteCore.getType() :
            return 0;
        parts = line[3:].strip().split(',');
        lParts = parts[0].strip().split(' ');
        lNodes = [];
        for x in lParts :
            if x.find('-') > 0 :
                y = x.strip().split('-');
                lNodes.extend([z for z in range(int(y[0]),int(y[1])+1)]);
            else :
                lNodes.append(int(x));
        rParts = parts[1].strip().split(' ');
        rNodes = [];
        for x in rParts :
            if x.find('-') > 0 :
                y = x.strip().split('-');
                rNodes.extend([z for z in range(int(y[0]),int(y[1])+1)]);
            else :
                rNodes.append(int(x));
        return NearBiPartiteCore(sorted(lNodes),sorted(rNodes));
    load = staticmethod(load);


class CorePeriphery(Structure) :
    cNodes = [];
    numCores = 0;
    sNodes = [];
    numSpokes = 0;
    
    def __init__(self, cores, spokes):
        self.cNodes = cores;
        self.numCores = len(cores);
        self.sNodes = spokes;
        self.numSpokes = len(spokes);

    def getType():
        return "cp";
    getType = staticmethod(getType);

    def isCorePeriphery(self):
        return True;

    def load(line) :
        # "cp [hubids], [spoke ids]
        if line[:2] != CorePeriphery.getType() :
            return 0;
        parts = line[3:].strip().split(',');
        cParts = parts[0].strip().split(' ');
        cNodes = [];
        for x in cParts :
            if x.find('-') > 0 :
                y = x.strip().split('-');
                cNodes.extend([z for z in range(int(y[0]),int(y[1])+1)]);
            else :
                cNodes.append(int(x));
        sParts = parts[1].strip().split(' ');
        sNodes = [];
        for x in sParts :
            if x.find('-') > 0 :
                y = x.strip().split('-');
                sNodes.extend([z for z in range(int(y[0]),int(y[1])+1)]);
            else :
                sNodes.append(int(x));
        return CorePeriphery(sorted(cNodes),sorted(sNodes));
    load = staticmethod(load);


class JellyFish(Structure) :
    cNodes = [];
    numCores = 0;
    sNodes = [[]];
    numSpokes = [];
    numSpokeSum = 0;
    
    def __init__(self, cores, spokes):
        self.cNodes = cores;
        self.numCores = len(cores);
        self.sNodes = spokes;
        self.numSpokes = [len(s) for s in spokes];
        self.numSpokeSum = sum(self.numSpokes);

    def getType():
        return "jf";
    getType = staticmethod(getType);

    def isJellyFish(self):
        return True;

    def load(line) :
        # jf [hubids], [[spoke ids],]
        if line[:2] != JellyFish.getType() :
            return 0;
        parts = line[3:].strip().split(',');
        cParts = parts[0].strip().split(' ');
        cNodes = [];
        for x in cParts :
            if x.find('-') > 0 :
                y = x.strip().split('-');
                cNodes.extend([z for z in range(int(y[0]),int(y[1])+1)]);
            else :
                cNodes.append(int(x));
                
        sNodes = [[] for x in range(len(cNodes))];
        
        for i in range(len(cNodes)) :
            sParts = parts[i+1].strip().split(' ');
            for x in sParts :
                if x.find('-') > 0 :
                    y = x.strip().split('-');
                    sNodes[i].extend([z for z in range(int(y[0]),int(y[1])+1)]);
                else :
                    sNodes[i].append(int(x));
            sNodes[i] = sorted(sNodes[i]);
        return JellyFish(sorted(cNodes),sNodes);
    load = staticmethod(load);



