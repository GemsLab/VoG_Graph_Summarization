import config;

from math import log,factorial;
from error import Error;
from graph import Graph;
from model import Model;

### basic functions
# determine possible number of edges between `numEdges' nodes
def CalcCliqueNumPosEdges(numEdges):
  # directed graph, no self-loops
  # (|n|^2)-n
  return numEdges*numEdges - numEdges;

# (n choose k)
def choose(n, k):
 if 0 <= k <= n:
   p = 1
   for t in xrange(min(k, n - k)):
     p = (p * (n - t)) // (t + 1)
   return p;
 else:
   return 0;

def composition(n,k) :
    return choose(n-1,k-1);

def LC(n,k) :
    return log(composition(n,k),2);

def weakcomposition(n,k) :
    return choose(n+k-1,k-1);
    
def LwC(n,k) :
    return log(weakcomposition(n,k),2);

# Encoded length of `n` 0/1 entries with `k` 1s (aka, Naive Uniform)
def LnU(n,k):
    #print 'LnU', n, k
    if n==0 or k==0 or k==n:
        return 0;    
    x = -log(k / float(n),2);
    y = -log((n-k)/float(n),2);
    return k * x + (n-k) * y;
    
# Encoded length of `n` 0/1 entries with `k` 1s (aka, Uniform)
def LU(n,k) :
    if n==0 or k==0 :
        return 0;   
    return log(choose(n,k),2);

# encoded size of an integer >=1 as by Rissanen's 1983 Universal code for integers
def LN(z) :
  if z <= 0 :
    return 0;
  c = log(2.865064,2);
  i = log(z,2);
  while i > 0 :
    c = c + i;
    i = log(i,2);
  return c;
 


### Our Encoding Starts Here ###

### Total Encoded Size
def L(G, M, errorEnc): 
    E = Error(G); # initially, everything is error, nothing is covered
    error_cost = 0;
    
    model_cost = LN(M.numStructs+1);    # encode number of structures we're encoding with
    model_cost += LwC(M.numStructs, M.numStrucTypes);            # encode the number per structure

    # encode the structure-type identifier per type
    if M.numFullCliques > 0 :
        model_cost += M.numFullCliques * log(M.numFullCliques / float(M.numStructs), 2);
    if M.numNearCliques  > 0 :
        model_cost += M.numNearCliques * log(M.numNearCliques / float(M.numStructs), 2);
    if M.numChains > 0 :
        model_cost += M.numChains * log(M.numChains / float(M.numStructs), 2);
    if M.numStars > 0 :
        model_cost += M.numStars * log(M.numStars / float(M.numStructs), 2);
    if M.numBiPartiteCores > 0 :
        model_cost += M.numBiPartiteCores * log(M.numBiPartiteCores / float(M.numStructs), 2);
    if M.numNearBiPartiteCores > 0 :
        model_cost += M.numNearBiPartiteCores * log(M.numNearBiPartiteCores / float(M.numStructs), 2);
    if M.numJellyFishes > 0 :
        model_cost += M.numJellyFishes * log(M.numJellyFishes / float(M.numStructs), 2);
    if M.numCorePeripheries > 0 :
        model_cost += M.numCorePeripheries * log(M.numCorePeripheries / float(M.numStructs), 2);

    
    # encode the structures
    for struc in M.structs :
        if struc.isFullClique() :
            model_cost += LfullClique(struc,M,G,E);
        elif struc.isNearClique() :
            model_cost += LnearClique(struc,M,G,E);
        elif struc.isChain() :
            model_cost += Lchain(struc,M,G,E);
        elif struc.isStar() :
            model_cost += Lstar(struc,M,G,E);
        elif struc.isCorePeriphery() :
            model_cost += LcorePeriphery(struc,M,G,E);
        elif struc.isBiPartiteCore() :
            model_cost += LbiPartiteCore(struc,M,G,E);
        elif struc.isNearBiPartiteCore() :
            model_cost += LnearBiPartiteCore(struc,M,G,E);
        elif struc.isJellyFish() :
            model_cost += LjellyFish(struc,M,G,E);
    
    
    # encode the error
    error_cost += 0 if E.numCellsCovered == 0 else log(E.numCellsCovered, 2);    # encode number of additive Errors
    if ((G.numNodes * G.numNodes - G.numNodes) / 2) - E.numCellsCovered > 0 :
        error_cost += log(((G.numNodes * G.numNodes - G.numNodes) / 2) - E.numCellsCovered, 2);    # encode number of Errors
        
    if errorEnc == "NP" :
        error_cost += LErrorNaivePrefix(G,M,E);
    elif errorEnc == "NB" :
        error_cost += LErrorNaiveBinom(G,M,E);
    elif errorEnc == "TP" :
        error_cost += LErrorTypedPrefix(G,M,E);
    elif errorEnc == "TB" :
        error_cost += LErrorTypedBinom(G,M,E);
    
    total_cost = model_cost + error_cost;
    
    return (total_cost, model_cost, error_cost, E);

# Encoded Size of a Full-Clique
def LfullClique(c, M, G, E):
    # update Error
    coverFullClique(G, E, c);
    
    cost = LN(c.numNodes);          # encode number of nodes
    if G.numNodes > 0 and c.numNodes > 0 :
        cost += LU(G.numNodes, c.numNodes);     # encode node ids
    return cost;

def coverFullClique(G, E, c):
    # c.nodes is ordered
    for i_idx in range(c.numNodes) :
        i = c.nodes[i_idx];
        for j_idx in range(i_idx+1,c.numNodes) :
            j = c.nodes[j_idx];
            
            if not E.isExcluded(i,j) :
                # only if (i,j) is not modelled perfectly
                
                if not E.isCovered(i,j) :
                    # edge is not modelled yet
                    if G.hasEdge(i,j) :
                        # yet there is a real edge, so now we undo an error
                        E.delUnmodelledError(i,j);
                    else :
                        # there is no real edge, but now we say there is, so we introduce error
                        E.addModellingError(i,j);
                    E.cover(i,j);

                else :
                    # edge is already modelled
                    if G.hasEdge(i,j) and E.isModellingError(i,j) :
                        # edge exists, but model denied
                        E.delModellingError(i,j);
                    elif not G.hasEdge(i,j) and not E.isModellingError(i,j) :
                        # edge does not exist, but now we say it does
                        E.addModellingError(i,j);
    return;


# Encoded Size of a Near-Clique  
def LnearClique(c, M, G, E) :
    # update Error, count coverage
    (cnt0,cnt1) = coverNearClique(G, E, c)
    
    cost = LN(c.numNodes);              # encode number of nodes
    cost += LU(G.numNodes, c.numNodes);  # encode node ids
    if cnt0+cnt1 > 0 :
        cost += log(cnt0+cnt1, 2);     # encode probability of a 1 (cnt0+cnt1 is number of cells we describe, upperbounded by numnodes 2)
        cost += LnU(cnt0+cnt1, cnt1);       # encode the edges
    return cost;
	  
def coverNearClique(G, E, c) :
    # c.nodes is ordered    
    cnt0 = 0;
    cnt1 = 0;
    for i_idx in range(c.numNodes) :
        i = c.nodes[i_idx];
        for j_idx in range(i_idx+1, c.numNodes) :
            j = c.nodes[j_idx];
            
            if not E.isExcluded(i,j) :
                # only if (i,j) is not already modelled perfectly
                
                if not E.isCovered(i,j) :
                    # edge is not modelled yet
                    if G.hasEdge(i,j) :
                        # yet there is a real edge, so now we undo an error
                        E.delUnmodelledError(i,j);
                    E.coverAndExclude(i,j);

                else :
                    # edge is already modelled
                    if E.isModellingError(i,j) :
                        # but wrongly, we undo that error
                        E.delModellingError(i,j);
                    E.exclude(i,j)
                            
                if G.hasEdge(i,j) :
                    cnt1 += 1;
                else:
                    cnt0 += 1;
                
    return (cnt0,cnt1);


# Encoded Size of a Chain
def Lchain(ch, M, G, E) :
    # update Error
    coverChain(G,E,ch);
    
    cost = LN(ch.numNodes-1); # we know chain is at least 2 nodes
    cost += LU(G.numNodes,ch.numNodes); # identify the nodes
    cost += log(factorial(ch.numNodes),2) # identify their order
    
    ## same as LU + log(factorial)
    #for nid in range(ch.numNodes) :
    #    cost += log(G.numNodes - nid, 2); # identify the node ids in order
    return cost;

def coverChain(G, E, ch) :
    # model chain
    for i_idx in range(ch.numNodes-1) :
        i = ch.nodes[i_idx];
        j = ch.nodes[i_idx+1];
        
        if not E.isExcluded(i,j) :
            # only if (i,j) is not already modelled perfectly
            if not E.isCovered(i, j) :
                # edge is not modelled yet
                
                if G.hasEdge(i, j) :
                    E.delUnmodelledError(i, j);
                else :
                    E.addModellingError(i, j);
                E.cover(i,j);

            else :
                # edge is already modelled

                if G.hasEdge(i,j) and E.isModellingError(i,j) :
                    # model is wrong in saying no edge
                    E.delModellingError(i,j);
                # elif G.hasEdge(i,j) and not E.isModellingError(i,j) :
                # there is an edge, and we knew that
                # elif not G.hasEdge(i,j) and E.isModellingError(i,j) :
                # there is no edge, but we keep saying there is
                elif not G.hasEdge(i,j) and not E.isModellingError(i,j) :
                    # there is no edge, but now we say there is
                    E.addModellingError(i,j);

    if config.optModelZeroes == True :
        # model non-shortcuts
        for i_idx in range(ch.numNodes) :
            i = ch.nodes[i_idx];
            for j_idx in range(i_idx+2, ch.numNodes) : # skip the direct neighbour
                j = ch.nodes[j_idx];
                
                if not E.isExcluded(i,j) :
                    # only if (i,j) is not already modelled perfectly
                    if not E.isCovered(i,j) :
                        # edge not yet modelled
                        if G.hasEdge(i,j) :
                            # oops, there is an edge, but we say there aint
                            E.addModellingError(i,j);
                        #else :
                             # there is no edge, so we're good
                        E.cover(i,j);
                    #else :
                        # edge is modelled
                        #if G.hasEdge(i,j) and E.isModellingError(i,j) :
                            # model incorrect in saying there is no edge - no change
                        #if G.hasEdge(i,j) and not E.isModellingError(i,j) :
                            # model correct in saying there is an edge, no change
                        # ...
    return;



# Encoded Size of a Star
def Lstar(star, M, G, E) :
    # update Error
    coverStar(G, E, star);
    
    cost = LN(star.numSpokes);      # number of spokes (we know there's one hub)
    cost += log(G.numNodes, 2);     # identify the hub-node
    
    #cost += star.numSpokes * log(G.numNodes-1,2);  # identify the spoke-nodes
    cost += LU(G.numNodes-1,star.numSpokes);  # identify the spoke-nodes
    
    return cost;

def coverStar(G, E, st) :
    
    i = st.cNode;
    for j in st.sNodes:
        x = min(i,j);
        y = max(i,j);
        if not E.isExcluded(i,j) :
            # only if (i,j) is not already modelled perfectly
            
            if G.hasEdge(x,y) :
                if E.isCovered(x,y) :
                    if E.isModellingError(x,y) :
                        # previously modelled as 0, we fix the error
                        E.delModellingError(x,y);
                else :
                    E.delUnmodelledError(x,y);
                    E.cover(x,y);
            else :
                if E.isCovered(x,y) :
                    if not E.isModellingError(x,y) :
                        E.addModellingError(x,y);
                else :
                    E.addModellingError(x,y);
                    E.cover(x,y)
                        

    if config.optModelZeroes == True :
        # model non-shortcuts
        for i_idx in range(st.numSpokes) :
            i = st.sNodes[i_idx];
            for j_idx in range(i_idx+1, st.numSpokes) :
                j = st.sNodes[j_idx];
                    
                if not E.isExcluded(i,j) :
                    # only if (i,j) is not already modelled perfectly
                    
                    if not E.isCovered(i,j) :
                        # edge not yet modelled
                        if G.hasEdge(i,j) :
                            # oops, there is an edge, but we say there aint
                            E.addModellingError(i,j);
                        #else :
                             # there is no edge, so we're good
                        E.cover(i,j);
                    #else :
                        # edge is modelled
                        #if G.hasEdge(i,j) and E.isModellingError(i,j) :
                            # model incorrect in saying there is no edge - no change
                        #if G.hasEdge(i,j) and not E.isModellingError(i,j) :
                            # model correct in saying there is an edge, no change
                        # ...
            
    return;
    
# Encoded Size of a bi-partite core
def LbiPartiteCore(bc, M, G, E) :
    # update Error
    coverBiPartiteCore(G, E, bc);    
    
    cost = LN(bc.numLeftNodes) + LN(bc.numRightNodes);
    cost += LU(G.numNodes, bc.numLeftNodes);
    cost += LU(G.numNodes- bc.numLeftNodes, bc.numRightNodes);
    return cost;
    
def coverBiPartiteCore(G, E, bc) :
    
    # 1. fill in the 1s between the parts
    for i in bc.lNodes :
        for j in bc.rNodes :
            if not E.isExcluded(i,j) :
                # only if (i,j) is not already modelled perfectly
                if G.hasEdge(i,j) :
                    # there is an edge
                    if E.isCovered(i,j) :
                        if E.isModellingError(i,j) :
                            # model says 0, we fix to 1
                            E.delModellingError(i,j);
                    else :
                        # model didnt say anything, we fix it
                        E.delUnmodelledError(i,j);
                        E.cover(i,j);
                else :
                    # there is no edge
                    if E.isCovered(i,j) :
                        # but the cell is modelled
                        if not E.isModellingError(i,j) :
                            E.addModellingError(i,j); # we make a boo-boo
                    else :
                        # the cell is not modelled, yet
                        E.addModellingError(i,j);
                        E.cover(i,j);

    # 2. fill in the 0s in left part
    for i_idx in range(len(bc.lNodes)-1) :
        i = bc.lNodes[i_idx];
        for j_idx in range(i_idx+1,len(bc.lNodes)) :
            j = bc.lNodes[j_idx];
            
            if not E.isExcluded(i,j) and not E.isCovered(i,j) :
                # only if (i,j) is not covered or already modelled perfectly
                    if E.isUnmodelledError(i,j) :
                        # edge exists!
                        E.delUnmodelledError(i,j);  # we now model this cell
                        E.addModellingError(i,j);   # but do so wrongly
                    E.cover(i,j);
                
    # 3. fill in the 0s in right part
    for i_idx in range(len(bc.rNodes)-1) :
        i = bc.rNodes[i_idx];
        for j_idx in range(i_idx+1,len(bc.rNodes)) :
            j = bc.rNodes[j_idx];
            
            if not E.isExcluded(i,j) and not E.isCovered(i,j) :
                # only if (i,j) is not covered or already modelled perfectly
                    if E.isUnmodelledError(i,j) :
                        # edge exists!
                        E.delUnmodelledError(i,j);  # we now model this cell
                        E.addModellingError(i,j);   # but do so wrongly
                    E.cover(i,j);
    return;


# Encoded Size of a near bi-partite core
def LnearBiPartiteCore(nb, M, G, E) :
    # update Error
    (cnt0,cnt1) = coverNearBiPartiteCore(G, E, nb);    
    
    # encode number of nodes in sets A and B
    cost = LN(nb.numLeftNodes) + LN(nb.numRightNodes);
    # encode node ids of sets A and B
    cost += LU(G.numNodes, nb.numLeftNodes);
    cost += LU(G.numNodes- nb.numLeftNodes, nb.numRightNodes);
    
    if cnt0+cnt1 > 0 :
        # encode probability of a 1 between sets A and B
        cost += log(cnt0+cnt1, 2);
        # encode the actual edges between A and B
        cost += LnU(cnt0+cnt1, cnt1);
    return cost;
    
	  
def coverNearBiPartiteCore(G, E, nb) :
    # first encode the edges between the parts
    cnt0 = 0;
    cnt1 = 0;
    for i_idx in range(nb.numLeftNodes) :
        i = nb.lNodes[i_idx];
        for j_idx in range(nb.numRightNodes) :
            j = nb.rNodes[j_idx];

            if not E.isExcluded(i,j) :
                # only if (i,j) is not already modelled perfectly

                if not E.isCovered(i,j) :
                    # edge is not modelled yet
                    if G.hasEdge(i,j) :
                        # yet there is a real edge, so now we undo an error
                        E.delUnmodelledError(i,j);
                    E.coverAndExclude(i,j);

                else :
                    # edge is already modelled
                    if E.isModellingError(i,j) :
                        # but wrongly, we undo that error
                        E.delModellingError(i,j);
                    E.exclude(i,j)
                            
                if G.hasEdge(i,j) :
                    cnt1 += 1;
                else:
                    cnt0 += 1;


    # 2. fill in the 0s in left part
    for i_idx in range(len(nb.lNodes)-1) :
        i = nb.lNodes[i_idx];
        for j_idx in range(i_idx+1,len(nb.lNodes)) :
            j = nb.lNodes[j_idx];
            
            if not E.isExcluded(i,j) and not E.isCovered(i,j) :
                # only if (i,j) is not covered or already modelled perfectly
                    if E.isUnmodelledError(i,j) :
                        # edge exists!
                        E.delUnmodelledError(i,j);  # we now model this cell
                        E.addModellingError(i,j);   # but do so wrongly
                    E.cover(i,j);
                
    # 3. fill in the 0s in right part
    for i_idx in range(len(nb.rNodes)-1) :
        i = nb.rNodes[i_idx];
        for j_idx in range(i_idx+1,len(nb.rNodes)) :
            j = nb.rNodes[j_idx];
            
            if not E.isExcluded(i,j) and not E.isCovered(i,j) :
                # only if (i,j) is not covered or already modelled perfectly
                    if E.isUnmodelledError(i,j) :
                        # edge exists!
                        E.delUnmodelledError(i,j);  # we now model this cell
                        E.addModellingError(i,j);   # but do so wrongly
                    E.cover(i,j);
            
    return (cnt0,cnt1);


# Encoded Size of a jellyfish structure
def LjellyFish(jf, M, G, E) :
    # update Error
    coverJellyFish(G, E, jf);
    
    cost = LN(jf.numCores); # number of core nodes
    cost += LU(G.numNodes, jf.numCores); # core node ids

    cost += LN(jf.numSpokeSum) + LC(jf.numSpokeSum, jf.numCores); # number of spokes per core node
    cost += LU(G.numNodes - jf.numCores, jf.numSpokeSum); # spoke ids (-no- overlap between sets!)
    return cost;
    
def coverJellyFish(G, E, jf) :
    
    # first link up the nodes in the core
    for i_idx in range(len(jf.cNodes)) :
        i = jf.cNodes[i_idx];
        for j_idx in range(i_idx+1,len(jf.cNodes)) :
            j = jf.cNodes[j_idx];

            if not E.isExcluded(i,j) :
                # only if (i,j) is not already modelled perfectly
                
                if G.hasEdge(i,j) :
                    # there is an edge
                    if E.isCovered(i,j) :
                        if E.isModellingError(i,j) :
                            E.delModellingError(i,j); # model said 0, but we say 1
                    else :
                        # edge is there, but not covered, we fix it!
                        E.delUnmodelledError(i,j);
                        E.cover(i,j);
                else :
                    # there is no edge
                    if E.isCovered(i,j) :
                        if not E.isModellingError(i,j) :
                            E.addModellingError(i,j); # model said 0, we say 1
                    else :
                        E.addModellingError(i,j);
                        E.cover(i,j);

    # 2. link up the core nodes up to their respective spokes
    for i_idx in range(len(jf.cNodes)) :
        i = jf.cNodes[i_idx];
        for j_idx in range(len(jf.sNodes[i_idx])) :
            j = jf.sNodes[i_idx][j_idx];
            
            if not E.isExcluded(i,j) :
                # only if (i,j) is not already modelled perfectly
                
                if G.hasEdge(i,j) :
                    # there is an edge
                    if E.isCovered(i,j) :
                        if E.isModellingError(i,j) :
                            E.delModellingError(i,j); # model said 0, we fix to 1
                    else :
                        # edge is there, but not covered, we fix it
                        E.delUnmodelledError(i,j);
                        E.cover(i,j);
                else :
                    # there is no edge
                    if E.isCovered(i,j) :
                        if not E.isModellingError(i,j) :
                            E.addModellingError(i,j); # model said 0, but we say 1
                    else :
                        E.addModellingError(i,j);
                        E.cover(i,j);

    if config.optModelZeroes == True :
        # 3. model that the spokes within a set are not connected    
        # !!!   code can be made more efficient, by incorporating it in previous loop
        for i_idx in range(len(jf.cNodes)) :
            
            for j_idx in range(len(jf.sNodes[i_idx])-1) :
                j = jf.sNodes[i_idx][j_idx];
                
                for k_idx in range(j_idx+1,len(jf.sNodes[i_idx])) :
                    k = jf.sNodes[i_idx][k_idx];
                    
                    if not E.isExcluded(j,k) :
                        # only if (i,j) is not already modelled perfectly
                        
                        #if E.isModelled(j,k) :
                            # we don't change previous modelling, but
                        if not E.isModelled(j,k) :
                            # cell not yet modelled, and should be a 0
                            if G.hasEdge(j,k) :
                                # but, it has a 1, change it to modelling error
                                E.delUnmodelledError(j,k);
                                E.addModellingError(j,k);
                            E.cover(j,k);
    return;
    

# Encoded Size of a core periphery
def LcorePeriphery(cp, M, G, E) :
    # update Error
    coverCorePeriphery(G, E, cp);
    
    cost = LN(cp.numCores);     # number of core-nodes
    cost += LN(cp.numSpokes);       # number of spoke-nodes
    cost += cp.numCores * log(G.numNodes, 2);   # identify core-nodes
    cost += cp.numSpokes * log(G.numNodes - cp.numCores, 2);    # identify spoke-nodes
    return cost;
    
# check whether ok
def coverCorePeriphery(G, E, cp) :
    for i in cp.cNodes :
        for j in cp.sNodes :
            if not E.isModelled(i,j) :
                if G.hasEdge(i,j) :
                    E.delUnmodelledError(i,j);
                else :
                    E.addModellingError(i,j);
                E.cover(i,j);
    return;
    
# Encoded Size of a core periphery (a bit smarter)
def LcorePeripheryA(cp, M, G, E) :
    cost = LN(cp.numCoreNodes);     # number of core-nodes
    cost += LN(cp.numSpokes);       # number of spoke-nodes
    cost += LU(G.numNodes, cp.numCoreNodes);    # identify core-nodes
    cost += LU(G.numNodes - cp.numCoreNodes, cp.numSpokes); # identify spoke-nodes
    return cost;
    
    
### Encoding the Error

# here I encode all errors uniformly by a binomial -- hence, not yet the typed advanced stuff yet!
def LErrorNaiveBinom(G, M, E) :
    # possible number of edges in an undirected, non-self-connected graph of N nodes
    posNumEdges = (G.numNodes * G.numNodes - G.numNodes) / 2
    cost = LU(posNumEdges - E.numCellsExcluded, E.numUnmodelledErrors + E.numModellingErrors);
    if config.optVerbosity > 1 : print ' - L_nb(E)', cost;
    return cost;

def LErrorNaivePrefix(G, M, E) :
    # possible number of edges in an undirected, non-self-connected graph of N nodes
    posNumEdges = (G.numNodes * G.numNodes - G.numNodes) / 2
    cost = LnU(posNumEdges - E.numCellsExcluded, E.numModellingErrors + E.numUnmodelledErrors);
    if config.optVerbosity > 1 : print ' - L_np(E)', cost;
    return cost;

# here I encode all errors uniformly by a binomial -- hence, not yet the typed advanced stuff yet!
def LErrorTypedBinom(G, M, E) :
    # possible number of edges in an undirected, non-self-connected graph of N nodes
    posNumEdges = (G.numNodes * G.numNodes - G.numNodes) / 2
    
    # First encode the modelling errors
    #print 'First encode the modelling errors'
    #print 'E.numCellsCovered, E.numCellsExcluded, E.numModellingErrors;'
    #print E.numCellsCovered, E.numCellsExcluded, E.numModellingErrors;
    costM = LU(E.numCellsCovered - E.numCellsExcluded, E.numModellingErrors);
    if config.optVerbosity > 1 : print ' - L_tb(E+)', costM;

    # Second encode the unmodelled errors
    #print 'Second encode the unmodelled errors' (excluded cells are always covered!)
    #print posNumEdges - E.numCellsCovered, E.numUnmodelledErrors;
    costU = LU(posNumEdges - E.numCellsCovered, E.numUnmodelledErrors);
    if config.optVerbosity > 1 : print ' - L_tb(E-)', costU;
    return costM + costU;

def LErrorTypedPrefix(G, M, E) :
    # possible number of edges in an undirected, non-self-connected graph of N nodes
    posNumEdges = (G.numNodes * G.numNodes - G.numNodes) / 2
    costM = LnU(E.numCellsCovered - E.numCellsExcluded, E.numModellingErrors);
    if config.optVerbosity > 1 : print ' - L_tp(E+)', costM;
    costU = LnU(posNumEdges - E.numCellsCovered, E.numUnmodelledErrors);
    if config.optVerbosity > 1 : print ' - L_tp(E-)', costU;
    return costM + costU;
